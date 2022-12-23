from typing import Optional

from .utils.xdl_base import XDLBase


class Parameter(XDLBase):
    """This will be retired in future versions. Class for representing a given
    parameter.

    Args:
        id (str): ID for the component.
        parameter_type (str): Type of the parameter i.e. 'volume'
        min (str): minimum value for parameter.
        max (str): maximum value for parameter.
        default (str): default value for parameter.
    """

    PROP_TYPES = {
        "id": str,
        "parameter_type": str,
        "min": str,
        "max": str,
        "value": str,
    }

    DEFAULT_PROPS = {"parameter_type": None, "min": None, "max": None, "value": None}

    def __init__(
        self,
        id: str,  # noqa: A002
        value: str = None,
        parameter_type: Optional[str] = None,
        min: Optional[str] = None,  # noqa: A002
        max: Optional[str] = None,  # noqa: A002
        **kwargs,
    ) -> None:
        super().__init__(locals())
