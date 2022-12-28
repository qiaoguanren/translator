"""
.. module:: steps_synthesis.recrystallize
    :platforms: Unix, Windows
    :synopsis: XDL step to recrystallize a solid by changing temperature and
                stirring rate

"""

from typing import List, Dict, Any

# XDL
from xdl.steps.base_steps import AbstractStep, Step
from xdl.utils.prop_limits import (
    TIME_PROP_LIMIT,
    TEMP_PROP_LIMIT,
    VOLUME_PROP_LIMIT
)
from xdl.constants import REAGENT_PROP_TYPE, VESSEL_PROP_TYPE

# Relative
from .heatchill import HeatChill
from .dissolve import Dissolve
from ..base_step import ChemputerStep
from ...localisation import HUMAN_READABLE_STEPS

class Recrystallize(ChemputerStep, AbstractStep):
    """Step to recrystallize a solid by changing temperature and stirring rate

    Args:
        vessel (str): Crystallization vessel
        time (float): Time to wait for crystallization
        dissolve_temp (float): Temperature to dissolve crystals
        crystallize_temp (float): Temperature to induce crystallization
        solvent (str): Solvent to use
        solvent_volume (float): Volume of solvent to use
    """

    DEFAULT_PROPS = {
        'time': '2 hrs',
        'crystallize_temp': '25°C',
        'dissolve_temp': '25°C',
        'solvent': None,
        'solvent_volume': '10 mL',
    }

    PROP_TYPES = {
        'vessel': VESSEL_PROP_TYPE,
        'time': float,
        'dissolve_temp': float,
        'crystallize_temp': float,
        'solvent': REAGENT_PROP_TYPE,
        'solvent_volume': float
    }

    PROP_LIMITS = {
        'time': TIME_PROP_LIMIT,
        'dissolve_temp': TEMP_PROP_LIMIT,
        'crystallize_temp': TEMP_PROP_LIMIT,
        'solvent_volume': VOLUME_PROP_LIMIT,
    }

    def __init__(
        self,
        vessel: str,
        time: float = 'default',
        dissolve_temp: float = 'default',
        crystallize_temp: float = 'default',
        solvent: str = 'default',
        solvent_volume: float = 'default',
        **kwargs
    ):
        super().__init__(locals())

    def get_steps(self) -> List[Step]:
        """Get the list of steps/base steps to execute.

        Returns:
            List[Step]: Steps to execute.
        """

        steps = []

        # using solvent so get the dissolve steps
        if self.solvent:
            steps.append(self.get_dissolve_step())

        # Add crystallisation steps to list
        steps.append(self.get_crystallize_steps())

        return steps

    def get_dissolve_step(self) -> Step:
        """Get the Dissolve step

        Returns:
            Step: Dissolve steps
        """

        return Dissolve(
            vessel=self.vessel,
            solvent=self.solvent,
            volume=self.solvent_volume,
            temp=self.dissolve_temp,
        )

    def get_crystallize_steps(self) -> Step:
        """Get the HeatChill step to enduce crystallisation

        Returns:
            Step: HeatChill step
        """

        return HeatChill(
            vessel=self.vessel,
            temp=self.crystallize_temp,
            time=self.time,
            stir=True,
        )

    @property
    def requirements(self) -> Dict[str, Dict[str, Any]]:
        """Get the requirements needed for this step

        Returns:
            Dict[str, Dict[str, Any]]: Step requirements
        """

        temps = []
        if self.crystallize_temp:
            temps.append(self.crystallize_temp)
        if self.dissolve_temp:
            temps.append(self.dissolve_temp)
        return {
            'vessel': {
                'heatchill': True,
                'temp': temps
            }
        }

    def human_readable(self, language: str = 'en') -> str:
        """Gets the human-readable text for this step

        Args:
            language (str, optional): Localisation language. Defaults to 'en'.

        Raises:
            KeyError: Localisation language is not supported

        Returns:
            str: Human-readable text for this step
        """

        # English human readable uses new system
        if language != 'en':
            try:
                # Human-readable Dissolve Step
                if self.solvent:
                    return HUMAN_READABLE_STEPS[
                        'Recrystallize (with solvent)'][language].format(
                            **self.formatted_properties())

                # Human-readable HeatChill step
                else:
                    return HUMAN_READABLE_STEPS[
                        'Recrystallize (without solvent)'][language].format(
                            **self.formatted_properties())

            # Language is not supported
            except KeyError:
                return self.name

        # Return default English text
        else:
            return super().human_readable(language=language)
