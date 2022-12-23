import os
import random
from typing import Callable, Union

import pytest

from xdl import XDL
from xdl.errors import XDLEquivReferenceNotInReagents, XDLInvalidEquivalentsInput
from xdl.reagents import Reagent

try:
    from chemputerxdl import ChemputerPlatform
    from chemputerxdl.steps import Add, AddSolid, Confirm
except ModuleNotFoundError:
    pass

HERE = os.path.abspath(os.path.dirname(__file__))
FILES = os.path.join(HERE, "..", "..", "files")
BIGRIG = os.path.join(FILES, "bigrig.json")

#  N equivalents used in each of the Add steps - from 'add_equivalents.xdl'
#  file
ADD_EQUIVALENTS = (12, 2.9, 1)

#  number of moles to use in equiv_amount in each round of testing
MOLES_IN_EQUIV = (0.1, 3.3, 4)


@pytest.fixture
def full_equivalents_test() -> Callable:
    """Generates testing function for iterating through all available reagents
    in source_xdl, using each as a reference reagent with specified equivalent
    amount (in moles) expressed in units of 'g' or 'mol'.

    Args:
        source_xdl (XDL): XDL object.

    Returns:
        Callable: ```run_full_test``` function, with args: `n_moles`, `units`.
    """

    def run_full_test(n_moles: float, units: Union[str, str]):
        """Iterates through all available reagents in XDL object, using each
        as a reference reagent with 1 equivalent being equal to n_moles.

        Args:
            n_moles (float): number of moles in 1 equivalent.
            units (Union[Literal['g', 'mol']): specifies units the equivalent
                is specified in - 'mol' for number of moles directly, or 'g'
                for the mass of n_moles (in g).
        """
        assert units in ["g", "mol"]

        equiv_amount = n_moles

        source_xdl = XDL(
            os.path.join(FILES, "add_equivalents.xdl"), platform=ChemputerPlatform
        )

        #  for each reagent, use it as an equivalent and run appropriate tests
        for reagent in source_xdl.reagents:

            #  make sure to use correct units for equivalent amount
            if units == "g":
                equiv_amount = moles_to_mass(n_moles=n_moles, reagent=reagent)

            reagent_xdl = XDL(
                os.path.join(FILES, "add_equivalents.xdl"), platform=ChemputerPlatform
            )

            #  prepare for execution using current reagent as reference,
            #  n_moles or mass of n_moles as equivalent amount
            test_xdl = generate_test_xdl(
                source_xdl=reagent_xdl,
                equiv_ref=reagent.name,
                equiv_amount=equiv_amount,
                equiv_units=units,
            )

            assert hasattr(test_xdl, "context")

            #  get all Add, AddSolid steps
            add_steps = [s for s in test_xdl.steps if type(s) in [Add, AddSolid]]

            #  test each Add, AddSolid step to ensure final volume / mass is
            #  correct
            for step in add_steps:
                check_single_step(test_xdl=test_xdl, step=step, n_moles=n_moles)

            add_solid_steps = [s for s in add_steps if s.reagent_solid]
            assert len(add_solid_steps) == 1
            assert len(add_solid_steps[0].steps) == 1
            assert add_solid_steps[0].steps[0].name == "Confirm"

    return run_full_test


@pytest.mark.chemputer
def test_all_equivalents(full_equivalents_test: Callable):
    """Test all reagents in source_xdl as reference reagents, using every
    possible combination of 1 eq == n_moles for n_moles in MOLES_IN_EQUIV.

    Args:
        full_equivalents_test (Callable): ```run_full_test``` function.
    """

    #  expressed as mass ('g') or moles ('mol'), iterate through each avaialble
    #  reagent in source_xdl and define as reference reagent with 1 equivalent
    #  == n_moles
    for unit in ["g", "mol"]:
        for n_moles in MOLES_IN_EQUIV:
            full_equivalents_test(n_moles=n_moles, units=unit)


@pytest.mark.chemputer
def test_invalid_reagent_ref():
    """Tests whether correct error is range when invalid reagent is given
    as reference in ```prepare_for_execution``` method.

    Args:
        source_xdl (XDL): XDL object.
    """
    invalid_reagents = ["benzene", "buckfast", "MD2020", "ether net"]

    for reagent in invalid_reagents:

        for unit in ["mol", "g"]:
            for _ in range(10):
                source_xdl = XDL(
                    os.path.join(FILES, "add_equivalents.xdl"),
                    platform=ChemputerPlatform,
                )
                error_str = (
                    f"Equivalent reference {reagent} does not map to any"
                    " reagents. Either update Reagents section of XDL or choose"
                    " one of the following reagents as an equivalent"
                    " reference:\n"
                    f"{source_xdl.reagents}."
                )
                with pytest.raises(XDLEquivReferenceNotInReagents, match=error_str):
                    generate_test_xdl(
                        source_xdl=source_xdl,
                        equiv_ref=reagent,
                        equiv_amount=f"{random.randint(1, 50)}",  # noqa: DUO102 # nosec B311
                        equiv_units=unit,
                    )


@pytest.mark.chemputer
def test_invalid_equivalents_input():
    # make sure errors are raised if equiv_amount and equiv_reference
    # are not both defined
    with pytest.raises(XDLInvalidEquivalentsInput):

        source_xdl = XDL(
            os.path.join(FILES, "add_equivalents.xdl"), platform=ChemputerPlatform
        )

        source_xdl.prepare_for_execution(equiv_reference="acetonitrile_water")

    with pytest.raises(XDLInvalidEquivalentsInput):

        source_xdl = XDL(
            os.path.join(FILES, "add_equivalents.xdl"), platform=ChemputerPlatform
        )

        source_xdl.prepare_for_execution(equiv_amount="100 mL")


def check_single_step(test_xdl: XDL, step: Add, n_moles: float):
    """Test a single Add or AddSolid step to ensure the final volume or mass
    is calculated correctly from equivalent amount.

    Args:
        _xdl (XDL): compiled XDL object.
        step (Add): add step to test.
        n_moles (float): number of moles in 1 equivalent.
    """

    assert hasattr(step, "context")

    #  use this to lookup correct prop to test and test functions for final
    #  value of said prop
    solid = True if step.reagent_solid else False

    #  used to lookup conversion for theoretical value of volume (for Add step)
    #  or mass (for AddSolid step) as calculated from equivalents
    theoretical_adds = {True: moles_to_mass, False: moles_to_volume}

    #  used to lookup relevant prop for step (step.volume and step.mass for
    #  Add, AddSolid steps, respectively)
    relevant_attrs = {True: "mass", False: "volume"}

    #  check number of target moles == equivalent moles calculated in step
    assert step.amount_units == "equivalents"
    assert round(step.context._equiv_moles, 12) == n_moles

    #  get reagent to be added in step, ensure step has fetched correct Reagent
    #  object (NOTE: this is NOT the reference reagent, but the reagent to
    #  be added)
    added_reagent = [r for r in test_xdl.reagents if r.name == step.reagent][0]
    assert added_reagent == step._reagent_object

    #  get the theoretical correct value of step.mass (AddSolid) or
    #  step.volume (Add)
    desired_value = theoretical_adds[solid](
        n_moles=n_moles * step.final_amount, reagent=added_reagent
    )

    #  get final value of step.mass (AddSolid) or step.volume (Add)
    observed_value = getattr(step, relevant_attrs[solid])

    #  make sure observed and ideal values are identical, minus weird rounding
    #  issue with floats
    assert round(observed_value, 12) == round(desired_value, 12)

    if solid:
        assert [type(s) for s in step.steps] == [Confirm]


def generate_test_xdl(
    source_xdl: XDL, equiv_ref: str, equiv_amount: float, equiv_units: str
) -> XDL:
    """Compile and return a test XDL object with equivalents.

    Args:
        source_xdl (XDL): XDL.
        equiv_ref (str): name of equivalent reference reagent.
        equiv_amount (float): equivalent amount.
        equiv_units (str): units of equivalent amount ('mol' or 'g').

    Returns:
        XDL: compiled XDL object.
    """
    source_xdl.prepare_for_execution(
        graph_file=BIGRIG,
        interactive=False,
        equiv_reference=equiv_ref,
        equiv_amount=f"{equiv_amount} {equiv_units}",
    )
    return source_xdl


def moles_to_mass(n_moles: float, reagent: Reagent) -> float:
    """Takes the number of moles (n_moles) in 1 equivalent of reference Reagent
    object and returns the corresponding mass of n_moles. To be used in
    setting ```equiv_amount``` in method ```prepare_for_execution```.

    Args:
        n_moles (float): number of moles in 1 equivalent of reference reagent.
        reagent (Reagent): XDL Reagent object.

    Returns:
        float: mass (in g) of n_moles.
    """
    #  reagent has defined molecular weight - use this to work out mass in 1
    #  equivalent
    if reagent.molecular_weight:
        return n_moles * reagent.molecular_weight

    #  reagent does not have defined molecular weight, so work out mass in 1
    #  1 equivalent from density and concentration
    concentration = reagent.concentration / 1000  # units = mol mL-1
    density = reagent.density  # units = g mL-1

    #  concentration -> volume
    #  get volume (in mL) from concentration (units = mol/L)
    volume = n_moles / concentration

    #  volume -> mass
    #  mass for 1 equivalent (in g) == density (g/mL) * number of mL in 1
    #  equivalent
    return volume * density


def moles_to_volume(n_moles: float, reagent: Reagent) -> float:
    """Converts number of moles to volume for a given reagent.

    Args:
        n_moles (float): number of moles (mol)
        reagent (Reagent): Reagent object.

    Returns:
        float: volume of reagent stock that contains exactly n_moles of
            reagent.
    """
    if reagent.concentration:  # units = mol L-1
        return n_moles / (reagent.concentration / 1000)

    density = reagent.density  # g mL-1
    molecular_weight = reagent.molecular_weight  # g mol-1

    # 1. n_moles to g:
    mass = molecular_weight * n_moles

    #  2. mass to volume
    volume = mass / density

    return volume
