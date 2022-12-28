from typing import List, Union

# from .blueprints import Blueprint
# from .hardware import Component
# from .parameters import Parameter
# from .platforms import AbstractPlatform
# from .reagents import Reagent
# from .steps.core import Step

###############
# Base Errors #
###############


class XDLError(Exception):
    """Base XDL error."""

    pass


class XDLGraphError(XDLError):
    """Graph related error."""

    pass


class XDLCompilationError(XDLError):
    """Error occurring during compilation."""

    pass


class XDLExecutionError(XDLError):
    """Error occurring during execution."""

    pass


class XDLValueError(XDLError):
    """Invalid value supplied."""

    pass


class XDLSanityCheckError(XDLError):
    """Step sanity check failed."""

    pass


#######################
# File I/O and Syntax #
#######################


class XDLInvalidFileTypeError(XDLError):
    """Tried to instantiate XDL with invalid file type."""

    def __init__(self, file_ext):
        self.file_ext = file_ext

    def __str__(self):
        return (
            f"{self.file_ext} is an invalid XDL file type. Valid file types:"
            " .xdl, .xdlexe, .json"
        )


class XDLInvalidSaveFormatError(XDLError):
    """Tried to save XDL with invalid file format."""

    def __init__(self, file_format: str):
        self.file_format = file_format

    def __str__(self):
        return (
            f'"{self.file_format}" is an invalid file format for saving XDL.'
            ' Valid file formats: "xml", "json".'
        )


class XDLVesselNotDeclaredError(XDLError):
    """Vessel used in procedure but not declared in Hardware section."""

    def __init__(self, step: "Step"):  # noqa: F821
        self.vessel = step.properties["vessel"]

        # let user know if declaration is missing in specific blueprint
        if hasattr(step.context.xdl(), "id"):
            self.section = step.context.xdl().id + " Blueprint"
        else:
            self.section = "Synthesis section"

    def __str__(self):
        return (
            f'"{self.vessel}" used as vessel in procedure but not declared in'
            f" <Hardware> section of XDL ({self.section})"
        )


class XDLReagentNotDeclaredError(XDLError):
    """Reagent used in procedure but not declared in Reagents section."""

    def __init__(self, step: "Step"):  # noqa: F821
        self.reagent = step.properties["reagent"]

        # let user know if declaration is missing in specific blueprint
        if hasattr(step.context.xdl(), "id"):
            self.section = step.context.xdl().id + " Blueprint"
        else:
            self.section = "Synthesis section"

    def __str__(self):
        return (
            f'"{self.reagent}" used as reagent in procedure but not declared in'
            f" <Reagents> section of XDL ({self.section})"
        )


class XDLDuplicateParameterID(XDLError):
    """Parameters can not be resolved as there is a duplicate parameter id"""

    def __init__(self, parameter: str, matches: List):
        self.parameter = parameter
        self.matches = matches

    def __str__(self):
        return (
            f'Parameter "{self.parameter}" could not be mapped as there are'
            " multiple values given with the same ID"
            f" ({[m.id for m in self.matches]})"
        )


class XDLFileNotFoundError(XDLError):
    """File given for loading xdl does not exist."""

    def __init__(self, file_name: str):
        self.file_name = file_name

    def __str__(self):
        return f"{self.file_name} does not exist."


class XDLInvalidInputError(XDLError):
    """Object given to instantiate XDL is not a file path, XML XDL string or XDL
    JSON dict.
    """

    def __init__(self, input_str: str):
        self.input_str = input_str

    def __str__(self):
        return (
            "Cannot instantiate XDL from this. Invalid syntax.\n\n" f"{self.input_str}"
        )


class XDLInvalidArgsError(XDLError):
    """Invalid combination of args given to XDL __init__."""

    def __str__(self):
        return (
            "Unable to initialise XDL object, invalid argument combination"
            " given. Either xdl arg must be given with the name of a valid XDL"
            " file or XDL string, or steps, reagents and hardware arguments"
            " must all be given with lists of instantiated objects."
        )


class XDLXMLInvalidRoot(XDLError):
    """Invalid tag for root node in XDL XML."""

    def __init__(self, invalid_root: str, valid_roots: List[str]):
        self.invalid_root = invalid_root
        self.valid_roots = valid_roots

    def __str__(self):
        return (
            f"{self.invalid_root} is not a valid root node for XDL XML."
            " Please choose from the following valid root tags:"
            f" {', '.join(self.valid_roots)}"
        )


class XDLMissingBlueprintElement(XDLError):
    """Tag for blueprint-step is not defined in or accessible from XDL XML."""

    def __init__(self, tag: str, blueprint_tags: List[str]):
        self.tag = tag
        self.blueprint_tags = blueprint_tags

    def __str__(self):
        return (
            f"{self.tag} is not specified in Blueprint XML. The following"
            " blueprint XML tags are present in your XDL file:"
            f" {', '.join(self.blueprint_tags)}."
        )


class XDLMismatchedBlueprintID(XDLError):
    """Mismatch in blueprint id when attempting to spawn steps from a blueprint
    -containing XDL XML.
    """

    def __init__(self, blueprint_id: str, target_id: str):
        self.mismatched_id = blueprint_id
        self.valid_id = target_id

    def __str__(self):
        return (
            f"{self.mismatched_id} does not match id for the {self.valid_id}"
            " blueprint."
        )


class XDLNoParameterValue(XDLError):
    """No 'value' set for Parameter."""

    def __init__(self, parameter_id):
        self.id = parameter_id

    def __str__(self):
        return (
            f'No value for the Parameter "{self.id}". A default value can be'
            ' specified via "value"="example_value" in the Parameters section'
            " or a value can be set when when declaring a blueprint"
            f' ({self.id}="example_value")'
        )


class XDLInvalidBlueprintMappingID(XDLError):
    """Reagent id does not map to any available reagents in Blueprint."""

    def __init__(
        self,
        id: str,  # noqa: A002
        valid_ids: List[str],
        target_class: Union["Component", "Reagent", "Parameter"],  # noqa: F821
    ):
        self.id = id
        self.valid_ids = valid_ids
        self.target_class = target_class

    def __str__(self):
        return (
            f"{self.id} is not a valid Blueprint {self.target_class} id."
            f" Valid {self.target_class} ids for this blueprint:"
            f" {', '.join(self.valid_ids)}"
        )


class XDLAttrDuplicateID(XDLError):
    """Raised if two or more Blueprint, Reagent, Parameter or Component objects
    in the same XDL have the same id / name.
    """

    def __init__(
        self,
        id: str,  # noqa: A002
        target_class: Union[
            "Blueprint", "Reagent", "Parameter", "Component"  # noqa: F821
        ],
    ):
        self.id = id
        self.target_class = target_class

    def __str__(self):
        return (
            f"{self.target_class}s must have unique ids. {self.id} is used at"
            " least twice."
        )


#########
# Graph #
#########


class XDLGraphInvalidFileTypeError(XDLGraphError):
    """Invalid file type given for loading graph."""

    def __init__(self, graph_file: str):
        self.graph_file = graph_file

    def __str__(self):
        return (
            f'Graph file "{self.graph_file}" has any invalid file type. '
            " Valid file types: .json, .graphml"
        )


class XDLGraphFileNotFoundError(XDLGraphError):
    """File path given for graph does not exist."""

    def __init__(self, graph_file: str):
        self.graph_file = graph_file

    def __str__(self):
        return f'Graph file "{self.graph_file}" does not exist.'


class XDLGraphTypeError(XDLGraphError):
    """Object with invalid type given to instantiate graph."""

    def __init__(self, graph_file: str):
        self.graph_file = graph_file

    def __str__(self):
        return (
            f"{type(self.graph_file)} is not a valid type to load a graph"
            " Accepted objects: Paths to .json or .graphml graph files."
            " Contents of .json graph as dict. Networkx MultiDiGraph."
        )


###############
# Compilation #
###############


class XDLDoubleCompilationError(XDLCompilationError):
    """User tries to compile the same XDL object twice."""

    def __str__(self):
        return "Cannot compile same XDL object twice."


#############
# Execution #
#############


class XDLInvalidPlatformControllerError(XDLExecutionError):
    """Invalid platform controller supplied."""

    def __init__(self, platform_controller: str):
        self.platform_controller = platform_controller

    def __str__(self):
        return (
            "Invalid platform controller supplied."
            f" Type: {type(self.platform_controller)}"
            f" Value: {self.platform_controller}"
        )


class XDLExecutionBeforeCompilationError(XDLExecutionError):
    """User tries to execute xdl before compiling it."""

    def __str__(self):
        return (
            "Trying to execute procedure that has not been compiled. First"
            " call xdl_obj.prepare_for_execution(graph)."
        )


class XDLDurationBeforeCompilationError(XDLExecutionError):
    """User tries to calculate duration before compiling procedure."""

    def __str__(self):
        return (
            "Trying to calculate duration for procedure that has not been"
            " compiled. First call xdl_obj.prepare_for_execution(graph)."
        )


class XDLReagentVolumesBeforeCompilationError(XDLExecutionError):
    """User tries to calculate reagents volumes used before compiling
    procedure.
    """

    def __str__(self):
        return (
            "Trying to calculate reagent volumes for procedure that has not"
            " been compiled. First call xdl_obj.prepare_for_execution(graph)."
        )


class XDLExecutionOnDifferentGraphError(XDLExecutionError):
    """User tries to execute XDL using different graph than the one used to
    compile it.
    """

    def __str__(self):
        return (
            "Trying to execute XDL on different graph than the one it was"
            " compiled with."
        )


########
# Misc #
########


class XDLStepIndexError(XDLError):
    """User supplies a step index out of bounds of step list."""

    def __init__(self, step_index: int, len_steps: int):
        self.step_index = step_index
        self.len_steps = len_steps

    def __str__(self):
        return (
            f"{self.step_index} is out of bounds for step list with length"
            f" {self.len_steps}"
        )


class XDLStepNotInStepsListError(XDLError):
    """When user asks to execute a step object that isn't in ``xdl_obj.steps``."""

    def __init__(self, step):
        self.step = step

    def __str__(self):
        return (
            f"Given step not found in steps list.\n\n"
            f"{self.step.name}\n"
            f"{self.step.properties}"
        )


class XDLInvalidPlatformError(XDLError):
    """User supplies an invalid platform."""

    def __init__(self, platform):
        self.platform = platform

    def __str__(self):
        return (
            f"{self.platform} is an invalid platform. Platform must be"
            ' "chemputer" or a subclass of AbstractPlatform.'
        )


class XDLNoPlatformSuppliedError(XDLError):
    """User has not supplied an appropriate platform."""

    def __init__(self):
        pass

    def __str__(self):
        return (
            "No XDL platform has been supplied. Please supply an appropriate"
            " XDLPlatform to execute with your XDL."
        )


class XDLPlatformMismatchError(XDLError):
    def __init__(self):
        pass

    def __str__(self):
        return (
            "XDL platforms differ when adding two XDL objects together."
            " Please ensure that both platforms are the same class of Platform."
        )


class XDLLanguageUnavailableError(XDLError):
    """User requests human readable in a language that is unavailable."""

    def __init__(self, language, available_languages=None):
        self.language = language
        self.available_languages = available_languages

    def __str__(self):
        s = f"Language {self.language} not supported."
        if self.available_languages is not None:
            s += f'Available languages: {", ".join(self.available_languages)}'
        return s


class XDLMissingStepError(XDLError):
    def __init__(self, step_name: str, platform: "AbstractPlatform"):  # noqa: F821
        self.step_type = step_name
        self.valid_steps = list(platform.step_library)

    def __str__(self):
        return (
            f"{self.step_type} is not a valid step. Available steps:"
            f" {', '.join(self.valid_steps)}."
        )


class XDLInvalidStepsTypeError(XDLError):
    def __init__(self, steps_type):
        self.steps_type = steps_type

    def __str__(self):
        return (
            f"Invalid type for steps: {self.steps_type}\n"
            "Valid types: List or Dict with steps sections."
        )


class XDLUnimplementedStepError(XDLCompilationError):
    def __init__(self, step_name: str) -> None:
        self.step_name = step_name

    def __str__(self):
        return f'"{self.step_name}" is an unimplemented step.' "Unable to compile."


class XDLTracerError(XDLError):
    def __init__(self, step_name, properties, step_list_index):
        self.step_name = step_name
        self.properties = properties
        self.step_list_index = step_list_index

    def __str__(self):
        return (
            "End of Tracer reached. Could not find step\n"
            f"{self.step_name}\n"
            "with the following properties:\n"
            f"{self.properties}\n"
            f"at the index {self.step_list_index} of the step list."
        )


##################
# Step Templates #
##################


class XDLStepTemplateError(XDLError):
    """Error related to abstract step templates."""

    pass


class XDLStepTemplateMissingPropError(XDLStepTemplateError):
    """Step implementation missing mandatory prop."""

    def __init__(self, name, prop, prop_type):
        self.name = name
        self.prop = prop
        self.prop_type = prop_type

    def __str__(self):
        return (
            f'"{self.name}" step template requires an "{self.prop}"'
            f" ({self.prop_type}) property, but this has not been found in"
            " PROP_TYPES."
        )


class XDLStepTemplatePropTypeError(XDLStepTemplateError):
    """Step implementation has an invalid prop type."""

    def __init__(self, name, prop, prop_type, invalid_prop_type):
        self.name = name
        self.prop = prop
        self.prop_type = prop_type
        self.invalid_prop_type = invalid_prop_type

    def __str__(self):
        return (
            f'"{self.name}" step template requires that "{self.prop}" has prop'
            f" type {str(self.prop_type)}. Prop type found is"
            f" {str(self.invalid_prop_type)}."
        )


class XDLStepTemplateMissingDefaultPropError(XDLStepTemplateError):
    """Step implementation missing mandatory default prop."""

    def __init__(self, name, prop, default_prop):
        self.name = name
        self.prop = prop
        self.default_prop = default_prop

    def __str__(self):
        return (
            f'"{self.name}" step template requires that "{self.prop}" has a'
            f" default value of {self.default_prop}, but this has not been"
            " found in DEFAULT_PROPS."
        )


class XDLStepTemplateInvalidDefaultPropError(XDLStepTemplateError):
    """Step implementation has invalid default prop."""

    def __init__(self, name, prop, default_prop, invalid_default_prop):
        self.name = name
        self.prop = prop
        self.default_prop = default_prop
        self.invalid_default_prop = invalid_default_prop

    def __str__(self):
        return (
            f'"{self.name}" step template requires that "{self.prop}" has a'
            f" default value of {str(self.default_prop)}. Default value found"
            f" is {str(self.invalid_default_prop)}."
        )


class XDLStepTemplateMissingPropLimitError(XDLStepTemplateError):
    """Step implementation missing mandatory prop limit."""

    def __init__(self, name, prop, prop_limit):
        self.name = name
        self.prop = prop
        self.prop_limit = prop_limit

    def __str__(self):
        return (
            f'"{self.name}" step template requires that "{self.prop}" has'
            f" prop_limit {self.prop_limit}, but this has not been found in"
            "PROP_LIMITS."
        )


class XDLStepTemplateInvalidPropLimitError(XDLStepTemplateError):
    """Step implementation has invalid prop limit."""

    def __init__(self, name, prop, prop_limit, invalid_prop_limit):
        self.name = name
        self.prop = prop
        self.prop_limit = prop_limit
        self.invalid_prop_limit = invalid_prop_limit

    def __str__(self):
        return (
            f'"{self.name}" step template requires that "{self.prop}" has a'
            " prop limit {str(self.prop_limit)}. Prop limit found is"
            f" {str(self.invalid_prop_limit)}."
        )


class XDLStepTemplateNameError(XDLStepTemplateError):
    """Step implementation has invalid name."""

    def __init__(self, mandatory_name, name):
        self.mandatory_name = mandatory_name
        self.name = name

    def __str__(self):
        return (
            f"{self.mandatory_name} step must have class name"
            f" {self.mandatory_name}. Name found: {self.name}."
        )


##############
# Prop Types #
##############


class XDLUndeclaredDefaultPropError(XDLError):
    """Prop included in ``DEFAULT_PROPS`` but not in ``PROP_TYPES``."""

    def __init__(self, step_name, prop):
        self.step_name = step_name
        self.prop = prop

    def __str__(self):
        return (
            f"{self.step_name} step class has {self.prop} in DEFAULT_PROPS but"
            " not in PROP_TYPES."
        )


class XDLUndeclaredPropLimitError(XDLError):
    """Prop included in ``PROP_LIMITS`` but not in ``PROP_TYPES``."""

    def __init__(self, step_name, prop):
        self.step_name = step_name
        self.prop = prop

    def __str__(self):
        return (
            f"{self.step_name} step class has {self.prop} in PROP_LIMITS but"
            " not in PROP_TYPES."
        )


class XDLUndeclaredInternalPropError(XDLError):
    """Prop included in ``INTERNAL_PROPS`` but not in ``PROP_TYPES``."""

    def __init__(self, step_name, prop):
        self.step_name = step_name
        self.prop = prop

    def __str__(self):
        return (
            f"{self.step_name} step class has {self.prop} in INTERNAL_PROPS but"
            " not in PROP_TYPES."
        )


class XDLUndeclaredAlwaysWriteError(XDLError):
    """Prop included in ``ALWAYS_WRITE`` but not in ``PROP_TYPES``."""

    def __init__(self, step_name, prop):
        self.step_name = step_name
        self.prop = prop

    def __str__(self):
        return (
            f"{self.step_name} step class has {self.prop} in ALWAYS_WRITE but"
            " not in PROP_TYPES."
        )


class XDLMissingDefaultPropError(XDLError):
    """``'default'`` given as value for prop but prop not in ``DEFAULT_PROPS``."""

    def __init__(self, xdl_element_name, prop):
        self.xdl_element_name = xdl_element_name
        self.prop = prop

    def __str__(self):
        return (
            f'"default" given as value for {self.prop} property, but no default'
            f" value found in {self.xdl_element_name} DEFAULT_PROPS."
        )


class XDLMissingPropTypeError(XDLError):
    """Value given for prop but prop not in ``PROP_TYPES``."""

    def __init__(self, xdl_element_name, prop):
        self.xdl_element_name = xdl_element_name
        self.prop = prop

    def __str__(self):
        return f"Missing prop type for {self.prop} in {self.xdl_element_name}\
 class."


class XDLFailedPropLimitError(XDLValueError):
    """Value given for prop does not match prop limit."""

    def __init__(self, xdl_element_name, prop, value, prop_limit):
        self.xdl_element_name = xdl_element_name
        self.prop = prop
        self.value = value
        self.prop_limit = prop_limit

    def __str__(self):
        return (
            f'{self.xdl_element_name}: Value "{self.value}" does not match'
            f' "{self.prop}" prop limit. {self.prop_limit.hint}'
        )


class XDLTypeConversionError(XDLValueError):
    """Error occurred converting value to prop type."""

    def __init__(self, xdl_element_name, prop, prop_type, value):
        self.xdl_element_name = xdl_element_name
        self.prop = prop
        self.value = value
        self.prop_type = prop_type

    def __str__(self):
        return (
            f"{self.xdl_element_name}: Unable to convert {self.prop} value"
            f" {self.value} to {self.prop_type}."
        )


class XDLInvalidEquivalentsInput(XDLError):
    """Invalid prepare_for_execution input for equivalents. Both equiv_amount
    and equiv_reference must be supplied.
    """

    def __init__(self, equiv_amount, equiv_reference):

        if not equiv_amount:
            self.provided = "equiv_reference"
            self.notprovided = "equiv_amount"

        if not equiv_reference:
            self.provided = "equiv_amount"
            self.notprovided = "equiv_reference"

    def __str__(self):
        return (
            f"Must provide both equivalents arguments. {self.provided} \n\n"
            f" provided but not {self.notprovided}."
        )


class XDLEquivReferenceNotInReagents(XDLError):
    """``equiv_reference`` passed in to prepare_for_execution method does not
    match any reagents.
    """

    def __init__(self, reagents, equiv_reference):
        self.reagents = reagents

        if reagents is not None:
            self.reagents = ", ".join([r.name for r in reagents])

        self.equiv_reference = equiv_reference

    def __str__(self):
        return (
            f"Equivalent reference {self.equiv_reference} does not map to any"
            " reagents. Either update Reagents section of XDL or choose one of"
            " the following reagents as an equivalent reference:\n"
            f"{self.reagents}."
        )
