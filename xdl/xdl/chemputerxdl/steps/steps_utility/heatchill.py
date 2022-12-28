"""
.. module:: steps_utility.heatchill
    :platforms: Unix, Windows
    :synopsis: XDL steps dealing with Heating and Chilling reaction vessels

"""

from typing import Optional, List, Dict, Any

from xdl.steps.base_steps import AbstractStep, Step
from ..base_step import ChemputerStep
from ...constants import (
    CHILLER_MIN_TEMP,
    CHILLER_MAX_TEMP,
    HEATER_MAX_TEMP,
)
from ..steps_base import (
    CChillerSetTemp,
    CStartChiller,
    CSetRecordingSpeed,
    CChillerWaitForTemp,
    CStopChiller,
    CRampChiller,
    CSetCoolingPower,

    CStirrerSetTemp,
    CStirrerHeat,
    CStirrerWaitForTemp,
    CStopHeat,

    CRotavapStartHeater,
    CRotavapStopHeater,
    CRotavapSetTemp,
)
from .general import Wait
from .stirring import StopStir, StartStir
from ...constants import (
    DEFAULT_ROTAVAP_WAIT_FOR_TEMP_TIME
)
from xdl.constants import ROOM_TEMPERATURE, VESSEL_PROP_TYPE
from xdl.utils.misc import SanityCheck
from ...localisation import HUMAN_READABLE_STEPS
#from ...utils.execution import get_heater_chiller, get_vessel_type
from ...utils.prop_limits import VESSEL_TYPE_PROP_LIMIT, VESSEL_CLASS_PROP_LIMIT
from xdl.utils.prop_limits import TEMP_PROP_LIMIT, ROTATION_SPEED_PROP_LIMIT

def heater_chiller_sanity_checks(
    heater: str, chiller: str, temp: float
) -> List[SanityCheck]:
    """Perform sanity checks on heaters and chillers

    Args:
        heater (str): Heater to check
        chiller (str): Chiller to check
        temp (float): Temperatures to check

    Returns:
        List[SanityCheck]: List of checks to perform
    """

    checks = []

    # No heater but chiller
    if not heater and chiller:
        # Add a check for chiller temperatures
        for condition in [
            temp <= CHILLER_MAX_TEMP,
            temp >= CHILLER_MIN_TEMP
        ]:
            checks.append(
                SanityCheck(
                    condition=condition,
                    error_msg=f'{temp} is an invalid temperature for a\
 chiller.',
                )
            )

    # No chiller but heater
    if not chiller and heater:
        # Add a check for heater temperatures
        for condition in [
            temp >= 18,
            temp <= HEATER_MAX_TEMP
        ]:
            checks.append(
                SanityCheck(
                    condition=condition,
                    error_msg=f'{temp} is an invalid temperature for a heater.'
                )
            )

    # Check temperatures are within valid ranges
    checks.append(
        SanityCheck(
            condition=CHILLER_MIN_TEMP <= temp <= HEATER_MAX_TEMP,
            error_msg=f'{temp} is an invalid temperature for a heater or a\
 chiller.'
        )
    )

    return checks

class StartHeatChill(ChemputerStep, AbstractStep):
    """Start heating/chilling vessel to given temp and leave heater/chiller on.
    Don't wait to reach temp.

    Args:
        vessel (str): Vessel to heat/chill.
        temp (float): Temperature to heat/chill to in degrees C.
        vessel_type (str): Given internally. Used to know whether to use
            heater or chiller base steps. 'filter', 'rotavap' or 'reactor'
    """

    PROP_TYPES = {
        'vessel': VESSEL_PROP_TYPE,
        'temp': float,
        'vessel_type': str,
        'heater': str,
        'chiller': str
    }

    PROP_LIMITS = {
        'vessel_type': VESSEL_TYPE_PROP_LIMIT,
        'temp': TEMP_PROP_LIMIT,
    }

    INTERNAL_PROPS = [
        'vessel_type',
        'heater',
        'chiller',
    ]

    def __init__(
        self,
        vessel: str,
        temp: float,

        # Internal properties
        vessel_type: Optional[str] = None,
        heater: Optional[str] = None,
        chiller: Optional[str] = None,
        **kwargs
    ) -> None:
        super().__init__(locals())

    def on_prepare_for_execution(self, graph: Dict):
        """Prepares the current step for execution.
        Gets/sets/cleans up appropriate items in preparation for exection.

        Args:
            graph (Dict): Chemputer Graph to check
        """

        # Obtain the vessel type if not defined
        if not self.vessel_type:
            self.vessel_type = get_vessel_type(graph, self.vessel)

        # Obtain the heater and the chiller
        self.heater, self.chiller = get_heater_chiller(graph, self.vessel)

    def get_steps(self) -> List[Step]:
        """Get the list of steps/base steps to execute.

        Returns:
            List[Step]: Steps to execute.
        """

        steps = []

        # Vessel type is defined
        if self.vessel_type:
            # Rotavap
            if self.vessel_type == 'rotavap':
                steps = self.get_rotavap_steps()

            # Vessel is not a rotavap
            else:
                # Temp less than 25, try use chiller
                if self.chiller:
                    if CHILLER_MIN_TEMP <= self.temp <= CHILLER_MAX_TEMP:
                        steps = self.get_chiller_steps()

                    # Try and use heater
                    elif self.heater and 18 <= self.temp <= HEATER_MAX_TEMP:
                        steps = self.get_heater_steps()

                # Temp greater than 25, try use heater, if not available try
                # use chiller.
                elif self.heater and 18 <= self.temp <= HEATER_MAX_TEMP:
                    steps = self.get_heater_steps()

        return steps

    def get_chiller_steps(self) -> List[Step]:
        """Get steps to start the chiller

        Returns:
            List[Step]: Chiller steps
        """

        return [
            CChillerSetTemp(vessel=self.vessel, temp=self.temp),
            CStartChiller(vessel=self.vessel),
        ]

    def get_heater_steps(self) -> List[Step]:
        """Get steps to start the heater

        Returns:
            List[Step]: Heater steps
        """

        return [
            CStirrerSetTemp(vessel=self.vessel, temp=self.temp),
            CStirrerHeat(vessel=self.vessel),
        ]

    def get_rotavap_steps(self) -> List[Step]:
        """Get steps to start the rotavap heater

        Returns:
            List[Step]: Rotavap heater steps
        """

        return [
            CRotavapSetTemp(rotavap_name=self.vessel, temp=self.temp),
            CRotavapStartHeater(rotavap_name=self.vessel),
        ]

    def sanity_checks(self, graph: Dict) -> List[SanityCheck]:
        """Gets a list of Sanity checks to perform for the step

        Args:
            graph (Dict): Chemputer graph to check

        Returns:
            List[SanityCheck]: List of checks to perform
        """

        return [
            SanityCheck(
                condition=(
                    self.heater
                    or self.chiller
                    or self.vessel_type == 'rotavap'
                ),
                error_msg=f'Trying to heat/chill vessel "{self.vessel}" with\
 no heater or chiller attached.'
            ),
            SanityCheck(
                condition=self.steps,
                error_msg=f'Unable to heat/chill vessel "{self.vessel}".\
 {self.properties}'
            )
        ] + heater_chiller_sanity_checks(self.heater, self.chiller, self.temp)

    @property
    def requirements(self) -> Dict[str, Dict[str, Any]]:
        """Gets the requirements needed for this step.

        Returns:
            Dict[str, Dict[str, Any]]: Requirements for the step.
        """

        return {
            'vessel': {
                'heatchill': True,
                'temp': [self.temp]
            }
        }

class HeatChillSetTemp(ChemputerStep, AbstractStep):
    """Set temp on heater/chiller.

    Args:
        vessel (str): Vessel to set temp.
        temp (float): Temperature to set in degrees C.
        vessel_type (str): Given internally. Used to know whether to use
            heater or chiller base steps. 'filter', 'rotavap' or 'reactor'
    """

    INTERNAL_PROPS = [
        'vessel_type',
        'heater',
        'chiller'
    ]

    PROP_TYPES = {
        'vessel': VESSEL_PROP_TYPE,
        'temp': float,
        'vessel_type': str,
        'heater': str,
        'chiller': str
    }

    PROP_LIMITS = {
        'vessel_type': VESSEL_TYPE_PROP_LIMIT,
        'temp': TEMP_PROP_LIMIT,
    }

    def __init__(
        self,
        vessel: str,
        temp: float,

        # Internal properties
        vessel_type: Optional[str] = None,
        heater: Optional[str] = None,
        chiller: Optional[str] = None,
        **kwargs
    ) -> None:
        super().__init__(locals())

    def on_prepare_for_execution(self, graph: Dict):
        """Prepares the current step for execution.
        Gets/sets/cleans up appropriate items in preparation for exection.

        Args:
            graph (Dict): Chemputer Graph to check
        """

        # Obtain the vessel type if not defined
        if not self.vessel_type:
            self.vessel_type = get_vessel_type(graph, self.vessel)

        # Obtian the heater and chiller
        self.heater, self.chiller = get_heater_chiller(graph, self.vessel)

    def get_steps(self) -> List[Step]:
        """Get the list of steps/base steps to execute.

        Returns:
            List[Step]: Steps to execute.
        """

        steps = []

        # Vessel type is defined
        if self.vessel_type:
            # Vessel is a rotavap
            if self.vessel_type == 'rotavap':
                steps.append(
                    CRotavapSetTemp(rotavap_name=self.vessel, temp=self.temp),
                )

            # Vessel is other type
            else:
                # Add chiller step if present
                if self.chiller:
                    steps.append(
                        CChillerSetTemp(vessel=self.vessel, temp=self.temp),
                    )

                # Add heater step if present
                if self.heater:
                    steps.append(
                        CStirrerSetTemp(vessel=self.vessel, temp=self.temp),
                    )

        return steps

    def sanity_checks(self, graph: Dict) -> List[SanityCheck]:
        """Gets a list of Sanity checks to perform for the step

        Args:
            graph (Dict): Chemputer graph to check

        Returns:
            List[SanityCheck]: List of checks to perform
        """

        return [
            SanityCheck(
                condition=self.steps
            )
        ] + heater_chiller_sanity_checks(self.heater, self.chiller, self.temp)

    @property
    def requirements(self) -> Dict[str, Dict[str, Any]]:
        """Gets the requirements needed for this step.

        Returns:
            Dict[str, Dict[str, Any]]: Requirements for the step.
        """

        return {
            'vessel': {
                'heatchill': True,
                'temp': [self.temp]
            }
        }

class HeatChillToTemp(ChemputerStep, AbstractStep):
    """Heat/Chill vessel to given temp.

    Args:
        vessel (str): Vessel to heat/chill.
        temp (float): Temperature to heat/chill to in degrees C.
        active (bool): If True, will actively heat/chill to the desired temp and
            leave heater/chiller on. If False, stop heating/chilling and wait
            for the temp to be reached.
        continue_heatchill (bool): If True, heating/chilling will be left on
            at end of step, even if active is False.
        stir (bool): If True, step will be stirred, otherwise False.
        stir_speed (float): Speed to stir at, only used if stir == True.
        vessel_type (str): Given internally. Used to know whether to use
            heater or chiller base steps. 'filter', 'rotavap' or 'reactor'
    """

    DEFAULT_PROPS = {
        'active': True,
        'continue_heatchill': True,
        'stir': True,
        'stir_speed': '250 RPM',
        'wait_recording_speed': 2000,
        'after_recording_speed': 14,
    }

    PROP_TYPES = {
        'vessel': VESSEL_PROP_TYPE,
        'temp': float,
        'active': bool,
        'continue_heatchill': bool,
        'stir': bool,
        'stir_speed': float,
        'vessel_type': str,
        'wait_recording_speed': float,
        'after_recording_speed': float,
        'heater': str,
        'chiller': str
    }

    INTERNAL_PROPS = [
        'vessel_type',
        'heater',
        'chiller'
    ]

    PROP_LIMITS = {
        'temp': TEMP_PROP_LIMIT,
        'stir_speed': ROTATION_SPEED_PROP_LIMIT,
        'vessel_type': VESSEL_TYPE_PROP_LIMIT,
    }

    ALWAYS_WRITE = [
        'stir',
    ]

    def __init__(
        self,
        vessel: str,
        temp: float,
        active: bool = 'default',
        continue_heatchill: bool = 'default',
        stir: Optional[bool] = 'default',
        stir_speed: Optional[float] = 'default',
        wait_recording_speed: Optional[float] = 'default',
        after_recording_speed: Optional[float] = 'default',

        # Internal props
        vessel_type: Optional[str] = None,
        heater: Optional[str] = None,
        chiller: Optional[str] = None,
        **kwargs
    ) -> None:
        super().__init__(locals())
        assert temp is not None

    def on_prepare_for_execution(self, graph: Dict):
        """Prepares the current step for execution.
        Gets/sets/cleans up appropriate items in preparation for exection.

        Args:
            graph (Dict): Chemputer Graph to check
        """

        # Obtian the vessel type if not defined
        if not self.vessel_type:
            self.vessel_type = get_vessel_type(graph, self.vessel)

        # Obtain the heater and chiller
        self.heater, self.chiller = get_heater_chiller(graph, self.vessel)

    def get_steps(self) -> List[Step]:
        """Get the list of steps/base steps to execute.

        Returns:
            List[Step]: Steps to execute.
        """

        steps = []

        # Vessel type is defined
        if self.vessel_type:
            # Get intial steps
            steps = self.get_initial_heatchill_steps()

            # Get rotavap specific steps
            if self.vessel_type == 'rotavap':
                steps += [
                    Wait(time=DEFAULT_ROTAVAP_WAIT_FOR_TEMP_TIME),
                ]

            # Vessel is not a rotavap
            else:
                # Get chiller steps if present
                if self.chiller:
                    if CHILLER_MIN_TEMP <= self.temp <= CHILLER_MAX_TEMP:
                        steps += self.get_chiller_steps()

                    elif self.heater and 18 <= self.temp <= HEATER_MAX_TEMP:
                        steps += self.get_heater_steps()

                # Get heater steps if present
                elif self.heater and 18 <= self.temp <= HEATER_MAX_TEMP:
                    steps += self.get_heater_steps()

            # ASdd final steps
            steps += self.get_final_heatchill_steps()

        # Should be stirring, add StartStir step
        if self.stir:
            steps.insert(
                0,
                StartStir(
                    vessel=self.vessel,
                    vessel_type=self.vessel_type,
                    stir_speed=self.stir_speed
                )
            )

        # Shouldn't be stirring, add StopStir step
        else:
            steps.insert(
                0, StopStir(vessel=self.vessel, vessel_type=self.vessel_type)
            )

        return steps

    def sanity_checks(self, graph: Dict) -> List[SanityCheck]:
        """Gets a list of Sanity checks to perform for the step

        Args:
            graph (Dict): Chemputer graph to check

        Returns:
            List[SanityCheck]: List of checks to perform
        """

        return heater_chiller_sanity_checks(
            self.heater, self.chiller, self.temp
        )

    def get_chiller_steps(self) -> List[Step]:
        """Get chiller recording steps

        Returns:
            List[Step]: Chiller recording steps
        """

        return [
            CSetRecordingSpeed(self.wait_recording_speed),
            CChillerWaitForTemp(vessel=self.vessel),
            CSetRecordingSpeed(self.after_recording_speed),
        ]

    def get_heater_steps(self) -> List[Step]:
        """Get heater recording steps

        Returns:
            List[Steps]: Heater recording steps
        """

        return [
            CSetRecordingSpeed(self.wait_recording_speed),
            CStirrerWaitForTemp(vessel=self.vessel),
            CSetRecordingSpeed(self.after_recording_speed),
        ]

    def get_initial_heatchill_steps(self) -> List[Step]:
        """Get the initial steps for heatchill

        Returns:
            List[Step]: HeatChill steps
        """

        # Actively running, start heating/chilling
        if self.active:
            return [StartHeatChill(vessel=self.vessel, temp=self.temp)]

        # Not active, stop heating/chilling
        else:
            return [
                HeatChillSetTemp(vessel=self.vessel, temp=self.temp),
                StopHeatChill(vessel=self.vessel)
            ]

    def get_final_heatchill_steps(self) -> Optional[List[Step]]:
        """Get the final steps for heatchill

        Returns:
            Optional[List[Step]]: HeatChill steps, none if not needed
        """

        # Inactive heatchilling, need to switch on at end
        if self.continue_heatchill and not self.active:
            return [StartHeatChill(vessel=self.vessel, temp=self.temp)]

        # Active heatchilling, need to switch off at end
        elif not self.continue_heatchill and self.active:
            return [StopHeatChill(vessel=self.vessel)]

        # Inactive leaving off, or active leaving on.
        else:
            return []

    def human_readable(self, language: str = 'en') -> str:
        """Get the human-readable text for this step

        Args:
            language (str, optional): Localisation language. Defaults to 'en'.

        Raises:
            KeyError: Localisation not supported

        Returns:
            str: Human-readable text for the step
        """

        # English uses new conditional template human readable format
        if language == 'en':
            return super().human_readable(language=language)

        # Non english uses old basic template human readable format
        try:
            if self.stir:
                return HUMAN_READABLE_STEPS[
                    'HeatChillToTemp (stirring)'][language].format(
                        **self.formatted_properties())
            else:
                return HUMAN_READABLE_STEPS[
                    'HeatChillToTemp (not stirring)'][language].format(
                        **self.formatted_properties())
        except KeyError:
            return self.name

    @property
    def requirements(self) -> Dict[str, Dict[str, Any]]:
        """Gets the requirements needed for this step.

        Returns:
            Dict[str, Dict[str, Any]]: Requirements for the step.
        """

        return {
            'vessel': {
                'heatchill': True,
                'temp': [self.temp]
            }
        }

class StopHeatChill(ChemputerStep, AbstractStep):
    """Stop heater/chiller on given vessel..

    Args:
        vessel (str): Name of vessel attached to heater/chiller..
        vessel_type (str): Given internally. Used to know whether to use
            heater or chiller base steps. 'ChemputerFilter' or
            'ChemputerReactor'.
    """

    PROP_TYPES = {
        'vessel': VESSEL_PROP_TYPE,
        'vessel_type': str,
        'heater': str,
        'chiller': str
    }

    INTERNAL_PROPS = [
        'vessel_type',
        'heater',
        'chiller'
    ]

    PROP_LIMITS = {
        'vessel_type': VESSEL_TYPE_PROP_LIMIT,
    }

    def __init__(
        self,
        vessel: str,

        # Internal properties
        vessel_type: Optional[str] = None,
        heater: str = None,
        chiller: str = None,
        **kwargs
    ) -> None:
        super().__init__(locals())

    def on_prepare_for_execution(self, graph: Dict):
        """Prepares the current step for execution.
        Gets/sets/cleans up appropriate items in preparation for exection.

        Args:
            graph (Dict): Chemputer Graph to check
        """

        # Obtain vessel type if not defined
        if not self.vessel_type:
            self.vessel_type = get_vessel_type(graph, self.vessel)

        # Obtain the heater and chiller
        self.heater, self.chiller = get_heater_chiller(graph, self.vessel)

    def get_steps(self) -> List[Step]:
        """Get the list of steps/base steps to execute.

        Returns:
            List[Step]: Steps to execute.
        """

        steps = []

        # Vessel type is defined
        if self.vessel_type:
            # Get rotavap steps if vessel is rotavap
            if self.vessel_type == 'rotavap':
                steps.append(CRotavapStopHeater(self.vessel))

            # Vessel not a rotavap, get chiller and heater steps
            else:
                if self.chiller:
                    steps.append(CStopChiller(self.vessel))

                if self.heater:
                    steps.append(CStopHeat(self.vessel))

        return steps

    @property
    def requirements(self) -> Dict[str, Dict[str, Any]]:
        """Gets the requirements needed for this step.

        Returns:
            Dict[str, Dict[str, Any]]: Requirements for the step.
        """

        return {
            'vessel': {
                'heatchill': True,
            }
        }

class HeatChillReturnToRT(ChemputerStep, AbstractStep):
    """Let heater/chiller return to room temperatre and then stop
    heating/chilling.

    Args:
        vessel (str): Vessel to attached to heater/chiller to return to room
            temperature.
        stir (bool): If True, step will be stirred, otherwise False.
        stir_speed (float): Speed to stir at, only used if stir == True.
        vessel_type (str): Given internally. Used to know whether to use
            heater or chiller base steps. 'ChemputerFilter' or
            'ChemputerReactor'.
    """

    DEFAULT_PROPS = {
        'stir': True,
        'stir_speed': '250 RPM',
        'wait_recording_speed': 2000,
        'after_recording_speed': 14,
    }

    INTERNAL_PROPS = [
        'vessel_type',
    ]

    PROP_TYPES = {
        'vessel': VESSEL_PROP_TYPE,
        'stir': bool,
        'stir_speed': float,
        'wait_recording_speed': float,
        'after_recording_speed': float,
        'vessel_type': str
    }

    PROP_LIMITS = {
        'stir_speed': ROTATION_SPEED_PROP_LIMIT,
    }

    def __init__(
        self,
        vessel: str,
        stir: Optional[bool] = 'default',
        stir_speed: Optional[float] = 'default',
        wait_recording_speed: Optional[float] = 'default',
        after_recording_speed: Optional[float] = 'default',

        # Internal properties
        vessel_type: Optional[str] = None,
        **kwargs
    ) -> None:
        super().__init__(locals())

    def on_prepare_for_execution(self, graph: Dict):
        """Prepares the current step for execution.
        Gets/sets/cleans up appropriate items in preparation for exection.

        Args:
            graph (Dict): Chemputer Graph to check
        """

        # Obtain the vessel type if not defined
        if not self.vessel_type:
            self.vessel_type = get_vessel_type(graph, self.vessel)

    def get_steps(self) -> List[Step]:
        """Get the list of steps/base steps to execute.

        Returns:
            List[Step]: Steps to execute.
        """

        steps = []

        # Get chiller steps if vessel is a filter
        if self.vessel_type == 'filter':
            steps = [ChillerReturnToRT(vessel=self.vessel)]

        # Get heater steps if vessel is a reactor
        elif self.vessel_type == 'reactor':
            steps = [StirrerReturnToRT(vessel=self.vessel)]

        # Get rotavap steps if vessel is a rotavap
        elif self.vessel_type == 'rotavap':
            steps = [
                CRotavapStopHeater(rotavap_name=self.vessel),
                Wait(time=DEFAULT_ROTAVAP_WAIT_FOR_TEMP_TIME),
            ]

        # Should be stirring, add StartStir step to beginning
        if self.stir:
            steps.insert(
                0,
                StartStir(
                    vessel=self.vessel,
                    vessel_type=self.vessel_type,
                    stir_speed=self.stir_speed
                )
            )

        # Shouldn't be stirring, add in StopStir step at beginning
        else:
            steps.insert(
                0, StopStir(vessel=self.vessel, vessel_type=self.vessel_type)
            )

        return steps

    @property
    def requirements(self) -> Dict[str, Dict[str, Any]]:
        """Gets the requirements needed for this step.

        Returns:
            Dict[str, Dict[str, Any]]: Requirements for the step.
        """

        return {
            'vessel': {
                'heatchill': True,
            }
        }

class StirrerReturnToRT(ChemputerStep, AbstractStep):

    DEFAULT_PROPS = {
        'wait_recording_speed': 2000,
        'after_recording_speed': 14,
    }

    PROP_TYPES = {
        'vessel': VESSEL_PROP_TYPE,
        'wait_recording_speed': float,
        'after_recording_speed': float
    }

    def __init__(
        self,
        vessel: str,
        wait_recording_speed: Optional[float] = 'default',
        after_recording_speed: Optional[float] = 'default',
    ):
        super().__init__(locals())

    def get_steps(self) -> List[Step]:
        """Get the list of steps/base steps to execute.

        Returns:
            List[Step]: Steps to execute.
        """

        return [
            CStirrerSetTemp(vessel=self.vessel, temp=ROOM_TEMPERATURE),
            CStopHeat(vessel=self.vessel),
            CSetRecordingSpeed(self.wait_recording_speed),
            CStirrerWaitForTemp(vessel=self.vessel),
            CSetRecordingSpeed(self.after_recording_speed),
        ]

class ChillerReturnToRT(ChemputerStep, AbstractStep):

    DEFAULT_PROPS = {
        'wait_recording_speed': 2000,
        'after_recording_speed': 14,
    }

    INTERNAL_PROPS = [
        'vessel_class'
    ]

    PROP_TYPES = {
        'vessel': VESSEL_PROP_TYPE,
        'wait_recording_speed': float,
        'after_recording_speed': float,
        'vessel_class': str
    }

    PROP_LIMITS = {
        'vessel_class': VESSEL_CLASS_PROP_LIMIT,
    }

    def __init__(
        self,
        vessel: str,
        wait_recording_speed: Optional[float] = 'default',
        after_recording_speed: Optional[float] = 'default',

        # Internal properties
        vessel_class: str = None,
    ):
        super().__init__(locals())

    def on_prepare_for_execution(self, graph: Dict):
        """Prepares the current step for execution.
        Gets/sets/cleans up appropriate items in preparation for exection.

        Args:
            graph (Dict): Chemputer Graph to check
        """

        self.vessel_class = graph.nodes[self.vessel]['class']

    def get_steps(self) -> Optional[List[Step]]:
        """Get the list of steps/base steps to execute.

        Returns:
            Optional[List[Step]]: Steps to execute. None if chiller not
                                    supported.
        """

        # Julabo chiller
        if self.vessel_class == 'JULABOCF41':
            return [
                CChillerSetTemp(vessel=self.vessel, temp=ROOM_TEMPERATURE),
                CSetCoolingPower(vessel=self.vessel, cooling_power=0),
                CStartChiller(vessel=self.vessel),
                CSetRecordingSpeed(self.wait_recording_speed),
                CChillerWaitForTemp(vessel=self.vessel),
                CSetRecordingSpeed(self.after_recording_speed),
                CSetCoolingPower(vessel=self.vessel, cooling_power=100),
                CStopChiller(self.vessel)
            ]

        # Huber chiller
        elif self.vessel_class == 'HuberPetiteFleur':
            return [
                CRampChiller(
                    vessel=self.vessel,
                    ramp_duration='1 hr',
                    end_temperature=ROOM_TEMPERATURE
                )
            ]

        # No other chiller's supported
        else:
            return []
