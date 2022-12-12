"""
.. module:: steps_synthesis.dry
    :platforms: Unix, Windows
    :synopsis: XDL step for srying a vessel by applying vacuum for a given time

"""

from typing import Optional, List, Dict, Any, Union

# XDL
from xdl.steps.base_steps import Step, AbstractStep
from xdl.utils.prop_limits import (
    TIME_PROP_LIMIT,
    TEMP_PROP_LIMIT,
    PRESSURE_PROP_LIMIT
)
from xdl.constants import ROOM_TEMPERATURE, VESSEL_PROP_TYPE

# Relative
from ..base_step import ChemputerStep
from ..steps_utility.vacuum import ApplyVacuum
from ..steps_utility import (
    StopStir,
    HeatChillToTemp,
    RotavapStartRotation,
    RotavapStopRotation,
)
from ..steps_base import CMove, CRotavapLiftDown, CRotavapLiftUp
from ...constants import (
    BOTTOM_PORT,
    DEFAULT_DRY_WASTE_VOLUME,
    CHEMPUTER_WASTE,
)
# from ...utils.execution import (
#     get_nearest_node,
#     get_vacuum_configuration,
#     get_vessel_stirrer,
#     get_vessel_type,
# )
from ...utils.prop_limits import VALVE_PORT_PROP_LIMIT, VESSEL_TYPE_PROP_LIMIT

class Dry(ChemputerStep, AbstractStep):
    """Dry given vessel by applying vacuum for given time.

    Args:
        vessel (str): Vessel name to dry.
        time (float): Time to dry vessel for in seconds. (optional)
        temp (float): Temperature to dry at.
        waste_vessel (str): Given internally. Vessel to send waste to.
        vacuum (str): Given internally. Name of vacuum flask.
        vacuum_device (str): Name of actual vacuum device attached to vacuum
            flask. If there is no device (i.e. vacuum line in fumehood) will be
            None.
        vacuum_pressure (float): Pressure in mbar of vacuum. Only applied if
            vacuum_device isn't None.
        inert_gas (str): Given internally. Name of node supplying inert gas.
            Only used if inert gas filter dead volume method is being used.
        vacuum_valve (str): Given internally. Name of valve connecting filter
            bottom to vacuum.
        valve_unused_port (str): Given internally. Random unused position on
            valve.
        vessel_type (str): Given internally. 'reactor', 'filter', 'rotavap',
            'flask' or 'separator'.
        vessel_has_stirrer (bool): Given internally. True if vessel is connected
            to a stirrer.
    """

    DEFAULT_FILTER_VACUUM_PRESSURE = 400  # mbar
    DEFAULT_NON_FILTER_VACUUM_PRESSURE = 10  # mbar

    DEFAULT_PROPS = {
        'time': '1 hr',
        'aspiration_speed': 5,  # mL / min
        'continue_heatchill': False,
        'temp': None,
        'waste_vessel': None,
        'vacuum_pressure': None,
    }

    PROP_TYPES = {
        'vessel': VESSEL_PROP_TYPE,
        'time': float,
        'temp': float,
        'waste_vessel': str,
        'aspiration_speed': float,
        'continue_heatchill': bool,
        'vacuum': str,
        'vacuum_device': str,
        'vacuum_pressure': float,
        'inert_gas': str,
        'vacuum_valve': str,
        'valve_unused_port': int,
        'vessel_type': str,
        'vessel_has_stirrer': bool,
    }

    INTERNAL_PROPS = [
        'vacuum',
        'vacuum_device',
        'inert_gas',
        'vacuum_valve',
        'valve_unused_port',
        'vessel_type',
        'vessel_has_stirrer',
    ]

    PROP_LIMITS = {
        'time': TIME_PROP_LIMIT,
        'temp': TEMP_PROP_LIMIT,
        'vacuum_pressure': PRESSURE_PROP_LIMIT,
        'valve_unused_port': VALVE_PORT_PROP_LIMIT,
        'vessel_type': VESSEL_TYPE_PROP_LIMIT,
    }

    def __init__(
        self,
        vessel: str,
        time: Optional[float] = 'default',
        temp: Optional[float] = 'default',
        waste_vessel: Optional[str] = 'default',
        aspiration_speed: Optional[float] = 'default',
        continue_heatchill: Optional[bool] = 'default',
        vacuum_pressure: Optional[float] = 'default',

        # Internal properties
        vacuum: Optional[str] = None,
        vacuum_device: Optional[str] = False,
        inert_gas: Optional[str] = None,
        vacuum_valve: Optional[str] = None,
        valve_unused_port: Optional[Union[str, int]] = None,
        vessel_type: Optional[str] = None,
        vessel_has_stirrer: Optional[bool] = True,
        **kwargs
    ) -> None:
        super().__init__(locals())

    def sanity_checks(self, graph: Dict) -> List[Optional[Any]]:
        """Gets a list of Sanity checks to perform for the step

        Args:
            graph (Dict): Chemputer graph to check

        Returns:
            List[Optional[Any]]: List of checks to perform
        """

        return []

    def on_prepare_for_execution(self, graph: Dict):
        """Prepares the current step for execution.
        Gets/sets/cleans up appropriate items in preparation for exection.

        Args:
            graph (Dict): Chemputer Graph to check
        """

        # Obtain waste vessel if not defined
        if not self.waste_vessel:
            self.waste_vessel = get_nearest_node(
                graph, self.vessel, CHEMPUTER_WASTE
            )

        # Obtain vessel type if not defined
        if not self.vessel_type:
            self.vessel_type = get_vessel_type(graph, self.vessel)

        # Determine if the vessel has a stirrer attached
        if get_vessel_stirrer(graph, self.vessel):
            self.vessel_has_stirrer = True
        else:
            self.vessel_has_stirrer = False

        # Obtain vacuum configuration
        vacuum_info = get_vacuum_configuration(graph, self.vessel)

        # Obtain vacuum if not defnied
        if not self.vacuum:
            self.vacuum = vacuum_info['source']

        # Obtain inert gas if not defined
        if not self.inert_gas:
            self.inert_gas = vacuum_info['valve_inert_gas']

        # Obtain the valve attached to the vacuum if not defined
        if not self.vacuum_valve:
            self.vacuum_valve = vacuum_info['valve']

        # Obtain the vacuum valve's unused port if not defined
        if not self.valve_unused_port:
            self.valve_unused_port = vacuum_info['valve_unused_port']

        # Obtain the vacuum device if not defined
        if not self.vacuum_device:
            self.vacuum_device = vacuum_info['device']

    def get_steps(self) -> List[Step]:
        """Get the list of steps/base steps to execute.

        Returns:
            List[Step]: Steps to execute.
        """

        return (
            self.get_start_heatchill_steps()
            + self.get_stop_stir_steps()
            + self.get_rotavap_initialise_steps()
            + self.get_move_steps()
            + self.get_apply_vacuum_steps()
            + self.get_end_heatchill_steps()
            + self.get_rotavap_finish_steps()
        )

    def get_start_heatchill_steps(self) -> List[Optional[Step]]:
        """Get HeatChill steps required

        Returns:
            List[Optional[Step]]: HeatChill steps if needed, else []
        """

        # Get HeatChill step if a temperature is defined, else []
        return ([
            HeatChillToTemp(
                vessel=self.vessel,
                temp=self.temp,
                stir=False
            )
        ] if self.temp is not None else [])

    def get_rotavap_initialise_steps(self) -> List[Optional[Step]]:
        """Get steps to initialise the rotavap if defined

        Returns:
            List[Optional[Step]]: Steps to start the rotavap, else []
        """

        # Vessel is a rotavap, return steps to start it up
        if self.vessel_type == 'rotavap':
            return [
                CRotavapLiftDown(self.vessel),
                RotavapStartRotation(self.vessel),
            ]

        # No rotavap required
        return []

    def get_rotavap_finish_steps(self) -> List[Optional[Step]]:
        """Get steps to finish using the rotavap if defined

        Returns:
            List[Optional[Step]]: Steps tostop the rotavap, else []
        """

        # Vessel is a rotavap, return steps to finish using it
        if self.vessel_type == 'rotavap':
            return [
                CRotavapLiftUp(self.vessel),
                RotavapStopRotation(self.vessel),
            ]

        # No rotavap required
        return []

    def get_stop_stir_steps(self) -> List[Optional[Step]]:
        """Get steps associated with stopping attached stirrers

        Returns:
            List[Optional[Step]]: StopStir steps if the vessel has a stirrer,
                                else []
        """

        # Return StopStir if the vessel has a stirrer attached, else []
        return (
            [StopStir(vessel=self.vessel)]
            if self.vessel_has_stirrer
            else []
        )

    def get_move_steps(self) -> List[Optional[Step]]:
        """Get steps associated with movement

        Returns:
            List[Optional[Step]]: Movement steps
        """

        # use bottom port if the vessel is a filter, else None
        from_port = BOTTOM_PORT if self.vessel_type == 'filter' else None

        # Add a movement step if the vessel is a filter, else []
        return ([
            CMove(
                from_vessel=self.vessel,
                from_port=from_port,
                to_vessel=self.waste_vessel,
                volume=DEFAULT_DRY_WASTE_VOLUME,
                aspiration_speed=self.aspiration_speed,
            )
        ] if self.vessel_type == 'filter' else [])

    def get_apply_vacuum_steps(self) -> List[Step]:
        """Get steps associated with applying a vacuum

        Returns:
            List[Step]: ApplyVacuum steps.
        """

        # Port is bottom port if vessel is a filter, else None
        port = BOTTOM_PORT if self.vessel_type == 'filter' else None

        # Return ApplyVacuum step.
        return [
            ApplyVacuum(
                vessel=self.vessel,
                time=self.time,
                port=port,
                pressure=self.get_vacuum_pressure()
            )
        ]

    def get_end_heatchill_steps(self) -> List[Optional[Step]]:
        """Get steps associated with heating and chilling a vessel.

        Returns:
            List[Optional[Step]]: HeatChill steps if temperature is defined
                            and not continuing on with heating/chilling, else []
        """

        # Return HeatChill if a temperature is defined and not continuing
        # with heating/chilling, else []

        return ([
            HeatChillToTemp(
                vessel=self.vessel,
                temp=ROOM_TEMPERATURE,
                continue_heatchill=False,
                stir=False
            )
        ] if self.temp and not self.continue_heatchill else [])

    def get_vacuum_pressure(self) -> float:
        """Gets the pressure of the vacuum pump

        Returns:
            float: Vacuum pressure
        """

        # Pressure is already defined, return it
        if self.vacuum_pressure is not None:
            return self.vacuum_pressure

        # Get the vacuum pressure used for a filter vessel
        elif self.vessel_type == 'filter':
            return self.DEFAULT_FILTER_VACUUM_PRESSURE

        # Return the default vacuum pressure
        else:
            return self.DEFAULT_NON_FILTER_VACUUM_PRESSURE

    @property
    def requirements(self) -> Dict[str, Dict[str, Any]]:
        """Get the requirements needed for this step

        Returns:
            Dict[str, Dict[str, Any]]: Step requirements
        """

        return {
            'vessel': {
                'temp': [item for item in [self.temp] if item is not None],
            }
        }
