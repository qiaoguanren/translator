"""
Test scaling in blueprints from XDL XML (not 'traditional' XDL1 blueprints)

Scaling will involve specifying units in 'unit / eq' for specific reagents in
blueprint steps.
The base_scale, that is the reference in which the blueprint procedure was
developed and amounts calculated from initially, will be specified in the
procedure node.

Using XDL context, those specific reagent properties will be
scaled according to the equivalence reference and amount.
"""
import os
from typing import Any, Dict, List, Tuple

import pytest

from xdl import XDL
from xdl.blueprints import Blueprint
from xdl.context import Context

from .blueprint_fixtures import flatten_steps

try:
    from chemputerxdl import ChemputerPlatform
except ModuleNotFoundError:
    pass

HERE = os.path.abspath(os.path.dirname(__file__))
FILES = os.path.join(HERE, "..", "..", "files")


@pytest.fixture
def mitsunobu_scaling_props() -> List[Tuple[str, Dict[str, Any]]]:
    """List of final steps that will be spawned from 'Mitsunobu_blueprint.xdl'
    and their final props.

    Returns:
        List[Tuple[str, Dict[str, Any]]]: list of step name tuples and their
            associated props and values.
    """
    return [
        (
            "SetStirRate",
            {
                "stir_speed": 250.0,
            },
        ),
        (
            "SetStirRate",
            {
                "stir_speed": 250.0,
            },
        ),
        (
            "SetStirRate",
            {
                "stir_speed": 250.0,
            },
        ),
        ("Cyclic_Mitsunobu", {"id": "Cyclic_Mitsunobu"}),
        (
            "Add",
            {
                "reagent": "PPh3",
                "vessel": "reactor",
                "amount": "20 mg /eq",
                "mass": 0.0014,
                "volume": None,
            },
        ),
        (
            "Add",
            {
                "reagent": "Z-Hyp-OH",
                "vessel": "reactor",
                "amount": "1 eq",
                "mass": 0.9284,
                "volume": None,
            },
        ),
        (
            "Dissolve",
            {
                "vessel": "reactor",
                "solvent": "THF",
                "volume": 0.35,
                "time": 60,
            },
        ),
        (
            "Dissolve",
            {
                "vessel": "DIAD_vial",
                "solvent": "THF",
                "volume": 0.14,
                "time": 60,
            },
        ),
        (
            "HeatChillToTemp",
            {
                "vessel": "reactor",
                "temp": 0,
                "stir": True,
            },
        ),
        (
            "Transfer",
            {
                "from_vessel": "DIAD_vial",
                "to_vessel": "reactor",
                "volume": 0.42,
                "time": 600,
                "rinsing_volume": 1,
                "rinsing_repeats": 3,
                "rinse_withdrawal_excess": 0,
            },
        ),
        (
            "ResetHandling",
            {
                "solvent": "THF",
            },
        ),
        (
            "ResetHandling",
            {
                "solvent": "diethyl ether",
            },
        ),
        (
            "HeatChill",
            {
                "vessel": "reactor",
                "temp": 25,
                "time": 8 * 60 * 60,
                "stir": True,
            },
        ),
        (
            "Evaporate",
            {
                "vessel": "reactor",
                "temp": 45,
                "time": 60 * 60,
                "pressure": 50,
                "mode": "auto",
            },
        ),
        (
            "Precipitate",
            {
                "vessel": "reactor",
                "reagent": "diethyl ether",
                "volume": 0.7,
            },
        ),
        (
            "Dissolve",
            {
                "vessel": "reactor",
                "solvent": "diethyl ether",
                "volume": 1.4,
                "time": 300,
            },
        ),
        (
            "Transfer",
            {
                "from_vessel": "reactor",
                "to_vessel": "rotavap",
                "rinsing_volume": 20,
                "rinsing_repeats": 3,
                "rinse_withdrawal_excess": 0,
                "volume": 100,
            },
        ),
        (
            "ResetHandling",
            {
                "solvent": "diethyl ether",
            },
        ),
        (
            "Evaporate",
            {
                "vessel": "rotavap",
                "time": 30 * 60,
            },
        ),
        (
            "Dry",
            {
                "vessel": "rotavap",
                "time": 30 * 60,
            },
        ),
        (
            "ResetHandling",
            {
                "solvent": "methanol",
            },
        ),
    ]


@pytest.mark.chemputer
def test_blueprint_scaling(mitsunobu_scaling_props):
    xdl_file = os.path.join(FILES, "Mitsunobu_blueprint_scaled_equivalents.xdl")
    x = XDL(xdl_file, platform=ChemputerPlatform)
    graph_file = os.path.join(FILES, "Mitsunobu_graph.json")

    x.prepare_for_execution(
        graph_file, interactive=False, equiv_reference="Z-Hyp-OH", equiv_amount="1 g"
    )

    # check blueprint base scale, equiv_reference, equiv_amount and equiv_moles
    # are correct for blueprints steps and non-blueprint steps
    all_steps = flatten_steps(x.steps)
    for s in all_steps:
        if isinstance(s.context.xdl(), Blueprint):
            # step within inside blueprint
            assert s.context._base_scale == 0.05
            assert s.context._reference_reagent.name == "PPh3"
            assert s.context.equiv_amount == "3.5 mmol"
        else:
            # step within main procedure
            assert s.context._base_scale is None
            assert s.context._reference_reagent.name == "Z-Hyp-OH"
            assert s.context.equiv_amount == "1 g"

    # check all volume and masses are correct for all steps
    for i, (step_name, props) in enumerate(mitsunobu_scaling_props):
        step = all_steps[i]
        assert step.name == step_name

        assert type(step.context) == Context

        for prop, prop_value in props.items():
            step_value = getattr(step, prop)
            if type(step_value) == float:
                step_value = round(step_value, 4)

            if step.name in ["Dissolve", "Precipitate"] and prop == "volume":
                # This list has one entry.
                add_step = [s for s in step.steps if s.name == "Add"][0]
                step_value = round(add_step.volume, 4)

            if step.name == "Transfer" and prop == "volume":
                # Because of Volume splitting in Transfer, it's possible to have
                # two CMove steps in Transfer, in which case we take the latter.
                cmove_step = [s for s in step.steps if s.name == "CMove"][-1]
                step_value = round(cmove_step.volume, 4)

            assert step_value == prop_value
