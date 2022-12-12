import pytest
from xdl.errors import (
    XDLUndeclaredAlwaysWriteError,
    XDLUndeclaredDefaultPropError,
    XDLUndeclaredPropLimitError,
    XDLUndeclaredInternalPropError
)
from xdl.steps import AbstractStep
from xdl.utils.prop_limits import ROTATION_SPEED_PROP_LIMIT

class TestUndeclaredDefaultProp(AbstractStep):

    __test__ = False

    PROP_TYPES = {
        'volume': float
    }

    DEFAULT_PROPS = {
        'volume': '15 mL',
        'stir': True
    }

    def __init__(self):
        super().__init__(locals())

    def get_steps(self):
        return []

class TestUndeclaredInternalProp(AbstractStep):

    __test__ = False

    PROP_TYPES = {
        'volume': float
    }

    DEFAULT_PROPS = {
        'volume': '15 mL'
    }

    INTERNAL_PROPS = [
        'stir'
    ]

    def __init__(self):
        super().__init__(locals())

    def get_steps(self):
        return []

class TestUndeclaredAlwaysWrite(AbstractStep):

    __test__ = False

    PROP_TYPES = {
        'volume': float
    }

    DEFAULT_PROPS = {
        'volume': '15 mL'
    }

    ALWAYS_WRITE = [
        'stir'
    ]

    def __init__(self):
        super().__init__(locals())

    def get_steps(self):
        return []

class TestUndeclaredPropLimit(AbstractStep):

    __test__ = False

    PROP_TYPES = {
        'volume': float
    }

    DEFAULT_PROPS = {
        'volume': '15 mL'
    }

    PROP_LIMITS = {
        'stir_speed': ROTATION_SPEED_PROP_LIMIT
    }

    def __init__(self):
        super().__init__(locals())

    def get_steps(self):
        return []

@pytest.mark.unit
def test_undeclared_default_props():
    """Test error raised if default prop specified that isn't in PROP_TYPES."""
    with pytest.raises(XDLUndeclaredDefaultPropError):
        TestUndeclaredDefaultProp()

@pytest.mark.unit
def test_undeclared_prop_limits():
    """Test error raised if prop limit specified that isn't in PROP_TYPES."""
    with pytest.raises(XDLUndeclaredPropLimitError):
        TestUndeclaredPropLimit()

@pytest.mark.unit
def test_undeclared_internal_props():
    """Test error raised if internal prop specified that isn't in PROP_TYPES."""
    with pytest.raises(XDLUndeclaredInternalPropError):
        TestUndeclaredInternalProp()

@pytest.mark.unit
def test_undeclared_always_write():
    """Test error raised if always write specified that isn't in PROP_TYPES."""
    with pytest.raises(XDLUndeclaredAlwaysWriteError):
        TestUndeclaredAlwaysWrite()
