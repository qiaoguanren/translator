import os
import shutil

import pytest

from xdl import XDL
from xdl.errors import XDLInvalidSaveFormatError
from xdl.readwrite.xml_generator import xdl_to_xml_string

try:
    from chemputerxdl import ChemputerPlatform
except ModuleNotFoundError:
    pass


HERE = os.path.abspath(os.path.dirname(__file__))
INTEGRATION_FOLDER = os.path.join(HERE, "..", "..", "files")
UNIT_FOLDER = os.path.join(HERE, "..", "..", "files")
TEST_OUTPUT = os.path.join(HERE, "test_output")
os.makedirs(TEST_OUTPUT, exist_ok=True)


def compare_xdls(xdl1, xdl2):
    for i, step in enumerate(xdl1.steps):
        assert step.name == xdl2.steps[i].name
        for prop, val in step.properties.items():
            if prop != "context":
                if prop not in step.INTERNAL_PROPS and prop != "children":
                    assert val == xdl2.steps[i].properties[prop]


@pytest.mark.chemputer
def test_readwrite():
    for f in os.listdir(INTEGRATION_FOLDER):
        if f.endswith(".xdl") and (f.startswith("orgsyn") or f.startswith("lidocaine")):
            f_path = os.path.join(INTEGRATION_FOLDER, f)
            if (not f.startswith("AlkylFluor")) and (not f.startswith("Mitsunobu")):
                # AlkylFluor weird as writes internal props
                x = XDL(f_path, platform=ChemputerPlatform)
                os.makedirs("test_output", exist_ok=True)
                save_xml_path = os.path.join("test_output", f)
                save_json_path = os.path.join("test_output", f[:-3] + "json")
                x.save(save_xml_path)
                x.save(save_json_path, file_format="json")
                x_xml = XDL(save_xml_path, platform=ChemputerPlatform)
                x_json = XDL(save_json_path, platform=ChemputerPlatform)
                shutil.rmtree("test_output")
                compare_xdls(x_xml, x_json)
                compare_xdls(x_json, x)
                compare_xdls(x, x_xml)

                # try to save as an unsupported format
                with pytest.raises(XDLInvalidSaveFormatError):
                    x.save(save_xml_path, file_format="png")


@pytest.mark.chemputer
def test_readwrite_procedure_sections():
    xdl_f = os.path.join(UNIT_FOLDER, "procedure-sections.xdl")
    x1 = XDL(xdl_f, platform=ChemputerPlatform)
    output_file = os.path.join(HERE, "test_output", "procedure-section.xdl")
    x1.save(output_file)
    x2 = XDL(output_file, platform=ChemputerPlatform)
    compare_xdls(x1, x2)
    for x1_section, x2_section in zip(x1.sections.values(), x2.sections.values()):
        assert len(x1_section) == len(x2_section) > 0


@pytest.mark.chemputer
def test_readwrite_procedure_sections_json():
    xdl_f = os.path.join(UNIT_FOLDER, "procedure-sections.xdl")
    x1 = XDL(xdl_f, platform=ChemputerPlatform)
    output_file = os.path.join(HERE, "test_output", "procedure-section.json")
    x1.save(output_file, file_format="json")
    x2 = XDL(output_file, platform=ChemputerPlatform)
    compare_xdls(x1, x2)
    for x1_section, x2_section in zip(x1.sections.values(), x2.sections.values()):
        assert len(x1_section) == len(x2_section) > 0


@pytest.mark.chemputer
def test_readwrite_metadata():
    """Test ``<Metadata />`` section can be loaded and saved correctly."""
    # Test load
    xdl_f = os.path.join(UNIT_FOLDER, "metadata.xdl")
    x1 = XDL(xdl_f, platform=ChemputerPlatform)
    assert x1.metadata.product == "lidocaine"

    # Test XML save and reload
    output_file = os.path.join(HERE, "test_output", "metadata.xdl")
    x1.save(output_file)
    x2 = XDL(output_file, platform=ChemputerPlatform)
    assert x2.metadata.product == "lidocaine"

    # Test JSON save and reload
    output_file = os.path.join(HERE, "test_output", "metadata.json")
    x2.save(output_file, file_format="json")
    x3 = XDL(output_file, platform=ChemputerPlatform)
    assert x3.metadata.product == "lidocaine"


@pytest.mark.chemputer
def test_context_removal():
    """Test 'context' is not present in the resultant XML"""

    for f in os.listdir(INTEGRATION_FOLDER):
        # Skip non-xdl files and the AlkylFluor one
        # if not f.endswith(".xdl") or f.startswith("AlkylFluor"):
        #     continue

        if (f.startswith("orgsyn") or f.startswith("lidocaine")) and f.endswith("xdl"):
            # Load XDL
            filepath = os.path.join(INTEGRATION_FOLDER, f)
            x = XDL(filepath, platform=ChemputerPlatform)

            # Check does not contain the 'context' entry
            xml = xdl_to_xml_string(x)
            assert "context" not in xml
