"""
.. module:: steps_synthesis.evaporate
    :platforms: Unix, Windows
    :synopsis: XDL step for evaporation of material form a vessel

"""

from typing import Optional, List, Dict, Any

# XDL
from xdl.steps.base_steps import Step, AbstractStep
from xdl.utils.prop_limits import (
    TIME_PROP_LIMIT,
    TEMP_PROP_LIMIT,
    VOLUME_PROP_LIMIT,
    ROTATION_SPEED_PROP_LIMIT,
    PRESSURE_PROP_LIMIT,
    PropLimit,
)
from xdl.constants import VESSEL_PROP_TYPE
from xdl.utils.graph import undirected_neighbors

# Relative
from ..base_step import ChemputerStep
from ..steps_base import (
    CRotavapLiftDown,
    CRotavapAutoEvaporation,
)
from ..steps_utility import (
    HeatChillToTemp,
    StopHeatChill,
    Wait,
    Purge,
    Transfer,
    RotavapStopEverything,
    RotavapHeatToTemp,
    RotavapStartVacuum,
    RotavapStartRotation,
)

from ..steps_base.chiller import (
    CStartChiller,
    CStopChiller
)
from ...constants import (
    COLLECT_PORT, ROTAVAP_CLASSES, CHILLER_CLASSES, CHEMPUTER_WASTE)
#from ...utils.execution import get_nearest_node

class Evaporate(ChemputerStep, AbstractStep):
    """Evaporate contents of given vessel at given temp and given pressure for
    given time.

    Args:
        rotavap_name (str): Name of rotavap vessel.
        temp (float): Temperature to set rotavap water bath to in °C.
        pressure (float): Pressure to set rotavap vacuum to in mbar. Has no
            effect if mode == 'auto', otherwise must be passed.
        time (float): Time to rotavap for in seconds.
        rotation_speed (float): Speed in RPM to rotate flask at.
        mode (str): 'manual' or 'auto'. If 'manual', given time/temp/pressure
            are used. If 'auto', automatic pressure/time evaluation built into
            the rotavap are used. In this case time and pressure should still be
            given, but correspond to maximum time and minimum pressure that if
            either is reached, the evaporation will stop.
    """

    DEFAULT_PROPS = {
        'time': '2 hrs',
        'rotation_speed': '150 RPM',
        'pressure': None,
        'mode': 'manual',
        'temp': '25°C',
    }

    PROP_TYPES = {
        'rotavap_name': VESSEL_PROP_TYPE,
        'temp': float,
        'pressure': float,
        'time': float,
        'rotation_speed': float,
        'mode': str,
        'waste_vessel': str,
        'collection_flask_volume': float,
        'has_chiller': bool
    }

    INTERNAL_PROPS = [
        'waste_vessel',
        'collection_flask_volume',
        'has_chiller',
    ]

    PROP_LIMITS = {
        'temp': TEMP_PROP_LIMIT,
        'pressure': PRESSURE_PROP_LIMIT,
        'time': TIME_PROP_LIMIT,
        'rotation_speed': ROTATION_SPEED_PROP_LIMIT,
        'mode': PropLimit(
            enum=['manual', 'auto', 'purge'],
            default='manual',
        ),
        'collection_flask_volume': VOLUME_PROP_LIMIT,
    }

    def __init__(
        self,
        rotavap_name: str,
        temp: float = 'default',
        pressure: Optional[float] = 'default',
        time: Optional[float] = 'default',
        rotation_speed: Optional[float] = 'default',
        mode: Optional[str] = 'default',

        # Internal properties
        waste_vessel: Optional[str] = None,
        collection_flask_volume: Optional[float] = None,
        has_chiller: bool = False,
        **kwargs
    ):
        super().__init__(locals())

    def on_prepare_for_execution(self, graph: Dict):
        """Prepares the current step for execution.
        Gets/sets/cleans up appropriate items in preparation for exection.

        Args:
            graph (Dict): Chemputer Graph to check
        """

        # Obtain collection volume form rotavap if not defined
        if not self.collection_flask_volume:
            rotavap = graph.nodes[self.rotavap_name]
            if 'collection_flask_volume' in rotavap:
                self.collection_flask_volume = rotavap[
                    'collection_flask_volume'
                ]

        # Obtian waste vesse lif not defined
        if not self.waste_vessel:
            self.waste_vessel = get_nearest_node(
                graph, self.rotavap_name, CHEMPUTER_WASTE
            )

        # Iterate through al lgraph nodes
        for node, data in graph.nodes(data=True):
            # Get all attached vesses to the current node
            attached_vessels = [i for i in undirected_neighbors(graph, node)]

            # Current node is a Rotavap
            if data["class"] in ROTAVAP_CLASSES:
                # Iterate through all vessels
                for vessel in attached_vessels:
                    # Chiller is attached, set flag
                    if graph.nodes[vessel]["class"] in CHILLER_CLASSES:
                        self.has_chiller = True

    def get_chiller_steps_if_present(
        self, start: bool = True
    ) -> Optional[Step]:
        """Get chiller steps if a chiller is present

        Args:
            start (bool, optional): Start the chiller or stop. Defaults to True.

        Returns:
            Optional[Step]: Chiller step if present.
        """

        # Chiller is attached
        if self.has_chiller:
            if start:
                return CStartChiller(self.rotavap_name)
            return CStopChiller(self.rotavap_name)

    def get_default_steps(self, col_vol: float) -> List[Step]:
        """Get the list of default steps to execute for this Step.

        Args:
            col_vol (float): Colleciton volume

        Returns:
            List[Step]: Steps to execute
        """

        return [
            # Start rotation
            RotavapStartRotation(self.rotavap_name, self.rotation_speed),
            # Lower flask into bath.
            CRotavapLiftDown(self.rotavap_name),
            # Start chiller if present
            self.get_chiller_steps_if_present(),
            # Start vacuum
            RotavapStartVacuum(self.rotavap_name, self.pressure),
            # Start heating
            RotavapHeatToTemp(self.rotavap_name, self.temp),
            # Wait for evaporation to happen.
            Wait(time=self.time),
            # Stop evaporation.
            RotavapStopEverything(self.rotavap_name),
            # Stop chiller if present
            self.get_chiller_steps_if_present(start=False),
            # Empty collect flask
            Transfer(
                from_vessel=self.rotavap_name,
                to_vessel=self.waste_vessel,
                from_port=COLLECT_PORT,
                volume=col_vol
            )
        ]

    def get_auto_steps(self, col_vol: float) -> List[Step]:
        """Get steps for automatic evaporation

        Args:
            col_vol (float): Collection volume

        Returns:
            List[Step]: Steps to execute
        """

        # Default presure
        pressure = 1  # 1 == auto pressure

        # Pressure already defined
        if self.pressure:
            # Approximation. Pressure given should be pressure solvent
            # evaporates at, but in auto evaporation, pressure is the limit
            # of the pressure ramp, so actual pressure given needs to be
            # lower.
            pressure = self.pressure / 2

        return [
            # Start rotation
            RotavapStartRotation(self.rotavap_name, self.rotation_speed),
            # Lower flask into bath.
            CRotavapLiftDown(self.rotavap_name),
            # Start chiller if present
            self.get_chiller_steps_if_present(),
            # Start heating
            RotavapHeatToTemp(self.rotavap_name, self.temp),
            # Auto Evaporation
            CRotavapAutoEvaporation(
                rotavap_name=self.rotavap_name,
                sensitivity=2,  # High sensitivity
                vacuum_limit=pressure,
                time_limit=self.time,
                vent_after=True
            ),
            # Stop evaporation.
            RotavapStopEverything(self.rotavap_name),
            # Stop chiller if present
            self.get_chiller_steps_if_present(start=False),
            # Empty collect flask
            Transfer(
                from_vessel=self.rotavap_name,
                to_vessel=self.waste_vessel,
                from_port=COLLECT_PORT,
                volume=col_vol
            )
        ]

    def get_purge_steps(self) -> List[Step]:
        """Get steps for ``mode='purge'``. Do evaporation by purging liquid with
        gas.
        """
        steps = []
        if self.temp is not None:
            steps.append(HeatChillToTemp(
                vessel=self.rotavap_name,
                temp=self.temp,
            ))
        steps.append(
            Purge(
                vessel=self.rotavap_name,
                time=self.time,
            )
        )
        if self.temp is not None:
            steps.append(StopHeatChill(vessel=self.rotavap_name))
        return steps

    def get_steps(self) -> List[Step]:
        """Get the list of steps/base steps to execute.

        Returns:
            List[Step]: Steps to execute.
        """

        # Define the colelction volume
        collection_flask_volume = 'all'

        # Collection volume defiend
        if self.collection_flask_volume:
            collection_flask_volume = self.collection_flask_volume

        # Auto evaporation mode
        if self.mode == "auto":
            # Get automatic evaporation steps
            steps = self.get_auto_steps(collection_flask_volume)

        # Purge mode
        elif self.mode == 'purge':
            steps = self.get_purge_steps()

        # Manual mode
        else:
            # Get Default steps
            steps = self.get_default_steps(collection_flask_volume)

        # Remove blanks
        steps = [step for step in steps if step is not None]
        return steps

    @property
    def requirements(self) -> Dict[str, Dict[str, Any]]:
        """Get the requirements needed for this step

        Returns:
            Dict[str, Dict[str, Any]]: Step requirements
        """

        # Temp is defined and above 25, require heat chill
        heatchill = True if self.temp and self.temp > 25 else False

        # Define requires temperatures
        temps = []
        if self.temp:
            temps = [self.temp]

        # Return requirements
        return {
            'rotavap_name': {
                'rotavap': True,
                'heatchill': heatchill,
                'temp': temps,
            }
        }
