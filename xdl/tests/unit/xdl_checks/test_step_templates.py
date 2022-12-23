from typing import List

import pytest

from xdl.constants import REAGENT_PROP_TYPE, VESSEL_PROP_TYPE
from xdl.errors import (
    XDLStepTemplateInvalidDefaultPropError,
    XDLStepTemplateInvalidPropLimitError,
    XDLStepTemplateMissingDefaultPropError,
    XDLStepTemplateMissingPropError,
    XDLStepTemplateMissingPropLimitError,
    XDLStepTemplateNameError,
    XDLStepTemplatePropTypeError,
)
from xdl.steps.base_steps import Step
from xdl.steps.templates import AbstractAddStep
from xdl.utils.prop_limits import (
    ROTATION_SPEED_PROP_LIMIT,
    TIME_PROP_LIMIT,
    VOLUME_PROP_LIMIT,
)

add_params = {"reagent": "water", "vessel": "reactor", "volume": "15 mL"}


@pytest.mark.unit
def test_step_template_missing_prop_type():
    class Add(AbstractAddStep):
        PROP_TYPES = {
            "vessel": VESSEL_PROP_TYPE,
            "reagent": REAGENT_PROP_TYPE,
            "volume": float,
            "mass": float,
            # Missing time prop type
            "stir": bool,
            "stir_speed": float,
            "viscous": bool,
            "dropwise": bool,
            "purpose": str,
            "speed": float,
        }

        DEFAULT_PROPS = {
            "stir": False,
            "viscous": False,
            "time": None,
            "stir_speed": None,
            "dropwise": False,
            "purpose": None,
            "speed": 40,
        }

        PROP_LIMITS = {
            "volume": VOLUME_PROP_LIMIT,
            "time": TIME_PROP_LIMIT,
            "stir_speed": ROTATION_SPEED_PROP_LIMIT,
        }

        def __init__(
            self,
            vessel,
            reagent,
            volume,
            time="default",
            stir="default",
            stir_speed="default",
            viscous="default",
            dropwise="default",
            purpose="default",
            amount="default",
            **kwargs,
        ):
            super().__init__(locals())

        def get_steps(self) -> List[Step]:
            return []

    with pytest.raises(XDLStepTemplateMissingPropError):
        Add(**add_params)


@pytest.mark.unit
def test_step_template_incorrect_prop_type():
    class Add(AbstractAddStep):
        PROP_TYPES = {
            "vessel": VESSEL_PROP_TYPE,
            "reagent": REAGENT_PROP_TYPE,
            "mass": float,
            "volume": str,  # Incorrect volume prop type, should be float
            "time": float,
            "stir": bool,
            "stir_speed": float,
            "viscous": bool,
            "dropwise": bool,
            "purpose": str,
            "speed": float,
        }

        DEFAULT_PROPS = {
            "stir": False,
            "viscous": False,
            "time": None,
            "stir_speed": None,
            "dropwise": False,
            "purpose": None,
            "speed": 40,
        }

        PROP_LIMITS = {
            "volume": VOLUME_PROP_LIMIT,
            "time": TIME_PROP_LIMIT,
            "stir_speed": ROTATION_SPEED_PROP_LIMIT,
        }

        def __init__(
            self,
            vessel,
            reagent,
            volume,
            time="default",
            stir="default",
            stir_speed="default",
            viscous="default",
            dropwise="default",
            purpose="default",
            amount="default",
            **kwargs,
        ):
            super().__init__(locals())

        def get_steps(self) -> List[Step]:
            return []

    with pytest.raises(XDLStepTemplatePropTypeError):
        Add(**add_params)


@pytest.mark.unit
def test_step_template_missing_default_prop():
    class Add(AbstractAddStep):
        PROP_TYPES = {
            "vessel": VESSEL_PROP_TYPE,
            "reagent": REAGENT_PROP_TYPE,
            "volume": float,
            "mass": float,
            "time": float,
            "stir": bool,
            "stir_speed": float,
            "viscous": bool,
            "dropwise": bool,
            "purpose": str,
            "speed": float,
            "amount": str,
        }

        DEFAULT_PROPS = {
            # Missing stir default prop
            "viscous": False,
            "time": None,
            "stir_speed": None,
            "dropwise": False,
            "purpose": None,
            "speed": 40,
            "amount": None,
            "mass": None,
        }

        PROP_LIMITS = {
            "volume": VOLUME_PROP_LIMIT,
            "time": TIME_PROP_LIMIT,
            "stir_speed": ROTATION_SPEED_PROP_LIMIT,
        }

        def __init__(
            self,
            vessel,
            reagent,
            amount="default",
            volume="default",
            mass="default",
            time="default",
            stir="default",
            stir_speed="default",
            viscous="default",
            dropwise="default",
            purpose="default",
            **kwargs,
        ):
            super().__init__(locals())

        def get_steps(self) -> List[Step]:
            return []

    with pytest.raises(XDLStepTemplateMissingDefaultPropError):
        Add(**add_params)


@pytest.mark.unit
def test_step_template_invalid_default_prop():
    class Add(AbstractAddStep):
        PROP_TYPES = {
            "vessel": VESSEL_PROP_TYPE,
            "reagent": REAGENT_PROP_TYPE,
            "volume": float,
            "mass": float,
            "time": float,
            "stir": bool,
            "stir_speed": float,
            "viscous": bool,
            "dropwise": bool,
            "purpose": str,
            "speed": float,
            "amount": str,
        }

        DEFAULT_PROPS = {
            "stir": True,  # Should be False
            "viscous": False,
            "time": None,
            "stir_speed": None,
            "dropwise": False,
            "purpose": None,
            "speed": 40,
            "amount": None,
            "mass": None,
            "volume": None,
        }

        PROP_LIMITS = {
            "volume": VOLUME_PROP_LIMIT,
            "time": TIME_PROP_LIMIT,
            "stir_speed": ROTATION_SPEED_PROP_LIMIT,
        }

        def __init__(
            self,
            vessel,
            reagent,
            volume,
            time="default",
            stir="default",
            stir_speed="default",
            viscous="default",
            dropwise="default",
            purpose="default",
            amount="default",
            **kwargs,
        ):
            super().__init__(locals())

        def get_steps(self) -> List[Step]:
            return []

    with pytest.raises(XDLStepTemplateInvalidDefaultPropError):
        Add(**add_params)


@pytest.mark.unit
def test_step_template_missing_prop_limit():
    class Add(AbstractAddStep):
        PROP_TYPES = {
            "vessel": VESSEL_PROP_TYPE,
            "reagent": REAGENT_PROP_TYPE,
            "volume": float,
            "mass": float,
            "time": float,
            "stir": bool,
            "stir_speed": float,
            "viscous": bool,
            "dropwise": bool,
            "purpose": str,
            "speed": float,
            "amount": str,
        }

        DEFAULT_PROPS = {
            "stir": False,
            "viscous": False,
            "time": None,
            "stir_speed": None,
            "dropwise": False,
            "purpose": None,
            "speed": 40,
            "amount": None,
            "volume": None,
            "mass": None,
        }

        PROP_LIMITS = {
            # Missing volume prop limit
            "time": TIME_PROP_LIMIT,
            "stir_speed": ROTATION_SPEED_PROP_LIMIT,
        }

        def __init__(
            self,
            vessel,
            reagent,
            volume,
            time="default",
            stir="default",
            stir_speed="default",
            viscous="default",
            dropwise="default",
            purpose="default",
            **kwargs,
        ):
            super().__init__(locals())

        def get_steps(self) -> List[Step]:
            return []

    with pytest.raises(XDLStepTemplateMissingPropLimitError):
        Add(**add_params)


@pytest.mark.unit
def test_step_template_incorrect_prop_limit():
    class Add(AbstractAddStep):
        PROP_TYPES = {
            "vessel": VESSEL_PROP_TYPE,
            "reagent": REAGENT_PROP_TYPE,
            "volume": float,
            "time": float,
            "stir": bool,
            "stir_speed": float,
            "viscous": bool,
            "dropwise": bool,
            "purpose": str,
            "speed": float,
            "amount": str,
            "mass": float,
        }

        DEFAULT_PROPS = {
            "stir": False,
            "viscous": False,
            "time": None,
            "stir_speed": None,
            "dropwise": False,
            "purpose": None,
            "speed": 40,
            "amount": None,
            "volume": None,
            "mass": None,
        }

        PROP_LIMITS = {
            "volume": TIME_PROP_LIMIT,  # Wrong prop limit
            "time": TIME_PROP_LIMIT,
            "stir_speed": ROTATION_SPEED_PROP_LIMIT,
        }

        def __init__(
            self,
            vessel,
            reagent,
            volume,
            time="default",
            stir="default",
            stir_speed="default",
            viscous="default",
            dropwise="default",
            purpose="default",
            **kwargs,
        ):
            super().__init__(locals())

        def get_steps(self) -> List[Step]:
            return []

    with pytest.raises(XDLStepTemplateInvalidPropLimitError):
        Add(**add_params)


@pytest.mark.unit
def test_step_template_incorrect_name():
    class Madd(AbstractAddStep):
        PROP_TYPES = {
            "vessel": VESSEL_PROP_TYPE,
            "reagent": REAGENT_PROP_TYPE,
            "volume": float,
            "time": float,
            "stir": bool,
            "stir_speed": float,
            "viscous": bool,
            "dropwise": bool,
            "purpose": str,
            "speed": float,
        }

        DEFAULT_PROPS = {
            "stir": False,
            "viscous": False,
            "time": None,
            "stir_speed": None,
            "dropwise": False,
            "purpose": None,
            "speed": 40,
            "volume": None,
        }

        PROP_LIMITS = {
            "volume": VOLUME_PROP_LIMIT,
            "time": TIME_PROP_LIMIT,
            "stir_speed": ROTATION_SPEED_PROP_LIMIT,
        }

        def __init__(
            self,
            vessel,
            reagent,
            volume,
            time="default",
            stir="default",
            stir_speed="default",
            viscous="default",
            dropwise="default",
            purpose="default",
            **kwargs,
        ):
            super().__init__(locals())

        def get_steps(self) -> List[Step]:
            return []

    with pytest.raises(XDLStepTemplateNameError):
        Madd(**add_params)
