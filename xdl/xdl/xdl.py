from typing import List, Dict, Any, Union, Optional
import os
import copy
import logging
import json
import re
import datetime

from .errors import (
    XDLReagentNotDeclaredError,
    XDLVesselNotDeclaredError,
    XDLInvalidFileTypeError,
    XDLInvalidPlatformControllerError,
    XDLStepIndexError,
    XDLExecutionBeforeCompilationError,
    XDLInvalidPlatformError,
    XDLInvalidInputError,
    XDLFileNotFoundError,
    XDLInvalidArgsError,
    XDLDoubleCompilationError,
    XDLLanguageUnavailableError,
    XDLInvalidSaveFormatError,
    XDLDurationBeforeCompilationError,
    XDLReagentVolumesBeforeCompilationError,
)
from .hardware import Hardware
from .platforms.abstract_platform import AbstractPlatform
from .reagents import Reagent
from .readwrite.utils import read_file
from .readwrite.xml_interpreter import xdl_str_to_objs
from .readwrite.xml_generator import xdl_to_xml_string
from .readwrite.json import xdl_to_json, xdl_from_json_file, xdl_from_json
from .steps import Step, AbstractBaseStep
from .utils import get_logger
from .utils.vessels import VesselSpec
from .utils.misc import (
    steps_are_equal,
    xdl_elements_are_equal,
    reagent_volumes_table
)
from .utils.localisation import get_available_languages

class XDL(object):
    """
    Interpets XDL (file or str) and provides an object for further use.

    Attributes:
        base_steps (List[AbstractBaseStep]): List of base steps used by
            procedure.
        compiled (bool): True if XDL procedure has been compiled and is ready to
            execute, otherwise False.
        graph_sha256 (str): Graph hash of the graph the procedure was compiled
            with. If procedure has not been compiled, None.

    Methods:
        # Information
        human_readable -> str: Returns entire procedure in human readable form.
        duration(fmt=False) -> Union[int, str]: Returns time in seconds, or
            formatted duration if fmt is True. Only callable after compilation.
        reagent_volumes -> Dict[str, float]: Return Dict of reagents and the
            total volumes of the reagents used in the procedure. Only callable
            after compilation.

        # Tools
        scale_procedure(scale): Scale volumes in procedure by given scale factor
        graph(graph_template, save) -> MultiDiGraph: Generate hardware graph to
            use for compilation and execution. If graph template given, use this
            to generate graph rather than default template. If save given,
            save graph to this file.
        prepare_for_execution(graph, **kwargs): Compile procedure for execution
            on given graph.
        execute(platform_controller, step): Execute compiled procedure using
            given platform controller. If int is given for step, only execute
            step at that index of self.steps.

        # Output
        as_string -> str: Return XML string of XDL
        as_json -> Dict: Return XDL JSON format Dict
        as_json_string -> str: Return XDL JSON format string
        save(save_path, file_format): Save to given file in xml or json format.

    """
    # File name XDL was initialised from
    _xdl_file = None

    # Graph hash contained in <Synthesis> tag if XDL object is from xdlexe file
    graph_sha256 = None

    # True if XDL is loaded from xdlexe, or has been compiled, otherwise False
    # self.compiled == True implies that procedure is ready to execute
    compiled = False

    def __init__(
        self,
        xdl: str = None,
        steps: List[Step] = None,
        hardware: Hardware = None,
        reagents: List[Reagent] = None,
        logging_level: int = logging.INFO,
        platform: Union[str, AbstractPlatform] = 'chemputer',
    ) -> None:
        """Init method for XDL object.
        One of xdl or (steps, hardware and reagents) must be given.

        Args:
            xdl(str, optional): Path to XDL file or XDL str.
            steps (List[Step], optional): List of Step objects.
            hardware (Hardware, optional): Hardware object containing all
                components in XDL.
            reagents (List[Reagent], optional): List of Reagent objects.
            logger (logging.Logger): Logger object to use. If not given will
                be made.
            platform (str): Platform to run XDL on. 'chemputer' or 'chemobot'.

        Raises:
            ValueError: If insufficient args provided to instantiate object.
        """

        self._initialize_logging(logging_level)
        self._load_platform(platform)
        self._load_xdl(xdl, steps=steps, hardware=hardware, reagents=reagents)

        self.executor = self.platform.executor(self)
        self.compiled = self.graph_sha256 is not None

        self._validate_loaded_xdl()

    ##################
    # Initialization #
    ##################

    def _initialize_logging(self, logging_level: int) -> None:
        """Initialize logger with given logging level."""
        self.logger = get_logger()
        self.logger.setLevel(logging_level)
        self.logging_level = logging_level

    def _load_platform(self, platform: Union[str, AbstractPlatform]) -> None:
        """Initialise given platform. If 'chemputer' given initialise
        ChemputerPlatform otherwise platform should be a subclass of
        AbstractPlatform.

        Args:
            platform (Union[str, AbstractPlatform])

        Raises:
            XDLInvalidPlatformError: If platform is not 'chemputer' or a
                subclass of AbstractPlatform.
        """
        if platform == 'chemputer':
            from chemputerxdl import ChemputerPlatform
            self.platform = ChemputerPlatform()
        elif issubclass(platform, AbstractPlatform):
            self.platform = platform()
        else:
            raise XDLInvalidPlatformError(platform)

    def _load_xdl(
        self,
        xdl: str,
        steps: List[Step],
        reagents: List[Reagent],
        hardware: Hardware
    ) -> None:
        """Load XDL from given arguments. Valid argument combinations are
        just xdl, or all of steps, reagents and hardware. xdl can be a path to a
        .xdl, .xdlexe or .json file, or an XML string of the XDL.

        Args:
            xdl (str): Path to .xdl, .xdlexe or .json XDL file, or XML string.
            steps (List[Step]): List of Step objects to instantiate XDL with.
            reagents (List[Reagent]): List of Reagent objects to instantiate XDL
                with.
            hardware (Hardware): Hardware object to instantiate XDL with.

        Raises:
            XDLFileNotFoundError: xdl file given, but file not found.
            XDLInvalidInputError: xdl is not file or valid XML string.
            XDLInvalidArgsError: Invalid combination of arguments given.
                Valid argument combinations are just xdl, or all of steps,
                reagents and hardware.
        """
        # Load from XDL file or string
        if xdl:
            # Load from JSON dict
            if type(xdl) == dict:
                self._load_xdl_from_json_dict(xdl)

            elif type(xdl) == str:
                # Load from file
                if os.path.exists(xdl):
                    self._load_xdl_from_file(xdl)

                # Incorrect file path, raise error.
                elif xdl.endswith(('.xdl', '.xdlexe', '.json')):
                    raise XDLFileNotFoundError(xdl)

                # Load XDL from string, check string is not mismatched file path
                elif '<Synthesis' in xdl and '<Procedure>' in xdl:
                    self._load_xdl_from_xml_string(xdl)

            # Invalid input, raise error
            else:
                raise XDLInvalidInputError(xdl)

        # Initialise XDL from lists of Step, Reagent and Component objects
        elif (steps is not None
              and reagents is not None
              and hardware is not None):
            self.steps, self.hardware, self.reagents = steps, hardware, reagents
            self.executor = self.platform.executor(self)

        # Invalid combination of arguments given, raise error
        else:
            raise XDLInvalidArgsError()

    def _load_xdl_from_json_dict(self, xdl_json):
        """Load XDL from JSON dict.

        Args:
            xdl_json (Dict): XDL JSON dict.
        """
        parsed_xdl = xdl_from_json(xdl_json, self.platform)
        self.steps = parsed_xdl['steps']
        self.hardware = parsed_xdl['hardware']
        self.reagents = parsed_xdl['reagents']

    def _load_xdl_from_file(self, xdl_file):
        """Load XDL from .xdl, .xdlexe or .json file.

        Args:
            xdl_file (str): .xdl, .xdlexe or .json file to load XDL from.

        Raises:
            XDLInvalidFileTypeError: If given file is not .xdl, .xdlexe or .json
        """
        file_ext = os.path.splitext(xdl_file)[1]

        # Load from XML .xdl or .xdlexe file
        if file_ext == '.xdl' or file_ext == '.xdlexe':
            self._xdl_file = xdl_file
            xdl_str = read_file(xdl_file)
            self._load_xdl_from_xml_string(xdl_str)

        # Load from .json file
        elif file_ext == '.json':
            parsed_xdl = xdl_from_json_file(xdl_file, self.platform)
            self.steps = parsed_xdl['steps']
            self.hardware = parsed_xdl['hardware']
            self.reagents = parsed_xdl['reagents']

        # Invalid file type, raise error
        else:
            raise XDLInvalidFileTypeError(file_ext)

    def _load_xdl_from_xml_string(self, xdl_str):
        """Load XDL from XML string.

        Args:
            xdl_str (str): XML string of XDL.
        """
        parsed_xdl = xdl_str_to_objs(
            xdl_str=xdl_str, logger=self.logger, platform=self.platform)

        self._load_graph_hash(xdl_str)

        self.steps = parsed_xdl['steps']
        self.hardware = parsed_xdl['hardware']
        self.reagents = parsed_xdl['reagents']

    def _load_graph_hash(self, xdl_str: str) -> Optional[str]:
        """Obtain graph hash from given xdl str. If xdl str is not xdlexe, there
        will be no graph hash so return None.
        """
        graph_hash_search = re.search(r'graph_sha256="([a-z0-9]+)"', xdl_str)
        if graph_hash_search:
            self.graph_sha256 = graph_hash_search[1]

    def _validate_loaded_xdl(self):
        """Validate loaded XDL at end of __init__"""
        # Validate all vessels and reagents used in procedure are declared in
        # corresponding sections of XDL. Don't do this if XDL object is compiled
        # (xdlexe) as there will be lots of undeclared vessels from the graph.
        if not self.compiled:
            self._validate_vessel_and_reagent_props()

    def _validate_vessel_and_reagent_props(self):
        """Validate that all vessels and reagents used in procedure are declared
        in corresponding sections of XDL.

        Raises:
            XDLReagentNotDeclaredError: If reagent used in step but not declared
            XDLVesselNotDeclaredError: If vessel used in step but not declared
        """
        reagent_ids = [reagent.id for reagent in self.reagents]
        vessel_ids = [vessel.id for vessel in self.hardware]
        for step in self.steps:
            self._validate_vessel_and_reagent_props_step(
                step, reagent_ids, vessel_ids
            )

    def _validate_vessel_and_reagent_props_step(
            self, step, reagent_ids, vessel_ids):
        """Validate that all vessels and reagents used in given step are
        declared in corresponding sections of XDL.

        Args:
            step (Step): Step to validate all vessels and reagents declared.
            reagent_ids (List[str]): List of all declared reagent ids.
            vessel_ids (List[str]): List of all declared vessel ids.

        Raises:
            XDLReagentNotDeclaredError: If reagent used in step but not declared
            XDLVesselNotDeclaredError: If vessel used in step but not declared
        """
        for prop, prop_type in step.PROP_TYPES.items():
            # Check vessel has been declared
            if prop_type == 'vessel':
                vessel = step.properties[prop]
                if vessel and vessel not in vessel_ids:
                    raise XDLVesselNotDeclaredError(vessel)

            # Check reagent has been declared
            elif prop_type == 'reagent':
                reagent = step.properties[prop]
                if reagent and reagent not in reagent_ids:
                    raise XDLReagentNotDeclaredError(reagent)

        # Check child steps, don't need to check substeps as they aren't
        # obligated to have all vessels used explicitly declared.
        if hasattr(step, 'children'):
            for substep in step.children:
                self._validate_vessel_and_reagent_props_step(
                    substep, reagent_ids, vessel_ids
                )

    ###############
    # Information #
    ###############

    def human_readable(self, language='en') -> str:
        """Return human-readable English description of XDL procedure.

        Arguments:
            language (str): Language code corresponding to language that should
                be used. If language code not supported error message will be
                logged and no human_readable text will be logged.

        Returns:
            str: Human readable description of procedure.
        """
        s = ''
        # Get available languages
        available_languages = get_available_languages(
            self.platform.localisation)

        # Print human readable for every step.
        if language in available_languages:
            for i, step in enumerate(self.steps):
                s += f'{i+1}) {step.human_readable(language=language)}\n'

        # Language unavailable, raise error
        else:
            raise XDLLanguageUnavailableError(language, available_languages)

        return s

    def duration(self, fmt=False) -> Union[int, str]:
        """Estimated duration of procedure. It is approximate but should give a
        give a rough idea how long the procedure should take.

        Returns:
            int: Estimated runtime of procedure in seconds.
        """
        # If not compiled, raise error
        if not self.compiled:
            raise XDLDurationBeforeCompilationError()

        # Calculate duration
        duration = 0
        for step in self.steps:
            duration += step.duration(self.executor._graph)

        # Return formatted time string
        if fmt:
            timedelta = datetime.timedelta(seconds=int(duration))
            return str(timedelta)

        # Return duration in seconds
        return int(duration)

    def reagent_volumes(self, fmt=False) -> Dict[str, float]:
        """Compute volumes used of all liquid reagents in procedure and return
        as dict.

        Returns:
            Dict[str, float]: Dict of { reagent_name: volume_used... }
        """
        # Not compiled, raise error
        if not self.compiled:
            raise XDLReagentVolumesBeforeCompilationError()

        # Calculate volume of liquid reagents consumed by procedure
        reagents_consumed = {}
        for step in self.steps:
            step_reagents_consumed = step.reagents_consumed(
                self.executor._graph)
            for reagent, volume in step_reagents_consumed.items():
                if reagent in reagents_consumed:
                    reagents_consumed[reagent] += volume
                else:
                    reagents_consumed[reagent] = volume

        # Return pretty printed table str
        if fmt:
            return reagent_volumes_table(reagents_consumed)

        # Return Dict[str, float] of reagent volumes consumed by procedure.
        return reagents_consumed

    @property
    def base_steps(self) -> List[AbstractBaseStep]:
        """List of base steps of XDL procedure.

        Returns:
            List[AbstractBaseStep]: List of base steps of XDL procedure.
        """
        base_steps = []
        for step in self.steps:
            base_steps.extend(step.base_steps)
        return base_steps

    @property
    def vessel_specs(self) -> Dict[str, VesselSpec]:
        """Get specification of every vessel in procedure."""
        vessel_specs = {}
        for step in self.steps:
            for prop, spec in step.vessel_specs.items():
                vessel = step.properties[prop]
                if vessel in vessel_specs:
                    vessel_specs[vessel] += spec
                else:
                    vessel_specs[vessel] = spec
        return vessel_specs

    #########
    # Tools #
    #########

    def scale_procedure(self, scale: float) -> None:
        """Scale all volumes and masses in procedure.

        Args:
            scale (float): Number to scale all volumes and masses by.
        """
        for step in self.steps:
            self._apply_scaling(step, scale)

    def _apply_scaling(self, step: Step, scale: float) -> None:
        """Apply scale to steps, recursively applying to any child steps if the
        step has the attribute 'children', e.g. Repeat steps.

        Args:
            step (Step): Step to apply scaling to.
            scale (float): Amount to scale volumes and masses.
        """
        step.scale(scale)
        if hasattr(step, 'children') and step.children:
            for substep in step.children:
                self._apply_scaling(substep, scale)

    def graph(
        self,
        graph_template=None,
        save=None,
        **kwargs
    ):
        """Return graph to run procedure with, built on template.

        Returns:
            Dict: JSON node link graph as dictionary.
        """
        return self.platform.graph(
            self,
            template=graph_template,
            save=save,
            **kwargs
        )

    def prepare_for_execution(
        self,
        graph_file: str = None,
        interactive: bool = True,
        save_path: str = None,
        sanity_check: bool = True,
        **kwargs
    ) -> None:
        """Check hardware compatibility and prepare XDL for execution on given
        setup.

        Args:
            graph_file (str, optional): Path to graph file. May be GraphML file,
                JSON file with graph in node link format, or dict containing
                graph in same format as JSON file.
        """
        # Not already compiled, try to compile procedure.
        if not self.compiled:

            # Get XDLEXE save path from name of _xdl_file used to instantiate
            # XDL object.
            if self._xdl_file:
                save_path = self._xdl_file.replace('.xdl', '.xdlexe')

            # Compile procedure
            self.executor.prepare_for_execution(
                graph_file,
                interactive=interactive,
                sanity_check=sanity_check,
                **kwargs
            )

            # Save XDLEXE, switch self.compiled flag to True, and log reagent
            # volumes consumed by procedure and estimated duration.
            if self.executor._prepared_for_execution:
                # Save XDLEXE
                self.graph_sha256 = self.executor._graph_hash()
                if save_path:
                    xdlexe = xdl_to_xml_string(
                        self,
                        graph_hash=self.graph_sha256,
                        full_properties=True,
                        full_tree=True
                    )
                    with open(save_path, 'w') as fd:
                        fd.write(xdlexe)

                # Switch self.compiled flag to True and log procedure info
                self.compiled = True
                self.logger.info(
                    f'Reagents Consumed\n{self.reagent_volumes(fmt=True)}\n')
                self.logger.info(
                    f'Estimated duration: {self.duration(fmt=True)}\n')

        # XDL object already compiled, raise error
        else:
            raise XDLDoubleCompilationError()

    def execute(self, platform_controller: Any, step: int = None) -> None:
        """Execute XDL using given platform controller object.
        XDL object must either be loaded from a xdlexe file, or it must have
        been prepared for execution.

        Args:
            platform_controller (Any): Platform controller object instantiated
            with modules and graph to run XDL on.
        """
        # Check step not accidentally passed as platform controller
        if type(platform_controller) in [int, str, list, dict]:
            raise XDLInvalidPlatformControllerError(platform_controller)

        # Check XDL object has been compiled
        if self.compiled:
            # Execute full procedure
            if step is None:
                self.executor.execute(platform_controller)

            # Execute individual step.
            else:
                # Check step index is valid.
                try:
                    self.steps[step]
                except IndexError:
                    raise XDLStepIndexError(step, len(self.steps))

                # Execute step
                self.executor.execute_step(
                    platform_controller, self.steps[step])

        # XDL object not compiled, raise error
        else:
            raise XDLExecutionBeforeCompilationError()

    ##########
    # Output #
    ##########

    def as_string(self) -> str:
        """Return XDL str of procedure."""
        return xdl_to_xml_string(self)

    def as_json(self) -> Dict:
        """Return JSON dict of procedure."""
        return xdl_to_json(self)

    def as_json_string(self, pretty=True) -> str:
        """Return JSON str of procedure."""
        xdl_json = xdl_to_json(self)
        if pretty:
            return json.dumps(xdl_json, indent=2)
        return json.dumps(xdl_json)

    def save(
        self,
        save_file: str,
        file_format: str = 'xml'
    ) -> str:
        """Save as XDL file.

        Args:
            save_file (str): File path to save XDL to.
            full_properties (bool): If True, all properties will be included.
                If False, only properties that differ from their default values
                will be included.
                Including full properties is recommended for making XDL files
                that will stand the test of time, as defaults may change in new
                versions of XDL.
        """
        # Save XML
        if file_format == 'xml':
            xml_string = xdl_to_xml_string(self)
            with open(save_file, 'w') as fd:
                fd.write(xml_string)

        # Save JSON
        elif file_format == 'json':
            with open(save_file, 'w') as fd:
                json.dump(
                    xdl_to_json(self),
                    fd, indent=2
                )

        # Invalid file format given, raise error
        else:
            raise XDLInvalidSaveFormatError(file_format)

    #################
    # Magic Methods #
    #################

    def __str__(self):
        return self.as_string()

    def __add__(self, other: 'XDL') -> 'XDL':
        """Allow two XDL objects to be added together. Steps, reagents and
        components of this object are added to the new object lists first,
        followed by the same lists of the other object.
        """
        reagents, steps, components = [], [], []
        for xdl_obj in [self, other]:
            reagents.extend(xdl_obj.reagents)
            steps.extend(xdl_obj.steps)
            components.extend(list(xdl_obj.hardware))
        new_xdl_obj = XDL(steps=steps, reagents=reagents, hardware=components)
        return new_xdl_obj

    def __eq__(self, other: 'XDL') -> bool:
        """Compare equality of XDL objects based on steps, reagents and
        hardware. Steps are compared based step types and properties, including
        all substeps and child steps. Reagents and Components are compared
        based on properties.
        """
        if type(other) != XDL:
            # Don't raise NotImplementedError here as it causes unnecessary
            # crashes for example `if xdl_obj == None: ...`.
            return False

        # Compare lengths of lists first.
        if len(self.steps) != len(other.steps):
            return False
        if len(self.reagents) != len(other.reagents):
            return False
        if len(self.hardware.components) != len(other.hardware.components):
            return False

        # Detailed comparison of all step types and properties, including all
        # substeps and children.
        for i, step in enumerate(self.steps):
            if not steps_are_equal(step, other.steps[i]):
                return False

        # Compare properties of all reagents
        for i, reagent in enumerate(self.reagents):
            if not xdl_elements_are_equal(reagent, other.reagents[i]):
                return False

        # Compare properties of all components
        for i, component in enumerate(self.hardware.components):
            if not xdl_elements_are_equal(
                    component, other.hardware.components[i]):
                return False

        return True

    def __deepcopy__(self, memo) -> 'XDL':
        """Allow `copy.deepcopy(xdl)` to be called. Default does not work on
        Python 3.6 so that is why this method is here. Once 3.6 is no longer
        supported this method can go.
        """
        copy_steps = []
        copy_reagents = []
        copy_hardware = []

        # Copy steps
        for step in self.steps:
            copy_steps.append(copy.deepcopy(step, memo))

        # Copy reagents
        for reagent in self.reagents:
            copy_props = copy.deepcopy(reagent.properties)
            copy_reagents.append(type(reagent)(**copy_props))

        # Copy hardware
        for component in self.hardware:
            copy_props = copy.deepcopy(component.properties)
            copy_hardware.append(type(component)(**copy_props))

        # Return new XDL object
        return XDL(
            steps=copy_steps,
            reagents=copy_reagents,
            hardware=Hardware(copy_hardware),
            logging_level=self.logging_level
        )
