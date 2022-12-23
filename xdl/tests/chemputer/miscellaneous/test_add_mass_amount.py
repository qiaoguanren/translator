import os

import pytest

from xdl import XDL
from xdl.utils.sanitisation import convert_val_to_std_units

try:
    from chemputerxdl import ChemputerPlatform
    from chemputerxdl.steps import Add
except ModuleNotFoundError:
    pass

HERE = os.path.abspath(os.path.dirname(__file__))
FILES = os.path.join(HERE, "..", "..", "files")
BIGRIG = os.path.join(FILES, "bigrig.json")

#  Intended density, concentration and molecular weight for reagents in
#  `add_amount.xdl`
REAGENT_PROPS = {
    "ether": {
        "density": 2.6,  # g/mL
        "concentration": 56.435,  # mol/L
        "molecular_weight": 46.07,  # g/mol
    },
    "NaCl": {"solid": True, "molecular_weight": 58.443},  # g/mol
    "chloroacetyl chloride": {"density": 3},  # g/mL
    "water": {"concentration": 1, "molecular_weight": 18.0106},  # mol/L  # g/mol
}

#  reagent to be added in each step in `add_amount.xdl`
REAGENT_ADDITIONS = ("ether", "ether", "ether", "NaCl")

#  Intended molecular weight for solid Reagent
SOLID_REAGENT_MW = 58.443  # g/mol


@pytest.mark.chemputer
def test_add_amounts():
    """Tests Add step when using 'amount' prop to infer mass and volume
    indirectly.
    """
    x = XDL(os.path.join(FILES, "add_amount.xdl"), platform=ChemputerPlatform)
    x.prepare_for_execution(BIGRIG, testing=True)

    #  amounts to be added at each Add step and their units
    amounts = [(1.2, "g"), (2, "mol"), (None, None), (2, "mol"), (10, "g"), (1, "g")]

    #  masses to be added at each Add step and their units
    masses = [
        (None, None),
        (None, None),
        (68, "g"),
        (None, None),
        (None, None),
        (None, None),
    ]

    #  get Add steps
    add_steps = [s for s in x.steps if type(s) == Add]

    #  check Add steps have correct Reagent object
    for i, reagent_name in enumerate(REAGENT_ADDITIONS):

        #  get corresponding Add step
        step = add_steps[i]

        #  fetch name and properties for reagent to be added
        reagent_props = REAGENT_PROPS[reagent_name]

        #  check correct reagent is to be added
        assert step.reagent == reagent_name

        #  get Reagent object for target reagent
        reagent_object = step._reagent_object

        assert reagent_object == [r for r in x.reagents if r.name == step.reagent][0]

        #  check Reagent object has correct prop values
        for prop, val in reagent_props.items():
            val = convert_val_to_std_units(val)
            assert getattr(reagent_object, prop) == val

        #  get amount and / or mass specified in current Add step
        amount, mass = amounts[i], masses[i]

        #  get values needed to convert amount to mass and / or volume
        density = reagent_props.get("density")
        molecular_weight = reagent_props.get("molecular_weight")
        concentration = reagent_props.get("concentration")
        solid = reagent_props.get("solid")

        #  ensure amount to volume calculation has been done correctly based
        #  on amount specified
        if amount[0]:

            #  amount is in mass units, so use density to get final volume
            if amount[1] == "g":
                if density:
                    assert step.volume == amount[0] / density
                else:
                    assert molecular_weight is not None
                    assert type(molecular_weight) in [int, float]
                    if solid is None:
                        assert concentration is not None
                        assert type(concentration) in [int, float]

                        #  get theoretical volume:
                        #  g g-1 mol => mol. mol mol-1 mL => mL
                        theo_volume = (
                            (amount[0] / molecular_weight) / concentration
                        ) * 1000
                        assert step.volume == theo_volume
                    else:
                        assert step.volume is None
                        assert step.mass == step.amount == amount[1]

            #  amount is in mole units, so use reagent concentration to get
            #  final volume
            elif amount[1] == "mol":
                if solid is None:
                    assert concentration is not None and type(concentration) in [
                        int,
                        float,
                    ]
                    theo_volume = amount[0] / (concentration / 1000)
                    assert step.volume == theo_volume
                else:
                    assert step.volume is None
                    assert molecular_weight is not None and type(molecular_weight) in [
                        int,
                        float,
                    ]
                    assert step.mass == amount[0] * molecular_weight

        #  mass supplied directly, so use density to get final volume
        if mass[0]:
            assert density is not None and type(density) in [int, float]
            assert step.volume == mass[0] / density
