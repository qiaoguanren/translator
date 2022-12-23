from __future__ import annotations

import xml.etree.ElementTree as ET  # noqa: DUO107,N817 # nosec B405
from collections import defaultdict
from pathlib import Path

import pytest

from xdl import XDL
from xdl.readwrite.utils import read_file

try:
    from chemputerxdl import ChemputerPlatform
    from ChemputerXDL.tests.utils import generic_chempiler_test
except ModuleNotFoundError:
    pass

CURRENT_FOLDER = Path(__file__).parent.absolute()
INTEGRATION_FOLDER = CURRENT_FOLDER / "../../files"
INTEGRATION_FOLDER_BASE_STEPS = INTEGRATION_FOLDER / "/base_steps/"

XDL_FS = list(Path(INTEGRATION_FOLDER).glob("*.xdl"))
XDL_FS_BS = list(Path(INTEGRATION_FOLDER_BASE_STEPS).glob("*.xdl"))


def tree_to_dict(tree: str) -> dict:
    d = {tree.tag: {} if tree.attrib else None}
    children = list(tree)
    if children:
        dd = defaultdict(list)
        for dc in map(tree_to_dict, children):
            for k, v in dc.items():
                dd[k].append(v)
        d = {tree.tag: {k: v for k, v in dd.items()}}
    if tree.attrib:
        d[tree.tag].update((k, v) for k, v in tree.attrib.items())
    if tree.text:
        text = tree.text.strip()
        if children or tree.attrib:
            if text:
                d[tree.tag]["#text"] = text
        else:
            d[tree.tag] = text
    return d


@pytest.mark.unit
def test_all_attributes():
    for xdl_file in XDL_FS:
        if not str(xdl_file).startswith("orgsyn") or str(xdl_file).startswith(
            "lidocaine"
        ):
            continue

        graph_f = xdl_file.with_suffix(".json")

        if not graph_f.exists():
            continue

        xdl_str = read_file(xdl_file)
        xdl_tree = ET.XML(xdl_str)
        xdl_dict = tree_to_dict(xdl_tree)["Synthesis"]

        x = XDL(str(xdl_file), platform=ChemputerPlatform)
        x.prepare_for_execution(str(graph_f), interactive=False)

        # check hardware
        for i, param in enumerate(x.hardware):
            for attr, attr_value in xdl_dict["Hardware"][0]["Component"][i].items():
                if attr == "type":
                    attr = "component_type"

                if "Chemputer" in attr_value:
                    attr_value = attr_value.split("Chemputer", 1)[1].lower()
                assert param.__getattr__(attr) == attr_value

        # check reagents
        for i, param in enumerate(x.reagents):
            for attr, attr_value in xdl_dict["Reagents"][0]["Reagent"][i].items():
                if attr in ["density", "concentration"]:
                    attr_value = float(attr_value.split(" ", 1)[0])
                if attr_value == "True":
                    attr_value = True
                if attr_value == "False":
                    attr_value = False
                assert param.__getattr__(attr) == attr_value

        # check metadata
        if xdl_dict["Metadata"]:
            for m in xdl_dict["Metadata"]:
                for attr, attr_value in m.items():
                    assert x.metadata.__getattr__(attr) == attr_value

        # check parameters
        if xdl_dict["Parameters"]:
            for i, param in enumerate(x.parameters):
                for attr, attr_value in xdl_dict["Parameters"][0]["Parameter"][
                    i
                ].items():
                    if attr == "type":
                        attr = "parameter_type"
                    assert param.__getattr__(attr) == attr_value


@pytest.mark.unit
def test_base_step_attribute():
    for xdl_file in XDL_FS_BS:
        graph_f = xdl_file.with_suffix(".json")
        x = XDL(str(xdl_file), platform=ChemputerPlatform)
        x.prepare_for_execution(str(graph_f), interactive=False)

        assert type(x.base_steps) is list
        assert len(x.base_steps) > 0

        generic_chempiler_test(xdl_file, graph_f)


@pytest.mark.chemputer
def test_parameter_dict_overwriting():
    """Test that parameter values are overwritting when Parameter dict is
    passed into XDL constructor and that new Parameters are created.
    """
    xdl_f = str(INTEGRATION_FOLDER / "DMP_with_parameters.xdl")

    x1 = XDL(xdl_f, platform=ChemputerPlatform)

    parameter_dict = [
        {
            "id": "acetic_anhydride_volume",
            "parameter_type": "volume",
            "min": "250 mL",
            "max": "350 mL",
            "value": "200 mL",
        },
        {
            "id": "dry_temperature_1",
            "parameter_type": "temperature",
            "min": "23°C",
            "max": "27°C",
            "value": "25.0°C",
        },
    ]

    for i, param in enumerate(x1.parameters):
        for prop, val in parameter_dict[i].items():
            assert param.properties[prop] == val

    x2 = XDL(
        xdl_f,
        platform=ChemputerPlatform,
        parameters={"dry_temperature_1": "35.0°C", "new_param": "new_value"},
    )

    parameter_dict_2 = [
        {
            "id": "acetic_anhydride_volume",
            "parameter_type": "volume",
            "min": "250 mL",
            "max": "350 mL",
            "value": "200 mL",
        },
        {
            "id": "dry_temperature_1",
            "parameter_type": "temperature",
            "min": "23°C",
            "max": "27°C",
            "value": "35.0°C",
        },
        {"id": "new_param", "value": "new_value"},
    ]

    for i, param in enumerate(x2.parameters):
        for prop, val in parameter_dict_2[i].items():
            assert param.properties[prop] == val

    dry_temp_step = [s for s in x2.steps if s.name == "Dry"][0]
    assert dry_temp_step.properties["temp"] == 35.0
