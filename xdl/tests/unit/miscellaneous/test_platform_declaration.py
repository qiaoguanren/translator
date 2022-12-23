import json

import pytest

from xdl.platforms.placeholder import PlaceholderPlatform


@pytest.mark.unit
def test_platform_declaration():
    """Test platform declaration generation runs without error, and can be saved
    to JSON file (ChemifyAPI needs this functionality).
    """
    return json.dumps(PlaceholderPlatform().declaration)
