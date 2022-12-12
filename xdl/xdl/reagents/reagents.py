from typing import List
from ..utils.xdl_base import XDLBase
from ..utils.prop_limits import TEMP_PROP_LIMIT, VOLUME_PROP_LIMIT, PropLimit

VALID_REAGENT_ROLES = [
    'catalyst',
    'reagent',
    'solvent',
    'substrate',
]

class Reagent(XDLBase):
    """Base reagent class.

    Args:
        id (str): Unique identifier containing only letters, numbers and _
        clean_type (str): 'organic' or 'aqueous'. Used by XDLExecutor to decide
            what solvent to use in CleanBackbone steps.
        cas (int, optional): Defaults to None. CAS number of reagent as int.
        use_for_cleaning (bool, optional): Defaults to False. Specifies whether
            reagent can be used as a cleaning solvent. If the reagent is
            recognised as a common solvent setting this property to False will
            NOT stop it being used for cleaning.
        stir (bool, optional): Defaults to False. Specifies whether reagent
            flask should be stirred continuously.
        temp (float, optional): Defaults to None. Specifies temperature (in
            °C) to keep reagent flask at.
        role (str, optional): Defaults to None. Specifies reagent role. NOTE:
            must be a valid reagent role if specified (catalyst, reagent,
            solvent, substrate).
        last_minute_addition (str, optional): Defaults to None. Name of reagent
            that must be added to reagent flask immediately prior to addition.
        last_minute_addition_volume (float, optional): Defaults to None. Volume
            of last minute addition.
        preserve (bool, optional): Defaults to False. True if reagent is
            expensive and should be preserved when possible; False if not.
        incompatible_reagents (list, optional): Defaults to None. List of
            reagents that are incompatible with this reagent and should never
            be mixed in the backbone.
        is_base (bool, optional): Defaults to False. Specifies whether reagent
            is a base. If True, more thorough backbone cleaning will be carried
            out after addition of this reagent.
    """

    PROP_TYPES = {
        'id': str,
        'cas': int,
        'inchi': str,
        'role': str,
        'cleaning_solvent': str,
        'use_for_cleaning': bool,
        'stir': bool,
        'temp': float,
        'last_minute_addition': str,
        'last_minute_addition_volume': float,
        'preserve': bool,
        'incompatible_reagents': List[str],
        'is_base': bool
    }

    DEFAULT_PROPS = {
        'is_base': False,
        'cleaning_solvent': None,
        'use_for_cleaning': False,
        'stir': False,
        'cas': None,
        'temp': None,
        'role': None,
        'last_minute_addition': None,
        'last_minute_addition_volume': None,
        'preserve': False,
        'incompatible_reagents': None,
    }

    PROP_LIMITS = {
        'temp': TEMP_PROP_LIMIT,
        'last_minute_addition_volume': VOLUME_PROP_LIMIT,
        'role': PropLimit(
            enum=[
                'reagent',
                'solvent',
                'substrate',
                'catalyst',
                'base',
                'acid',
                'activating-agent'
            ]
        )
    }

    def __init__(
        self,
        id: str,
        cleaning_solvent: str = 'default',
        use_for_cleaning: str = 'default',
        stir: bool = 'default',
        cas: int = 'default',
        temp: float = 'default',
        role: str = 'default',
        last_minute_addition: str = 'default',
        last_minute_addition_volume: float = 'default',
        preserve: bool = 'default',
        incompatible_reagents: List[str] = 'default',
        is_base: bool = 'default',
        inchi: str = '',
    ) -> None:
        super().__init__(locals())
