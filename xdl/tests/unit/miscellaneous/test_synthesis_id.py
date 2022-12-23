import pytest

from xdl.utils.misc import synthesis_id

INVALID_CHARACTERS = r"!#$%()*+,/;?@[]^`{|}~=><& " + "'\t\r\n\""
INVALID_FIRST_CHARACTERS = r"-.0123456789"
VALID_IDS = ["id1", "deprotection_2x", "i", "j12345678.9"]


@pytest.mark.unit
def test_synthesis_ids():
    """Test validation of synthesis id string in the synthesis_id() function."""
    # ids with invalid first character should raise ValueError
    for c in INVALID_FIRST_CHARACTERS + INVALID_CHARACTERS:
        with pytest.raises(ValueError):
            synthesis_id({"id": f"{c}invalid_ids"})

    # ids with invalid internal characters should raise ValueError
    for c in INVALID_CHARACTERS:
        with pytest.raises(ValueError):
            synthesis_id({"id": f"invalid_{c}_ids"})

    # Test valid ids are properly recognized
    for i in VALID_IDS:
        assert synthesis_id({"id": i}) == i

    # Test id is 'None' if no value is provided
    assert synthesis_id({}) is None
