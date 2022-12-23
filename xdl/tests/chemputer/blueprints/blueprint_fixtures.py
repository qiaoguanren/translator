"""Fixtures for XDL XML blueprints tests in test_blueprint_xdl_xml.py (i.e.
blueprints that can be declared directly in XDL XML files)
"""
from typing import Any, Dict, List, Tuple

from xdl.xdl import Context


def check_props(steps, prop_list: List[Tuple[str, Dict[str, Any]]]):
    """Given a xdl objects, iterates through steps and asserts that the step
    props match those in the equivalent step in the prop_list.

    Args:
        steps (List): List of XDL steps that have been prepared for execution.
        prop_list (List[Tuple[str, Dict[str, Any]]]): list of step name
            tuples and their associated props and values. Should be spawned from
            the same xdl file as the xdl_object.
    """
    for i, (step_name, props) in enumerate(prop_list):
        step = steps[i]

        assert step.name == step_name  # nosec B101

        assert type(step.context) == Context  # nosec B101

        for prop, prop_value in props.items():
            step_value = getattr(step, prop)
            if type(step_value) == float:
                step_value = round(step_value, 4)
            assert step_value == prop_value  # nosec B101


def flatten_steps(steps):
    """Flattens blueprint so that children steps appear in list of steps.

    Args:
        steps (List[Step]): list of XDL steps
    """

    all_steps = []

    for step in steps:
        all_steps.append(step)
        if hasattr(step, "children"):
            all_steps.extend(flatten_steps(step.steps))

    return all_steps


def parameter_resolution_props() -> List[Tuple[str, Dict[str, Any]]]:
    """List of final steps that will be spawned from 'parameter_resolution.xdl'
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
        # BLUEPRINT USE 1
        ("Cyclic_Mitsunobu", {"id": "Cyclic_Mitsunobu"}),
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
            "Add",
            {
                "reagent": "PPh3",
                "vessel": "reactor",
                "amount": "1.197 eq",
                "mass": 1.0989,
                "volume": None,
            },
        ),
        (
            "Dissolve",
            {
                "vessel": "reactor",
                "solvent": "THF",
                "volume": 5,
                "time": 10 * 60,
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
            "Dissolve",
            {
                "vessel": "reactor",
                "solvent": "diethyl ether",
                "volume": 10,
                "time": 300,
            },
        ),
        # BLUEPRINT USE 2 (double amount and volumes)
        ("Cyclic_Mitsunobu", {"id": "Cyclic_Mitsunobu"}),
        (
            "Add",
            {
                "reagent": "Z-Hyp-OH",
                "vessel": "reactor",
                "amount": "1 eq",
                "mass": 1.8568,
                "volume": None,
            },
        ),
        (
            "Add",
            {
                "reagent": "PPh3",
                "vessel": "reactor",
                "amount": "1.197 eq",
                "mass": 2.1977,
                "volume": None,
            },
        ),
        (
            "Dissolve",
            {
                "vessel": "reactor",
                "solvent": "THF",
                "volume": 10,
                "time": 10 * 60,
            },
        ),
        (
            "HeatChill",
            {
                "vessel": "reactor",
                "temp": 25,
                "time": 16 * 60 * 60,
                "stir": True,
            },
        ),
        (
            "Dissolve",
            {
                "vessel": "reactor",
                "solvent": "diethyl ether",
                "volume": 13,
                "time": 300,
            },
        ),
        ("Wait", {"time": 3 * 60}),
    ]


def mitsunobu_props() -> List[Tuple[str, Dict[str, Any]]]:
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
                "reagent": "Z-Hyp-OH",
                "vessel": "reactor",
                "amount": "1 eq",
                "mass": 0.9284,
                "volume": None,
            },
        ),
        (
            "Add",
            {
                "reagent": "PPh3",
                "vessel": "reactor",
                "amount": "1.197 eq",
                "mass": 1.0989,
                "volume": None,
            },
        ),
        (
            "Dissolve",
            {
                "vessel": "reactor",
                "solvent": "THF",
                "volume": 16.2,
                "time": 60,
            },
        ),
        (
            "Dissolve",
            {
                "vessel": "DIAD_vial",
                "solvent": "THF",
                "volume": 2,
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
                "volume": 100,
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
            "Dissolve",
            {
                "vessel": "reactor",
                "solvent": "diethyl ether",
                "volume": 20,
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
        ("ResetHandling", {"solvent": "diethyl ether"}),
        ("Evaporate", {"vessel": "rotavap", "time": 30 * 60}),
        ("Dry", {"vessel": "rotavap", "time": 30 * 60}),
        ("ResetHandling", {"solvent": "methanol"}),
        ("Repeat", {"repeats": 2}),
        ("Single_Add", {"id": "Single_Add"}),
        ("Add", {"vessel": "reactor", "reagent": "THF", "amount": "1 mL"}),
    ]


def mitsunobu_equivalence_props() -> List[Tuple[str, Dict[str, Any]]]:
    """List of final steps that will be spawned from
    'Mitsunobu_blueprint_equiv_references.xdl' and their final props.

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
                "reagent": "Z-Hyp-OH",
                "vessel": "reactor",
                "amount": "1 eq",
                "mass": 0.9284,
                "volume": None,
            },
        ),
        (
            "Add",
            {
                "reagent": "PPh3",
                "vessel": "reactor",
                "amount": "1.197 eq",
                "mass": 1.0989,
                "volume": None,
            },
        ),
        (
            "Dissolve",
            {
                "vessel": "reactor",
                "solvent": "THF",
                "volume": 16.2,
                "time": 60,
            },
        ),
        (
            "Dissolve",
            {
                "vessel": "DIAD_vial",
                "solvent": "THF",
                "volume": 2,
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
                "volume": 100,
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
            "Dissolve",
            {
                "vessel": "reactor",
                "solvent": "diethyl ether",
                "volume": 20,
                "time": 300,
            },
        ),
        # MITSUNOBU 2
        ("Cyclic_Mitsunobu", {"id": "Cyclic_Mitsunobu"}),
        (
            "Add",
            {
                "reagent": "Z-Hyp-OH",
                "vessel": "reactor",
                "amount": "1 eq",
                "mass": 1.0113,
                "volume": None,
            },
        ),
        (
            "Add",
            {
                "reagent": "PPh3",
                "vessel": "reactor",
                "amount": "1.197 eq",
                "mass": 1.197,
                "volume": None,
            },
        ),
        (
            "Dissolve",
            {
                "vessel": "reactor",
                "solvent": "THF",
                "volume": 16.2,
                "time": 60,
            },
        ),
        (
            "Dissolve",
            {
                "vessel": "DIAD_vial",
                "solvent": "THF",
                "volume": 2,
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
                "volume": 100,
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
            "Dissolve",
            {
                "vessel": "reactor",
                "solvent": "diethyl ether",
                "volume": 20,
                "time": 300,
            },
        ),
        # standard steps
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
        ("ResetHandling", {"solvent": "diethyl ether"}),
        ("Evaporate", {"vessel": "rotavap", "time": 30 * 60}),
        ("Dry", {"vessel": "rotavap", "time": 30 * 60}),
        ("ResetHandling", {"solvent": "methanol"}),
        (
            "Add",
            {
                "reagent": "PPh3",
                "vessel": "reactor",
                "amount": "1 eq",
                "mass": 1,
                "volume": None,
            },
        ),
    ]


def simple_blueprint_props() -> List[Tuple[str, Dict[str, Any]]]:
    """List of final steps that will be spawned from
    'simple_blueprint_no_equivs.xdl' and their final props.

    Returns:
        List[Tuple[str, Dict[str, Any]]]: list of step name tuples and their
            associated props and values.
    """
    return [
        ("Add_Solid", {"id": "Add_Solid"}),
        (
            "Add",
            {
                "reagent": "histidine",
                "vessel": "reactor_01",
                "amount": "1 g",
                "mass": 1,
                "volume": None,
            },
        ),
        (
            "Add",
            {
                "reagent": "histidine",
                "vessel": "reactor_02",
                "amount": "0.25 g",
                "mass": 0.25,
                "volume": None,
            },
        ),
        (
            "Add",
            {
                "reagent": "histidine",
                "vessel": "reactor_03",
                "amount": "0.75 g",
                "mass": 0.75,
                "volume": None,
            },
        ),
        (
            "Wait",
            {
                "time": 30,
            },
        ),
        ("Add_Liquids", {"id": "Add_Liquids"}),
        (
            "Add",
            {
                "reagent": "water",
                "vessel": "reactor_01",
                "amount": None,
                "mass": None,
                "volume": 2,
            },
        ),
        (
            "Add",
            {
                "reagent": "acetonitrile_water",
                "vessel": "reactor_02",
                "amount": "2.6 mL",
                "mass": None,
                "volume": 2.6,
            },
        ),
        (
            "Add",
            {
                "reagent": "water",
                "vessel": "reactor_01",
                "amount": None,
                "mass": None,
                "volume": 1,
            },
        ),
        (
            "Wait",
            {
                "time": 30,
            },
        ),
        (
            "Add",
            {
                "reagent": "water",
                "vessel": "reactor_01",
                "amount": None,
                "mass": None,
                "volume": 2,
            },
        ),
    ]


def transfer_liquids_props() -> List[Tuple[str, Dict[str, Any]]]:
    """List of final steps and corresponding props that will be spawned from
    'simple_blueprint_ALC3_with_params.xdl'transfer liquid blueprint only.

    Returns:
        List[Tuple[str, Dict[str, Any]]]: list of step name tuples and their
            associated props and values.
    """
    return [
        (
            "CMove",
            {
                "from_vessel": "reactor_01",
                "to_vessel": "reactor_03",
                "volume": 1,
            },
        ),
        (
            "CMove",
            {
                "from_vessel": "reactor_02",
                "to_vessel": "reactor_03",
                "volume": 1,
            },
        ),
        (
            "Add",
            {
                "reagent": "water",
                "vessel": "reactor_01",
                "amount": None,
                "mass": None,
                "volume": 1,
            },
        ),
        (
            "Add",
            {
                "reagent": "water",
                "vessel": "reactor_02",
                "amount": None,
                "mass": None,
                "volume": 1,
            },
        ),
        (
            "Add",
            {
                "reagent": "water",
                "vessel": "reactor_03",
                "amount": None,
                "mass": None,
                "volume": 1,
            },
        ),
        (
            "CMove",
            {
                "from_vessel": "reactor_03",
                "to_vessel": "reactor_01",
                "volume": 1,
            },
        ),
    ]
