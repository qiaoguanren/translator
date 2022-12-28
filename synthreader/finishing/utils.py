from typing import List, Any, Union

from ..words import AbstractReagentWord
from .constants import (
    DEFAULT_COLD_REAGENT_TEMP,
    DEFAULT_ICECOLD_REAGENT_TEMP,
    DEFAULT_WARM_REAGENT_TEMP,
    DEFAULT_HOT_REAGENT_TEMP,
)

def get_reagent_temp(reagent: AbstractReagentWord) -> Union[None, float]:
    """Get temperature that reagent should be at, if specified, otherwise
    return None.

    Args:
        reagent (AbstractReagentWord): Reagent to get temperature from.

    Returns:
        float: Temperature that reagent should be used at. If not specified
            returns None.
    """
    if reagent.temp != None:
        return str(reagent.temp)

    elif reagent.icecold:
        return DEFAULT_ICECOLD_REAGENT_TEMP

    elif reagent.cold:
        return DEFAULT_COLD_REAGENT_TEMP

    elif reagent.warm:
        return DEFAULT_WARM_REAGENT_TEMP

    elif reagent.hot:
        return DEFAULT_HOT_REAGENT_TEMP

    return None
