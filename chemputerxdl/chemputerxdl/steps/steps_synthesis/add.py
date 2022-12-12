"""
.. module:: steps_synthesis.add
    :platforms; Unix, Windows
    :synopsis: XDL Step for adding a material to a vessel

"""

from typing import Optional, List, Dict, Any

# XDL
from xdl.steps.base_steps import Step, AbstractStep
from xdl.constants import VESSEL_PROP_TYPE, REAGENT_PROP_TYPE
from xdl.utils.misc import SanityCheck
from xdl.utils.prop_limits import (
    VOLUME_PROP_LIMIT,
    MASS_PROP_LIMIT,
    ROTATION_SPEED_PROP_LIMIT,
    TIME_PROP_LIMIT,
    POSITIVE_INT_PROP_LIMIT,
)

# Relative
from ..steps_utility import (
    PrimePumpForAdd, Wait, StopStir, StartStir, FlushTubing)
from ..steps_base import CMove, Confirm
from ..base_step import ChemputerStep
from ...constants import (
    DEFAULT_AFTER_ADD_WAIT_TIME,
    DEFAULT_VISCOUS_ASPIRATION_SPEED,
)
from ...localisation import HUMAN_READABLE_STEPS
# from ...utils.execution import (
#     get_waste_vessel,
#     get_reagent_vessel,
#     get_cartridge,
#     get_vessel_type,
# )
from ...utils.prop_limits import PORT_PROP_LIMIT
from ...constants import PORT_PROP_TYPE

class Add(ChemputerStep, AbstractStep):
    """Add given volume of given reagent to given vessel.

    Args:
        reagent (str): Reagent to add.
        volume (float): Volume of reagent to add.
        vessel (str): Vessel name to add reagent to.
        port (str): vessel port to use.
        through (str): Substrate to pass reagent through on way to vessel
        move_speed (float): Speed in mL / min to move liquid at. (optional)
        aspiration_speed (float): Aspiration speed (speed at which liquid is
            pulled out of reagent_vessel).
        dispense_speed (float): Dispense speed (speed at which liquid is pushed
            from pump into vessel).
        time (float): Time to spend dispensing liquid. Works by changing
            dispense_speed. Note: The time given here will not be the total step
            execution time, it will be the total time spent dispensing from the
            pump into self.vessel during the addition.
        stir (bool): If True, stirring will be started before addition.
        stir_speed (float): RPM to stir at, only relevant if stir = True.
        through_cartridge (str): Internal property. Node name of cartridge to
            pass reagent through on way to vessel.
        confirm_solid (bool): If False, skip Confirm step for solid addition
        priming_volume (float): Volume of reagent to use for priming tubing.

        anticlogging (bool): If True, a technique will be used to avoid clogging
            where reagent is added in small portions, each one followed by a
            small portion of solvent.
        anticlogging_solvent (str): Solvent to add between reagent additions
            during anticlogging routine.
        anticlogging_solvent_volume (float): Optional. Portion of solvent to add
            in each cycle of anticlogging add routine.
        anticlogging_reagent_volume (float): Optional. Portion of reagent to add
            in each cycle of anticlogging add routine.
        anticlogging_solvent_vessel (str): Given internally. Vessel containing
            anticlogging solvent.

        reagent_vessel (str): Given internally. Vessel containing reagent.
        waste_vessel (str): Given internally. Vessel to send waste to.
    """

    DEFAULT_PROPS = {
        'volume': None,
        'mass': None,
        'port': None,
        'through': None,
        'time': None,
        'anticlogging_solvent': None,
        'move_speed': 40,  # mL / min
        'aspiration_speed': 10,  # mL / min
        'dispense_speed': 40,  # mL / min
        'viscous': False,
        'stir_speed': '250 RPM',
        'anticlogging': False,
        'anticlogging_solvent_volume': '2 mL',
        'anticlogging_reagent_volume': '10 mL',
        'confirm_solid': True,
        'stir': False,
        'prime_n_times': 1,
        'priming_volume': '3 mL',
    }

    PROP_TYPES = {
        'reagent': REAGENT_PROP_TYPE,
        'vessel': VESSEL_PROP_TYPE,
        'volume': float,
        'mass': float,
        'port': PORT_PROP_TYPE,
        'through': str,
        'move_speed': float,
        'aspiration_speed': float,
        'dispense_speed': float,
        'viscous': bool,
        'time': float,
        'stir': bool,
        'stir_speed': float,
        'confirm_solid': bool,
        'anticlogging': bool,
        'anticlogging_solvent': REAGENT_PROP_TYPE,
        'anticlogging_solvent_volume': float,
        'anticlogging_reagent_volume': float,
        'through_cartridge': str,
        'reagent_vessel': str,
        'waste_vessel': str,
        'vessel_type': str,
        'anticlogging_solvent_vessel': str,
        'prime_n_times': int,
        'priming_volume': float,
    }

    INTERNAL_PROPS = [
        'through_cartridge',
        'reagent_vessel',
        'waste_vessel',
        'vessel_type',
        'anticlogging_solvent_vessel',
    ]

    PROP_LIMITS = {
        'volume': VOLUME_PROP_LIMIT,
        'mass': MASS_PROP_LIMIT,
        'port': PORT_PROP_LIMIT,
        'time': TIME_PROP_LIMIT,
        'stir_speed': ROTATION_SPEED_PROP_LIMIT,
        'anticlogging_solvent_volume': VOLUME_PROP_LIMIT,
        'anticlogging_reagent_volume': VOLUME_PROP_LIMIT,
        'prime_n_times': POSITIVE_INT_PROP_LIMIT,
        'priming_volume': VOLUME_PROP_LIMIT,
    }

    def __init__(
        self,
        reagent: str,
        vessel: str,
        volume: Optional[float] = 'default',
        mass: Optional[float] = 'default',
        port: Optional[str] = 'default',
        through: Optional[str] = 'default',
        move_speed: Optional[float] = 'default',
        aspiration_speed: Optional[float] = 'default',
        dispense_speed: Optional[float] = 'default',
        viscous: Optional[bool] = 'default',
        time: Optional[float] = 'default',
        stir: Optional[bool] = 'default',
        stir_speed: Optional[float] = 'default',
        confirm_solid: Optional[bool] = 'default',
        prime_n_times: Optional[int] = 'default',
        priming_volume: Optional[float] = 'default',

        anticlogging: Optional[bool] = 'default',
        anticlogging_solvent: Optional[str] = 'default',
        anticlogging_solvent_volume: Optional[float] = 'default',
        anticlogging_reagent_volume: Optional[float] = 'default',

        # Internal properties
        through_cartridge: Optional[str] = None,
        reagent_vessel: Optional[str] = None,
        waste_vessel: Optional[str] = None,
        vessel_type: Optional[str] = None,
        anticlogging_solvent_vessel: Optional[str] = None,
        **kwargs
    ) -> None:
        super().__init__(locals())

    def on_prepare_for_execution(self, graph: Dict):
        """Prepares the current step for execution.
        Gets/sets/cleans up appropriate items in preparation for exection.

        Args:
            graph (Dict): Chemputer Graph to check
        """

        # Obtain the waste vessel if not defined
        if not self.waste_vessel:
            self.waste_vessel = get_waste_vessel(
                graph, self.vessel
            )

        # Obtain the reagent vessel if not defined
        if not self.reagent_vessel:
            self.reagent_vessel = get_reagent_vessel(graph, self.reagent)

        # Obtain the anticlogging vessel if a solvent has been supplied
        if self.anticlogging_solvent and not self.anticlogging_solvent_vessel:
            self.anticlogging_solvent_vessel = get_reagent_vessel(
                graph, self.anticlogging_solvent
            )

        # Obtain the through cartridge if through nodes have been defined
        if not self.through_cartridge and self.through:
            self.through_cartridge = get_cartridge(graph, self.through)

        # Obtian the vessel type if not defined
        if not self.vessel_type:
            self.vessel_type = get_vessel_type(graph, self.vessel)

    def get_steps(self) -> List[Step]:
        """Get the list of steps/base steps to execute.

        Returns:
            List[Step]: Steps to execute.
        """

        # List to hold the execution steps
        steps = []

        # Solid addition
        if self.volume is None and self.mass is not None and self.confirm_solid:
            steps = [
                Confirm('Is {reagent} ({mass} g) in {vessel}?'.format(
                    **self.properties
                ))
            ]

        # Liquid addition
        else:
            # Get the anticlogging steps
            if self.anticlogging:
                steps = self.get_anticlogging_add_steps()

            # No anticlogging needed, get the Add steps
            else:
                steps = self.get_add_steps()

            # Add a step to flush the tubung
            steps.append(
                FlushTubing(
                    to_vessel=self.vessel,
                    to_port=self.port,
                    dispense_speed=self.get_dispense_speed(),
                    through_cartridge=self.through_cartridge,
                )
            )

            # Add Stirring step if stirring required
            if self.stir:
                steps.insert(
                    0,
                    StartStir(
                        vessel=self.vessel,
                        vessel_type=self.vessel_type,
                        stir_speed=self.stir_speed
                    )
                )

            # Stirring not required, add a stop stirring step
            else:
                steps.insert(0, StopStir(vessel=self.vessel))

        return steps

    def get_add_steps(self) -> List[Step]:
        """Get all Addition steps.

        Returns:
            List[Step]: Steps associated with addition
        """

        # Set pump aspiration speed depending on viscosity
        aspiration_speed = (
            self.aspiration_speed if not self.viscous
            else DEFAULT_VISCOUS_ASPIRATION_SPEED
        )

        # Return addition steps
        return [
            PrimePumpForAdd(
                reagent=self.reagent,
                volume=self.priming_volume,
                waste_vessel=self.waste_vessel,
                prime_n_times=self.prime_n_times,
                move_speed=self.move_speed,
                aspiration_speed=aspiration_speed,
                dispense_speed=self.get_dispense_speed()
            ),
            CMove(
                from_vessel=self.reagent_vessel,
                to_vessel=self.vessel,
                to_port=self.port,
                volume=self.volume,
                through=self.through_cartridge,
                move_speed=self.move_speed,
                aspiration_speed=aspiration_speed,
                dispense_speed=self.get_dispense_speed()
            ),
            Wait(time=DEFAULT_AFTER_ADD_WAIT_TIME)
        ]

    def get_anticlogging_add_steps(self) -> List[Step]:
        """Get all addition steps associated with anticlogging.

        Returns:
            List[Step]: Steps associated with anticlogging addition
        """

        # Obtain the dispense speed for the pumps
        dispense_speed = self.get_dispense_speed()

        # Add step for priming the pump
        steps = [
            PrimePumpForAdd(
                reagent=self.reagent,
                volume=self.priming_volume,
                waste_vessel=self.waste_vessel,
                prime_n_times=self.prime_n_times,
                move_speed=self.move_speed,
                aspiration_speed=self.aspiration_speed,
                dispense_speed=dispense_speed
            )
        ]

        # Calculate the total number of additions required
        n_adds = int(self.volume / self.anticlogging_reagent_volume) + 1

        # Add a Movement step for each addition required
        for _ in range(n_adds):
            steps.extend([
                CMove(
                    from_vessel=self.reagent_vessel,
                    to_vessel=self.vessel,
                    to_port=self.port,
                    volume=self.anticlogging_reagent_volume,
                    move_speed=self.move_speed,
                    aspiration_speed=self.aspiration_speed,
                    dispense_speed=dispense_speed),
                CMove(
                    from_vessel=self.anticlogging_solvent_vessel,
                    to_vessel=self.vessel,
                    to_port=self.port,
                    volume=self.anticlogging_solvent_volume,
                    move_speed=self.move_speed,
                    aspiration_speed=self.aspiration_speed,
                    dispense_speed=dispense_speed),
            ])

        # Add in a wait time after addition
        steps.append(Wait(time=DEFAULT_AFTER_ADD_WAIT_TIME))

        return steps

    def human_readable(self, language: str = 'en') -> str:
        """Get the human-readbale text for the step, based on localisation

        Args:
            language (str, optional): Localisation language. Defaults to 'en'.

        Returns:
            str: HUman-readable text for the step
        """

        # Not english
        if language != 'en':
            try:
                # Mass is defined
                if self.mass is not None:
                    # Get step text for the given language
                    return HUMAN_READABLE_STEPS['Add (mass)'][language].format(
                        **self.formatted_properties()
                    )

                # Volume is defined
                elif self.volume is not None:
                    # Get step text for given language
                    return (HUMAN_READABLE_STEPS['Add (volume)'][language]
                            .format(
                                **self.formatted_properties())
                            )

                # Default to returning the name
                else:
                    return self.name

            # Language not found, default to using name
            except KeyError:
                return self.name

        # Using english, use default human_readable method
        else:
            return super().human_readable(language=language)

    @property
    def requirements(self) -> Dict[str, Dict[str, Any]]:
        """Get any requirements this step needs

        Returns:
            Dict[str, Dict[str, Any]]: Dictionary contianing step requirements
        """

        return {
            'vessel': {
                'stir': self.stir,
            }
        }

    def get_dispense_speed(self) -> float:
        """Get the current dispensing speed

        Returns:
            float: Dispensing speed
        """

        # Time has been supplied, calculate dispensing speed
        if self.time:
            return self.volume / (self.time / 60)

        # Return already defined speed
        return self.dispense_speed

    def sanity_checks(self, graph: Dict) -> List[SanityCheck]:
        """Gets a list of Sanity checks to perform for the step

        Args:
            graph (Dict): Chemputer graph to check

        Returns:
            List[SanityCheck]: List of checks to perform
        """

        return [
            SanityCheck(
                condition=not self.through or self.through_cartridge,
                error_msg=f'Trying to add through "{self.through}" but cannot\
 find cartridge containing {self.through}.'
            ),

            SanityCheck(
                condition=self.mass or self.reagent_vessel,
                error_msg=f'No reagent flask present containing\
 "{self.reagent}".'
            ),

            SanityCheck(
                condition=self.vessel,
                error_msg=f'{self.vessel} cannot be None.'
            ),

            SanityCheck(
                condition=self.volume is not None or self.mass is not None,
                error_msg='Either volume or mass must be given.'
            ),

            SanityCheck(
                condition=self.waste_vessel,
                error_msg='Cannot find waste vessel to use when priming tubing.'
            )
        ]

    def scale(self, scale: float):
        """Scale volumes and/or masses by a given factor

        Args:
            scale (float): Scaling factor
        """

        if self.volume is not None:
            self.volume *= scale
        if self.mass is not None:
            self.mass *= scale
