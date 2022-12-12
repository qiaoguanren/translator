"""
.. module:: steps_synthesis.wash_solid
    :platforms: Unix, Windows
    :synopsis: XDL step for washing a solid with a given volume of
                of a given solvent

"""

from typing import Optional, Union, Dict, Any

# XDL
from xdl.steps.base_steps import AbstractStep
from xdl.steps.special_steps import Repeat
from xdl.utils.prop_limits import (
    VOLUME_PROP_LIMIT,
    TEMP_PROP_LIMIT,
    TIME_PROP_LIMIT,
    ROTATION_SPEED_PROP_LIMIT,
    WASH_SOLID_STIR_PROP_LIMIT,
)
from xdl.utils.misc import SanityCheck
from xdl.constants import REAGENT_PROP_TYPE, VESSEL_PROP_TYPE

# Relative
from .add import Add
from ..base_step import ChemputerStep
from ..steps_utility import (
    Wait,
    StartStir,
    StopStir,
    HeatChillToTemp,
    StopHeatChill,
    ApplyVacuum
)
from ..steps_base import CMove
from ...constants import (
    BOTTOM_PORT,
    TOP_PORT,
    DEFAULT_FILTER_EXCESS_REMOVE_FACTOR,
    DEFAULT_FILTER_ANTICLOGGING_ASPIRATION_SPEED,
    CHEMPUTER_WASTE,
)
# from ...utils.execution import (
#     get_nearest_node, get_vacuum_configuration, get_vessel_type)
from ...utils.prop_limits import (
    VALVE_PORT_PROP_LIMIT, VESSEL_TYPE_PROP_LIMIT
)

class WashSolid(ChemputerStep, AbstractStep):
    """Wash filter cake with given volume of given solvent.

    Args:
        vessel (str): Vessel containing contents to wash.
        solvent (str): Solvent to wash with.
        volume (float): Volume of solvent to wash with.
        temp (float): Optional. Temperature to perform wash at.
        vacuum_time (float): Time to wait after vacuum connected.
        stir (Union[float, str]): True, 'solvent' or False. True means stir from
            the start until the solvent has been removed. 'solvent' means stir
            after the solvent has been added and stop before it is removed.
            False means don't stir.
        stir_time (float): Time to stir for after solvent has been added. Only
            relevant if stir is True or 'solvent'.
        stir_speed (float): Speed to stir at in RPM. Only relevant if stir is
            True or 'solvent'.
        waste_vessel (str): Given internally. Vessel to send waste to.
        filtrate_vessel (str): Optional. Vessel to send filtrate to. Defaults to
            waste_vessel.
        aspiration_speed (float): Speed to remove solvent from filter_vessel.
        vacuum (str): Given internally. Name of vacuum flask.
        vacuum_device (str): Given internally. Name of vacuum device attached to
            vacuum flask. Can be None if vacuum is just from fumehood vacuum
            line.
        inert_gas (str): Given internally. Name of node supplying inert gas.
            Only used if inert gas filter dead volume method is being used.
        vacuum_valve (str): Given internally. Name of valve connecting filter
            bottom to vacuum.
        valve_unused_port (str): Given internally. Random unused position on
            valve.
        vessel_type (str): Given internally. 'reactor', 'filter', 'rotavap',
            'flask' or 'separator'.
        filter_dead_volume (float): Given internally. Dead volume of filter if
            vessel_type == 'filter' otherwise None.
        repeat (int): How many washes to do.
    """

    DEFAULT_FILTER_VACUUM_PRESSURE = 400  # mbar
    DEFAULT_NON_FILTER_VACUUM_PRESSURE = 10  # mbar

    DEFAULT_PROPS = {
        'volume': '20 mL',
        'vacuum_time': '10 seconds',
        'stir': True,
        'stir_time': '30 seconds',
        'stir_speed': '500 RPM',
        'aspiration_speed': 5,  # mL / min
        'anticlogging': False,
        'temp': None,
        'filtrate_vessel': None,
        'repeat': 1,
    }

    PROP_TYPES = {
        'vessel': VESSEL_PROP_TYPE,
        'solvent': REAGENT_PROP_TYPE,
        'volume': float,
        'temp': float,
        'vacuum_time': float,
        'stir': Union[bool, str],
        'stir_time': float,
        'stir_speed': float,
        'aspiration_speed': float,
        'filtrate_vessel': str,
        'anticlogging': bool,
        'waste_vessel': str,
        'vacuum': str,
        'vacuum_device': str,
        'inert_gas': str,
        'vacuum_valve': str,
        'valve_unused_port': int,
        'vessel_type': str,
        'filter_dead_volume': float,
        'repeat': int,
    }

    INTERNAL_PROPS = [
        'waste_vessel',
        'vacuum',
        'vacuum_device',
        'inert_gas',
        'vacuum_valve',
        'valve_unused_port',
        'vessel_type',
        'filter_dead_volume',
    ]

    ALWAYS_WRITE = [
        'volume',
    ]

    PROP_LIMITS = {
        'volume': VOLUME_PROP_LIMIT,
        'temp': TEMP_PROP_LIMIT,
        'vacuum_time': TIME_PROP_LIMIT,
        'stir': WASH_SOLID_STIR_PROP_LIMIT,
        'stir_time': TIME_PROP_LIMIT,
        'stir_speed': ROTATION_SPEED_PROP_LIMIT,
        'vessel_type': VESSEL_TYPE_PROP_LIMIT,
        'valve_unused_port': VALVE_PORT_PROP_LIMIT,
        'filter_dead_volume': VOLUME_PROP_LIMIT,
    }

    def __init__(
        self,
        vessel: str,
        solvent: str,
        volume: Optional[float] = 'default',
        temp: Optional[float] = None,
        vacuum_time: Optional[float] = 'default',
        stir: Optional[Union[bool, str]] = 'default',
        stir_time: Optional[float] = 'default',
        stir_speed: Optional[float] = 'default',
        aspiration_speed: Optional[float] = 'default',
        filtrate_vessel: Optional[str] = None,
        anticlogging: Optional[bool] = 'default',
        repeat: Optional[int] = 'default',

        # Internal properties
        waste_vessel: Optional[str] = None,
        vacuum: Optional[str] = None,
        vacuum_device: Optional[str] = None,
        inert_gas: Optional[str] = None,
        vacuum_valve: Optional[str] = None,
        valve_unused_port: Optional[Union[str, int]] = None,
        vessel_type: Optional[str] = None,
        filter_dead_volume: Optional[float] = None,
        **kwargs
    ) -> None:
        super().__init__(locals())

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

        # Obtain the vessel type if not defined
        if not self.vessel_type:
            self.vessel_type = get_vessel_type(graph, self.vessel)

        # Obtain the filter dead volume if not defined
        if not self.filter_dead_volume:
            # Get vessel info
            vessel = graph.nodes[self.vessel]

            # Set dead volume if present
            if 'dead_volume' in vessel:
                self.filter_dead_volume = vessel['dead_volume']

        # Obtian the vacuum information
        vacuum_info = get_vacuum_configuration(graph, self.vessel)

        # Obtain the vacuum if not defined from the vacuum info
        if not self.vacuum:
            self.vacuum = vacuum_info['source']

        # Obtian the inert gas if not defined from the vacuum info
        if not self.inert_gas:
            self.inert_gas = vacuum_info['valve_inert_gas']

        # Obtain the vacuum valve if not defined from the vacuum info
        if not self.vacuum_valve:
            self.vacuum_valve = vacuum_info['valve']

        # Obtain the vacuum valve unused port if not defined from
        # the vacuum info
        if not self.valve_unused_port:
            self.valve_unused_port = vacuum_info['valve_unused_port']

        # Obtain the vacuum device if not defined from the vacuum info
        if not self.vacuum_device:
            self.vacuum_device = vacuum_info['device']

    def get_steps(self):
        steps = (
            # self.temp is not None, start heating/chilling
            self.get_initial_heatchill_steps()
            # self.stir is True, start stirring here
            + self.get_initial_start_stir_steps()
            # Add solvent
            + self.get_add_solvent_steps()
            # self.stir == 'solvent', start stirring here
            + self.get_after_solvent_stir_steps()
            # Wait while stirring happens (or not if self.stir is False)
            + self.get_stir_wait_steps()
            # self.stir == 'solvent', stop stirring here
            + self.get_stop_stir_before_solvent_removal_steps()
            # Remove solvent
            + self.get_remove_solvent_steps()
            # self.stir == True, stop stirring here
            + self.get_stop_stir_after_solvent_removal_steps()
            # Apply vacuum for self.vacuum_time
            + self.get_apply_vacuum_steps()
            # self.temp is not None, stop heating/chilling
            + self.get_stop_heatchill_steps()
        )
        if self.repeat > 1:
            return [Repeat(children=steps, repeats=self.repeat)]

        return steps

    def get_add_solvent_steps(self):
        """Add solvent to filter cake"""

        # Always add to top port of filter, otherwise default port for reactor
        # and rotavap
        port = TOP_PORT if self.vessel_type == 'filter' else None

        return [Add(
            reagent=self.solvent,
            volume=self.volume,
            vessel=self.vessel,
            port=port,
            stir=self.stir is True,
            stir_speed=self.stir_speed
        )]

    def get_initial_heatchill_steps(self):
        """self.temp is not None, start heating/chilling at beginning"""
        if self.temp is not None:
            return [HeatChillToTemp(vessel=self.vessel, temp=self.temp)]
        return []

    def get_initial_start_stir_steps(self):
        """self.stir is True, start stirring at beginning"""
        if self.stir is True:
            return [StartStir(
                vessel=self.vessel,
                stir_speed=self.stir_speed
            )]
        return []

    def get_after_solvent_stir_steps(self):
        """self.stir == 'solvent', start stirring after solvent addition"""
        if self.stir == 'solvent':
            return [
                StartStir(
                    vessel=self.vessel,
                    stir_speed=self.stir_speed
                )
            ]
        return []

    def get_stir_wait_steps(self):
        """Stir filter cake and solvent briefly"""
        return [Wait(self.stir_time)]

    def get_remove_solvent_steps(self):
        """Remove solvent from vessel."""
        port = BOTTOM_PORT if self.vessel_type == 'filter' else None
        return [CMove(
            from_vessel=self.vessel,
            from_port=port,
            to_vessel=self.get_filtrate_vessel(),
            volume=self.get_withdraw_volume(),
            aspiration_speed=self.get_aspiration_speed()
        )]

    def get_stop_stir_before_solvent_removal_steps(self):
        """self.stir == 'solvent', stop stirring before removing solvent."""
        if self.stir == 'solvent':
            return [StopStir(vessel=self.vessel)]
        return []

    def get_stop_stir_after_solvent_removal_steps(self):
        """self.stir is True, stop stirring after removing solvent but
        before applying vacuum.
        """
        if self.stir is True:
            return [StopStir(vessel=self.vessel)]
        return []

    def get_apply_vacuum_steps(self):
        """Apply vacuum briefly after removing solvent."""

        # Port is bottom port if vessel is a filter, else None
        port = BOTTOM_PORT if self.vessel_type == 'filter' else None

        # Return ApplyVacuum step.
        return [
            ApplyVacuum(
                vessel=self.vessel,
                time=self.vacuum_time,
                port=port,
                pressure=self.get_vacuum_pressure()
            )
        ]

    def get_stop_heatchill_steps(self):
        """self.temp is not None, stop heating/chilling at end."""
        if self.temp is not None:
            return [StopHeatChill(vessel=self.vessel)]
        return []

    def get_vacuum_pressure(self) -> float:
        """Gets the pressure of the vacuum pump

        Returns:
            float: Vacuum pressure
        """
        # Get the vacuum pressure used for a filter vessel
        if self.vessel_type == 'filter':
            return self.DEFAULT_FILTER_VACUUM_PRESSURE

        # Return the default vacuum pressure
        else:
            return self.DEFAULT_NON_FILTER_VACUUM_PRESSURE

    def get_withdraw_volume(self):
        """Get volume to withdraw when removing solvent."""
        # Volume to withdraw after solvent is added.
        withdraw_volume = self.volume * DEFAULT_FILTER_EXCESS_REMOVE_FACTOR

        # If filter dead volume given internally, add it to withdraw volume.
        # This is because not only the solvent added, but also the dead volume
        # of the filter flask (volume below the frit) needs to be withdrawn.
        if self.filter_dead_volume:
            withdraw_volume += self.filter_dead_volume

        return withdraw_volume

    def get_aspiration_speed(self):
        """Get aspiration speed to use based on anticlogging property."""
        return (
            self.aspiration_speed if not self.anticlogging
            else DEFAULT_FILTER_ANTICLOGGING_ASPIRATION_SPEED
        )

    def get_filtrate_vessel(self):
        """Get vessel to send filtrate to."""
        return (
            self.filtrate_vessel if self.filtrate_vessel
            else self.waste_vessel
        )

    def sanity_checks(self, graph):
        return [
            SanityCheck(
                condition=self.vessel,
                error_msg=f'{self.vessel} cannot be None.'
            ),
        ]

    @property
    def requirements(self) -> Dict[str, Dict[str, Any]]:
        """Gets the requirements needed for this step.

        Returns:
            Dict[str, Dict[str, Any]]: Requirements for the step.
        """

        return {
            'vessel': {
                'stir': self.stir is not False,
                'temp': [] if self.temp is None else [self.temp]
            }
        }

    def scale(self, scale: float):
        """Scales the volume by a scale factor

        Args:
            scale (float): Scale factor
        """
        self.volume *= scale
