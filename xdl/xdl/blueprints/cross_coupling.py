from .base_blueprint import ReactionBlueprint
from ..steps.placeholders import (
    AddSolid,
    Dissolve,
    HeatChill,
    Evaporate,
    Filter,
    EvacuateAndRefill,
)
from ..reagents import Reagent
from ..utils.prop_limits import (
    MASS_PROP_LIMIT,
    TIME_PROP_LIMIT,
    TEMP_PROP_LIMIT,
)

class CrossCouplingBlueprint(ReactionBlueprint):
    """Generic cross coupling reaction blueprint. The wide variety of named
    cross coupling reactions is generally accessed by using different substrates
    """

    reaction_vessel = 'reactor'
    evaporation_vessel = 'rotavap'

    base_equivs = 1.5
    halide_equivs = 1.5

    PROP_TYPES = {
        'catalyst': str,
        'substrate': str,
        'substrate_mol': float,
        'substrate_molar_mass': float,
        'halide': str,
        'halide_molar_mass': float,
        'base': str,
        'base_molar_mass': float,

        'solvent': str,
        'quencher': str,
        'quencher_mass': float,
        'catalyst_mass': float,

        'temp': float,
        'time': float,
    }

    DEFAULT_PROPS = {
        'solvent': None,
        'catalyst_mass': '0.05 g',
        'quencher_mass': '20 g',
        'quencher': 'solid sodium carbonate',

        'temp': 100,
        'time': '1 hr',
    }

    PROP_LIMITS = {
        'catalyst_mass': MASS_PROP_LIMIT,
        'temp': TEMP_PROP_LIMIT,
        'time': TIME_PROP_LIMIT,
    }

    def __init__(
        self,
        catalyst: str,
        substrate: str,
        substrate_mol: float,
        substrate_molar_mass: float,
        base: str,
        base_molar_mass: float,
        halide: str,
        halide_molar_mass: float,

        solvent: str = 'default',
        quencher: str = 'default',
        quencher_mass: float = 'default',
        catalyst_mass: float = 'default',

        temp: float = 'default',
        time: float = 'default',
    ):
        super().__init__(locals())

    def get_solvent(self):
        if self.solvent is None:
            return '1,4-Dioxane'
        return self.solvent

    def get_solvent_volume(self):
        """Solvent volume is calculated as 5 mL / mmol of starting material.
        """
        return self.substrate_mol * 100 * 5

    def get_halide_mol(self):
        """Get number of moles of halide to use."""
        return self.substrate_mol * self.halide_equivs

    def get_base_mol(self):
        """Get number of moles of base to use."""
        return self.substrate_mol * self.base_equivs

    def get_halide_mass(self):
        return self.halide_molar_mass * self.get_halide_mol()

    def get_substrate_mass(self):
        return self.substrate_mol * self.substrate_molar_mass

    def get_base_mass(self):
        return self.get_base_mol() * self.base_molar_mass

    def build_prep(self):
        """Add all reactants and dissolve in solvent."""
        solvent = self.get_solvent()
        reagents = [
            Reagent(reagent) for reagent in
            [self.catalyst, self.halide, self.substrate, solvent]
        ]
        steps = [
            AddSolid(
                reagent=self.catalyst,
                vessel=self.reaction_vessel,
                mass=self.catalyst_mass,
                stir=False,
            ),
            Dissolve(
                vessel=self.reaction_vessel,
                solvent=self.solvent,
                volume=self.get_solvent_volume(),
            ),
            AddSolid(
                reagent=self.halide,
                vessel=self.reaction_vessel,
                mass=self.get_halide_mass(),
                mol=self.get_halide_mol(),
                stir=True,
            ),
            AddSolid(
                reagent=self.substrate,
                vessel=self.reaction_vessel,
                mass=self.get_substrate_mass(),
                mol=self.substrate_mol,
                stir=True,
            ),
        ]
        if self.base is not None:
            reagents.append(Reagent(self.base))
            steps.append(
                AddSolid(
                    reagent=self.base,
                    vessel=self.reaction_vessel,
                    mass=self.get_base_mass(),
                    stir=True,
                    mol=self.get_base_mol(),
                )
            )
        return steps, reagents

    def build_reaction(self):
        """React for at given temp for given time."""
        reagents = []
        steps = [
            HeatChill(
                vessel=self.reaction_vessel,
                temp=self.temp,
                time=self.time,
            ),
        ]
        return steps, reagents

    def build_workup(self):
        """Quench reaction, filter off quenching reagent and evaporate solvent.
        """
        reagents = [Reagent(self.quencher)]
        steps = [
            EvacuateAndRefill(vessel=self.reaction_vessel),
            AddSolid(
                reagent=self.quencher,
                vessel=self.reaction_vessel,
                mass=self.quencher_mass,
                stir=True,
                stir_speed="600 RPM",
            ),
            Filter(
                vessel=self.reaction_vessel,
                filtrate_vessel=self.evaporation_vessel,
            ),
            Evaporate(vessel=self.evaporation_vessel)
        ]
        return steps, reagents
