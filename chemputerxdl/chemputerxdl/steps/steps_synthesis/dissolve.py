"""
.. module:: steps_synthesis.dissolve
    :platforms: Unix, Windows
    :synopsis: XDL step for dissolving a material in a flask or rotavap

"""

from typing import Optional, List, Dict, Any

# XDL
from xdl.steps.base_steps import Step
from xdl.steps.templates import AbstractDissolveStep
from xdl.utils.prop_limits import (
    TIME_PROP_LIMIT,
    TEMP_PROP_LIMIT,
    VOLUME_PROP_LIMIT,
    ROTATION_SPEED_PROP_LIMIT,
)
from xdl.constants import VESSEL_PROP_TYPE, REAGENT_PROP_TYPE

# Relative
from .add import Add
from ..base_step import ChemputerStep
from ..steps_utility import Wait, HeatChillToTemp, StopHeatChill
from ..steps_base import (
    CRotavapSetRotationSpeed,
    CRotavapStartRotation,
    CRotavapStopRotation,
    CRotavapSetTemp,
    CRotavapStartHeater,
    CRotavapStopHeater,
    CRotavapLiftDown,
    CRotavapLiftUp,
)
from ...constants import DEFAULT_DISSOLVE_ROTAVAP_ROTATION_SPEED, PORT_PROP_TYPE
#from ...utils.execution import get_reagent_vessel, get_vessel_type
from ...utils.prop_limits import VESSEL_TYPE_PROP_LIMIT, PORT_PROP_LIMIT

class Dissolve(ChemputerStep, AbstractDissolveStep):
    """Dissolve contents of vessel in given solvent.

    Args:
        vessel (str): Vessel to dissolve contents of.
        solvent (str): Solvent to dissolve contents of vessel with.
        volume (float): Volume of solvent to use.
        port (str): Port to add solvent to.
        temp (float): Temperature to stir at. Optional.
        time (float): Time to stir for. Optional.
        stir_speed (float): Speed to stir at in RPM.
        solvent_vessel (str): Given internally. Flask containing solvent.
        vessel_type (str): Given internally. 'reactor', 'filter', 'rotavap',
            'flask' or 'separator'.
    """

    DEFAULT_PROPS = {
        'time': '20 minutes',
        'temp': '25°C',
        'stir_speed': '400 RPM',
        'port': None,
    }

    PROP_TYPES = {
        'vessel': VESSEL_PROP_TYPE,
        'solvent': REAGENT_PROP_TYPE,
        'volume': float,
        'port': PORT_PROP_TYPE,
        'temp': float,
        'time': float,
        'stir_speed': float,
        'solvent_vessel': str,
        'vessel_type': str
    }

    INTERNAL_PROPS = [
        'solvent_vessel',
        'vessel_type',
    ]

    PROP_LIMITS = {
        'volume': VOLUME_PROP_LIMIT,
        'port': PORT_PROP_LIMIT,
        'temp': TEMP_PROP_LIMIT,
        'time': TIME_PROP_LIMIT,
        'stir_speed': ROTATION_SPEED_PROP_LIMIT,
        'vessel_type': VESSEL_TYPE_PROP_LIMIT,
    }

    def __init__(
        self,
        vessel: str,
        solvent: str,
        volume: float,
        port: Optional[str] = 'default',
        temp: Optional[float] = 'default',
        time: Optional[float] = 'default',
        stir_speed: Optional[float] = 'default',

        # Internal properties
        solvent_vessel: Optional[str] = None,
        vessel_type: Optional[str] = None,
        **kwargs,
    ) -> None:
        super().__init__(locals())

    def on_prepare_for_execution(self, graph: Dict):
        """Prepares the current step for execution.
        Gets/sets/cleans up appropriate items in preparation for exection.

        Args:
            graph (Dict): Chemputer Graph to check
        """

        # Obtain solvent vessel if not defined
        if not self.solvent_vessel:
            self.solvent_vessel = get_reagent_vessel(graph, self.solvent)

        # Obtain the vessel type if not defined
        if not self.vessel_type:
            self.vessel_type = get_vessel_type(graph, self.vessel)

    def get_steps(self) -> List[Step]:
        """Get the list of steps/base steps to execute.

        Returns:
            List[Step]: Steps to execute.
        """

        # Get steps needed if the vessel type is a rotavap
        if self.vessel_type == 'rotavap':
            steps = [
                Add(reagent=self.solvent,
                    volume=self.volume,
                    vessel=self.vessel,
                    port=self.port,
                    stir=False),
                CRotavapSetTemp(self.vessel, self.temp),
                CRotavapStartHeater(self.vessel),
                CRotavapSetRotationSpeed(
                    self.vessel, DEFAULT_DISSOLVE_ROTAVAP_ROTATION_SPEED
                ),
                CRotavapStartRotation(self.vessel),
                CRotavapLiftDown(self.vessel),
                Wait(self.time),
                CRotavapStopRotation(self.vessel),
                CRotavapStopHeater(self.vessel),
                CRotavapLiftUp(self.vessel),
            ]

        # Get steps needed for any other type of vessel
        else:
            steps = [
                Add(
                    reagent=self.solvent,
                    volume=self.volume,
                    vessel=self.vessel,
                    port=self.port
                ),
                HeatChillToTemp(
                    vessel=self.vessel,
                    temp=self.temp,
                    stir=True,
                    stir_speed=self.stir_speed
                ),
                Wait(self.time),
                StopHeatChill(vessel=self.vessel),
            ]

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
                'temp': [self.temp],
                'stir': True,
            }
        }

    def scale(self, scale: float):
        """Scale the step by a scale factor

        Args:
            scale (float): Scale factor
        """

        self.scale *= scale
