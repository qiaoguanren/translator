import os
import pytest

from xdl.blueprints import CrossCouplingBlueprint
from xdl.steps.placeholders import AddSolid

HERE = os.path.abspath(os.path.dirname(__file__))
os.makedirs(os.path.join(HERE, 'test_output'), exist_ok=True)

@pytest.mark.unit
def test_cross_coupling_blueprint():
    # Blueprint parameters
    catalyst = 'Pd(OAc)2'

    substrate = 'boronic acid'
    substrate_mol = 1
    substrate_molar_mass = 50

    halide = 'R-Cl'
    halide_molar_mass = 43

    base = 'K2CO3'
    base_molar_mass = 138.205

    # Create blueprint and build xdl
    bp = CrossCouplingBlueprint(
        catalyst=catalyst,

        substrate=substrate,
        substrate_mol=substrate_mol,
        substrate_molar_mass=substrate_molar_mass,

        halide=halide,
        halide_molar_mass=halide_molar_mass,

        base=base,
        base_molar_mass=base_molar_mass,
    )
    x = bp.build(save=os.path.join(HERE, 'test_output', 'cross-coupling.xdl'))

    # Verify xdl
    for step in x.steps:
        if type(step) == AddSolid:

            # Check halide mass calculated correctly
            if step.reagent == halide:
                assert step.mass == (
                    halide_molar_mass
                    * substrate_mol
                    * CrossCouplingBlueprint.halide_equivs
                )

            # Check base mass calculated correctly
            elif step.reagent == base:
                assert step.mass == (
                    base_molar_mass
                    * substrate_mol
                    * CrossCouplingBlueprint.base_equivs
                )

            # Check substrate mass calculated correctly
            elif step.reagent == substrate:
                assert step.mass == (
                    substrate_molar_mass
                    * substrate_mol
                )
