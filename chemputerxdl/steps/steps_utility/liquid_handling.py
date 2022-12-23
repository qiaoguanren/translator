"""
.. module:: steps_utility.liquid_handling
    :platforms: Unix, Windows
    :synopsis: XDL steps to perform liquid handling operations

"""

from typing import Optional, List, Dict

# XDL
from xdl.steps.base_steps import AbstractStep, Step
from xdl.steps.special_steps import Repeat
from xdl.utils.prop_limits import (
    VOLUME_PROP_LIMIT,
    TIME_PROP_LIMIT,
    POSITIVE_INT_PROP_LIMIT,
)
from xdl.utils.misc import SanityCheck
from xdl.constants import VESSEL_PROP_TYPE, REAGENT_PROP_TYPE

# Relative
from .heatchill import StopHeatChill
from .stirring import StopStir
from ..base_step import ChemputerStep
from ..steps_base import CMove
from ...constants import (
    DEFAULT_PORTS,
    DEFAULT_VISCOUS_ASPIRATION_SPEED,
    DEFAULT_AIR_FLUSH_TUBE_VOLUME,
)
from ...localisation import HUMAN_READABLE_STEPS
# from ...utils.execution import (
#     get_reagent_vessel,
#     get_cartridge,
#     get_vessel_stirrer,
#     node_in_graph,
#     get_heater_chiller,
#     get_flush_tube_vessel,
#     get_waste_vessel,
# )
from ...utils.prop_limits import PORT_PROP_LIMIT
from ...constants import PORT_PROP_TYPE

class PrimePumpForAdd(ChemputerStep, AbstractStep):
    """Prime pump attached to given reagent flask in anticipation of Add step.

    Args:
        reagent (str): Reagent to prime pump for addition.
        volume (float): Volume to prime
        reagent_vessel (str): Reagent vessel to use
        waste_vessel (str): Waste vessel to use
    """

    DEFAULT_PROPS = {
        'volume': '3 mL',
        'prime_n_times': 1,
        'move_speed': 40,  # mL / min
        'aspiration_speed': 10,  # mL / min
        'dispense_speed': 40,  # mL / min
    }

    INTERNAL_PROPS = [
        'reagent_vessel',
        'waste_vessel',
    ]

    PROP_TYPES = {
        'reagent': REAGENT_PROP_TYPE,
        'volume': float,
        'reagent_vessel': str,
        'waste_vessel': str,
        'prime_n_times': int,
        'move_speed': float,
        'aspiration_speed': float,
        'dispense_speed': float,
    }

    PROP_LIMITS = {
        'volume': VOLUME_PROP_LIMIT,
        'prime_n_times': POSITIVE_INT_PROP_LIMIT,
    }

    def __init__(
        self,
        reagent: str,
        volume: Optional[float] = 'default',
        prime_n_times: Optional[int] = 'default',
        move_speed: Optional[float] = 'default',
        aspiration_speed: Optional[float] = 'default',
        dispense_speed: Optional[float] = 'default',

        # Internal properties
        reagent_vessel: Optional[str] = None,
        waste_vessel: Optional[str] = None,
        **kwargs
    ) -> None:
        super().__init__(locals())

    def on_prepare_for_execution(self, graph: Dict):
        """Prepares the current step for execution.
        Gets/sets/cleans up appropriate items in preparation for exection.

        Args:
            graph (Dict): Chemputer Graph to check
        """

        # Obtain the reagent vessel if not defined
        if not self.reagent_vessel:
            self.reagent_vessel = get_reagent_vessel(graph, self.reagent)

        if not self.waste_vessel:
            self.waste_vessel = get_waste_vessel(graph, self.reagent_vessel)

    def get_steps(self) -> List[Step]:
        """Get the list of steps/base steps to execute.

        Returns:
            List[Step]: Steps to execute.
        """

        return [Repeat(
            repeats=self.prime_n_times,
            children=[
                CMove(
                    from_vessel=self.reagent_vessel,
                    to_vessel=self.waste_vessel,
                    volume=self.volume,
                    move_speed=self.move_speed,
                    aspiration_speed=self.aspiration_speed,
                    dispense_speed=self.dispense_speed
                )
            ]
        )]

class FlushTubing(ChemputerStep, AbstractStep):
    """Flush tubing with inert gas (if present), otherwise air (if present),
    otherwise do nothing.

    Args:
        to_vessel (str): Vessel to move to
        to_port (str, optional): Port to move to. Defaults to None.
        volume (float, optional): Volume to flush. Defaults to 'default'.
        dispense_speed (float, optional): Pump speed. Defaults to 'default'.
        through_cartridge (str, optional): Cartridge to move through.
                                            Defaults to 'None'.
        flush_tube_vessel (str, optional): Vessel to move flushed solvent to.
                                            Defaults to 'None'.
    """

    PROP_TYPES = {
        'to_vessel': VESSEL_PROP_TYPE,
        'to_port': PORT_PROP_TYPE,
        'volume': float,
        'dispense_speed': float,
        'through_cartridge': str,
        'flush_tube_vessel': str,
    }

    DEFAULT_PROPS = {
        'dispense_speed': 40,
        'volume': f'{DEFAULT_AIR_FLUSH_TUBE_VOLUME} mL',
        'to_port': None,
        'through_cartridge': None,
    }

    INTERNAL_PROPS = [
        'flush_tube_vessel',
    ]

    PROP_LIMITS = {
        'volume': VOLUME_PROP_LIMIT,
    }

    def __init__(
        self,
        to_vessel: str,
        to_port: Optional[str] = 'default',
        volume: Optional[float] = 'default',
        dispense_speed: Optional[float] = 'default',
        through_cartridge: Optional[str] = 'default',

        # Internal props
        flush_tube_vessel: Optional[str] = None,
    ):
        super().__init__(locals())

    def on_prepare_for_execution(self, graph: Dict):
        """Prepares the current step for execution.
        Gets/sets/cleans up appropriate items in preparation for exection.

        Args:
            graph (Dict): Chemputer Graph to check
        """

        # Obtain the flush tube vessel if not defined
        if not self.flush_tube_vessel:
            self.flush_tube_vessel = get_flush_tube_vessel(
                graph, self.to_vessel
            )

    def get_steps(self) -> Optional[List[Step]]:
        """Get the list of steps/base steps to execute.

        Returns:
            Optional[List[Step]]: Steps to execute. None if no flush vessel.
        """

        # Using a flush tube vessel, get movement step
        if self.flush_tube_vessel:
            return [
                CMove(
                    from_vessel=self.flush_tube_vessel,
                    to_vessel=self.to_vessel,
                    to_port=self.to_port,
                    through=self.through_cartridge,
                    dispense_speed=self.dispense_speed,
                    volume=DEFAULT_AIR_FLUSH_TUBE_VOLUME
                )
            ]

        # No flush vessel, empty
        return []

class Transfer(ChemputerStep, AbstractStep):
    """Transfer contents of one vessel to another.

    Args:
        from_vessel (str): Vessel name to transfer from.
        to_vessel (str): Vessel name to transfer to.
        volume (float): Volume to transfer in mL.
        from_port (str): Port on from_vessel to transfer from.
        to_port (str): Port on to_vessel to transfer from.
        through (str): Node name to transfer to.
        aspiration_speed (float): Speed in mL / min to pull liquid out of
            from_vessel.
        move_speed (float): Speed in mL / min to move liquid at.
        dispense_speed (float): Speed in mL / min to push liquid out of pump
            into to_vessel.
        through_cartridge (str): Internal property. Cartridge to pass through.
    """

    DEFAULT_PROPS = {
        'aspiration_speed': 10,  # mL / min
        'dispense_speed': 40,  # mL / min
        'move_speed': 40,  # mL / min
        'viscous': False,
        'flush_tubing': False,
        'from_port': None,
        'to_port': None,
        'through': None,
        'time': None,
    }

    INTERNAL_PROPS = [
        'through_cartridge',
        'transfer_all',
        'from_vessel_has_stirrer',
        'from_vessel_has_heater',
        'from_vessel_has_chiller',
    ]

    PROP_TYPES = {
        'from_vessel': VESSEL_PROP_TYPE,
        'to_vessel': VESSEL_PROP_TYPE,
        'volume': float,
        'from_port': PORT_PROP_TYPE,
        'to_port': PORT_PROP_TYPE,
        'through': str,
        'time': float,
        'aspiration_speed': float,
        'move_speed': float,
        'dispense_speed': float,
        'viscous': bool,
        'through_cartridge': str,
        'transfer_all': bool,
        'from_vessel_has_stirrer': bool,
        'from_vessel_has_heater': bool,
        'from_vessel_has_chiller': bool,
        'flush_tubing': bool,
    }

    PROP_LIMITS = {
        'volume': VOLUME_PROP_LIMIT,
        'from_port': PORT_PROP_LIMIT,
        'to_port': PORT_PROP_LIMIT,
        'time': TIME_PROP_LIMIT,
    }

    def __init__(
        self,
        from_vessel: str,
        to_vessel: str,
        volume: float,
        from_port: Optional[str] = 'default',
        to_port: Optional[str] = 'default',
        through: Optional[str] = 'default',
        time: Optional[float] = 'default',
        aspiration_speed: Optional[float] = 'default',
        move_speed: Optional[float] = 'default',
        dispense_speed: Optional[float] = 'default',
        viscous: Optional[bool] = 'default',
        flush_tubing: Optional[bool] = 'default',

        # Internal properties
        through_cartridge: Optional[str] = None,
        transfer_all: Optional[bool] = False,
        from_vessel_has_stirrer: Optional[bool] = False,
        from_vessel_has_heater: Optional[bool] = None,
        from_vessel_has_chiller: Optional[bool] = None,
        **kwargs
    ) -> None:
        super().__init__(locals())

    def on_prepare_for_execution(self, graph: Dict) -> str:
        """Prepares the current step for execution.
        Gets/sets/cleans up appropriate items in preparation for exection.

        Args:
            graph (Dict): Chemputer Graph to check
        """

        # Obtain the through cartridge if not defined
        if not self.through_cartridge and self.through:
            self.through_cartridge = get_cartridge(graph, self.through)

        # Obtain the to port if not defined
        if self.to_port in [None, ''] and self.to_vessel:
            # Get the vessel class of the to_vessel
            to_class = graph.nodes[self.to_vessel]['class']

            # Ports are present in default ports, set them
            if to_class in DEFAULT_PORTS:
                self.to_port = DEFAULT_PORTS[to_class]['to']

        # Check if the from vessel has a stirrer attached
        self.from_vessel_has_stirrer = (
            True if get_vessel_stirrer(graph, self.from_vessel) else False
        )

        # From vessel is defined
        if self.from_vessel:
            # Get the vessel class from the graph
            from_class = graph.nodes[self.from_vessel]['class']

            # Get teh ports if not defined
            if self.from_port in [None, ''] and self.from_vessel:
                # Vessel class is present in default ports, set it
                if from_class in DEFAULT_PORTS:
                    self.from_port = DEFAULT_PORTS[from_class]['from']

            # Ge the heater and the chiller
            heater, chiller = get_heater_chiller(graph, self.from_vessel)

            # Check heater is present
            if self.from_vessel_has_heater is None:
                self.from_vessel_has_heater = True if heater else False

            # Check chiller is present
            if self.from_vessel_has_chiller is None:
                self.from_vessel_has_chiller = True if chiller else False

    def get_steps(self) -> List[Step]:
        """Get the list of steps/base steps to execute.

        Returns:
            List[Step]: Steps to execute.
        """

        return (
            self.get_stop_stir_steps()
            + self.get_move_steps()
            + self.get_flush_tubing_steps()
            + self.get_stop_heatchill_steps()
        )

    def get_move_steps(self) -> List[Step]:
        """Get the list of steps/base steps to execute.

        Returns:
            List[Step]: Steps to execute.
        """

        # Get the pump speeds
        dispense_speed = self.get_dispense_speed()
        aspiration_speed = self.get_aspiration_speed()

        return [
            CMove(
                from_vessel=self.from_vessel,
                from_port=self.from_port,
                to_vessel=self.to_vessel,
                to_port=self.to_port,
                volume=self.volume,
                through=self.through_cartridge,
                aspiration_speed=aspiration_speed,
                move_speed=self.move_speed,
                dispense_speed=dispense_speed
            )
        ]

    def get_flush_tubing_steps(self) -> Optional[List[Step]]:
        """Get the list of steps/base steps to execute.

        Returns:
            Optional[List[Step]]: Steps to execute. Noen if flushing not
                                    required.
        """

        # Return flush step if required, else []
        return [
            FlushTubing(
                to_vessel=self.to_vessel,
                to_port=self.to_port,
                through_cartridge=self.through_cartridge,
                dispense_speed=self.get_dispense_speed(),
            )
        ] if self.flush_tubing else []

    def get_stop_stir_steps(self) -> Optional[List[Step]]:
        """Get StopStir steps if required

        Returns:
            Optional[List[Step]]: StopStir steps, else []
        """

        # Set by executor in _add_all_volumes
        if self.transfer_all:
            # Stirrer present, stop it
            if self.from_vessel_has_stirrer:
                return [StopStir(self.from_vessel)]

        # Not transferring all, not required
        return []

    def get_stop_heatchill_steps(self) -> Optional[List[Step]]:
        """Get the StopHeatChill steps if heater or chiller present

        Returns:
            Optional[List[Step]]: StopHeatChill step if required, else []
        """

        # have either a heater or chiller, stop them
        if self.from_vessel_has_heater or self.from_vessel_has_chiller:
            return [StopHeatChill(vessel=self.from_vessel)]

        # No heater or chiller attached
        return []

    def sanity_checks(self, graph: Dict) -> List[SanityCheck]:
        """Gets a list of Sanity checks to perform for the step

        Args:
            graph (Dict): Chemputer graph to check

        Returns:
            List[SanityCheck]: List of checks to perform
        """

        return [
            SanityCheck(
                condition=self.from_vessel and node_in_graph(
                    graph, self.from_vessel),
                error_msg='from_vessel must be node in graph.',
            ),
            SanityCheck(
                condition=self.to_vessel and node_in_graph(
                    graph, self.to_vessel),
                error_msg='to_vessel must be node in graph.'
            ),
            SanityCheck(
                condition=not self.through or self.through_cartridge,
                error_msg=f'Trying to transfer through "{self.through}" but cannot find\
 cartridge containing {self.through}.'
            )
        ]

    def get_dispense_speed(self) -> float:
        """Calculates the dispensing speed of the pumps
        Dispense Speed (mL / min) = (Volume(ml) / time(min))

        Returns:
            float: Dispensing speed of the pump
        """

        if self.time and type(self.volume) != str:
            return self.volume / (self.time / 60)

        return self.dispense_speed

    def get_aspiration_speed(self) -> float:
        """Get the aspiration speed of the pump.
        Speed dependent on whether the solution is viscous or not

        Returns:
            float: Aspiration speed of the pump
        """

        return (
            self.aspiration_speed if not self.viscous
            else DEFAULT_VISCOUS_ASPIRATION_SPEED
        )

    def human_readable(self, language: str = 'en') -> str:
        """Get the human-readable text for the step

        Args:
            language (str, optional): Localisation language. Defaults to 'en'.

        Raises:
            KeyError: Language not supported

        Returns:
            str: Human-readable text for the step
        """

        # English human readable uses new system
        if language != 'en':
            try:
                if self.through:
                    if self.volume == 'all':
                        return HUMAN_READABLE_STEPS[
                            'Transfer (all through)'][language].format(
                                **self.formatted_properties())

                    else:
                        return HUMAN_READABLE_STEPS[
                            'Transfer (through)'][language].format(
                                **self.formatted_properties())

                elif self.volume == 'all':
                    return HUMAN_READABLE_STEPS[
                        'Transfer (all)'][language].format(
                            **self.formatted_properties())

                else:
                    return HUMAN_READABLE_STEPS[self.name][language].format(
                        **self.formatted_properties())

            # Langauge not supported
            except KeyError:
                return self.name

        # Using English
        else:
            return super().human_readable(language=language)
