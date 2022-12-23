from typing import Optional

from .constants import REAGENT_PROP_TYPE
from .errors import XDLError
from .steps.templates import AbstractReagent
from .utils.prop_limits import (
    CONCENTRATION_PROP_LIMIT,
    DENSITY_PROP_LIMIT,
    MOLECULAR_FORMULA_PROP_LIMIT,
    MOLECULAR_WEIGHT_PROP_LIMIT,
    PERCENT_RANGE_PROP_LIMIT,
    TEMP_PROP_LIMIT,
)


class Reagent(AbstractReagent):
    """Class for representing a reagent used by a procedure.

    Args:
        name (str): Unique identifier containing only letters, numbers and _.
        inchi (str): Defaults to ``None``. IUPAC International Chemical
            Identifier (InChI) for reagent.
        clean_type (str): ``'organic'`` or ``'aqueous'``. Used to decide what
            type of solvent should be used to clean with after reagent has been
            used.
        cas (int): CAS number of reagent as ``int``.
        use_for_cleaning (bool): Defaults to ``False``. Specifies whether
            reagent can be used as a cleaning solvent. If the reagent is
            recognised as a common solvent setting this property to ``False``
            will NOT stop it being used for cleaning.
        stir (bool): Defaults to ``False``. Specifies whether reagent
            flask should be stirred continuously.
        temp (float): Defaults to ``None``. Specifies temperature (in
            °C) to keep reagent flask at.
        role (str): Defaults to ``None``. Specifies reagent role. NOTE:
            must be a valid reagent role if specified (catalyst, reagent,
            solvent, substrate).
        last_minute_addition (str): Defaults to ``None``. Name of reagent
            that must be added to reagent flask immediately prior to addition.
        last_minute_addition_volume (float): Defaults to ``None``. Volume
            of last minute addition.
        preserve (bool): Defaults to ``False``. ``True`` if reagent is
            expensive and should be preserved when possible; ``False`` if not.
        incompatible_reagents (List[str]): Defaults to ``None``. List of
            reagents that are incompatible with this reagent and should never
            be mixed in the backbone.
        is_base (bool): Defaults to ``False``. Specifies whether reagent
            is a base. If ``True``, more thorough backbone cleaning will be
            carried out after addition of this reagent.
        solid (bool): Defaults to ``False``. Specifies whether reagent is solid.
        molecular_formula (str): Defaults to ``None``. Molecular formula
            for reagent.
        molecular_weight (float): Defaults to ``None``. Molecular weight of
            reagent in g/mol (or units convertible to g / mol).
        density (float): Defaults to ``None``. Density of reagent in g / L (or
            units convertible to g/L).
        concentration (float): Defaults to ``None``. Concentration of reagent
            in mol/L (or units convertible to mol/L).
        atmosphere (str): Defaults to ``None``. Description of atmospheric
            conditions of reagent flask (e.g. 'under Argon').
        purity (float): Defaults to ``None``. Purity of reagent (in %).
        clean_with (str): Defaults to ``None``. Specify prefered reagent to
            use for cleaning after use of this reagent.
    """

    PROP_TYPES = {
        "name": str,
        "id": str,
        "inchi": str,
        "cas": int,
        "molecular_formula": str,
        "molecular_weight": float,
        "density": float,
        "concentration": float,
        "role": str,
        "preserve": bool,
        "use_for_cleaning": bool,
        "clean_with": REAGENT_PROP_TYPE,
        "stir": bool,
        "temp": float,
        "atmosphere": str,
        "purity": float,
        "solid": bool,
    }

    DEFAULT_PROPS = {
        "name": None,
        "id": None,
        "inchi": None,
        "cas": None,
        "molecular_formula": None,
        "molecular_weight": None,
        "density": None,
        "concentration": None,
        "role": "reagent",
        "preserve": False,
        "use_for_cleaning": False,
        "clean_with": None,
        "stir": False,
        "temp": None,
        "atmosphere": None,
        "purity": None,
        "solid": False,
    }

    PROP_LIMITS = {
        "molecular_formula": MOLECULAR_FORMULA_PROP_LIMIT,
        "molecular_weight": MOLECULAR_WEIGHT_PROP_LIMIT,
        "density": DENSITY_PROP_LIMIT,
        "concentration": CONCENTRATION_PROP_LIMIT,
        "temp": TEMP_PROP_LIMIT,
        "purity": PERCENT_RANGE_PROP_LIMIT,
    }

    def __init__(
        self,
        name: Optional[str] = "default",
        id: Optional[str] = "default",  # noqa: A002
        inchi: Optional[str] = "default",
        cas: Optional[int] = "default",
        molecular_formula: Optional[str] = "default",
        molecular_weight: Optional[float] = "default",
        density: Optional[float] = "default",
        concentration: Optional[float] = "default",
        role: Optional[str] = "default",
        preserve: Optional[bool] = "default",
        use_for_cleaning: Optional[bool] = "default",
        clean_with: Optional[bool] = "default",
        stir: Optional[bool] = "default",
        temp: Optional[float] = "default",
        atmosphere: Optional[str] = "default",
        purity: Optional[float] = "default",
        solid: Optional[bool] = "default",
        **kwargs,
    ) -> None:
        if not (name or id):
            raise XDLError("At least one of 'name' or 'id' must be specified.")
        super().__init__(locals())

        if not self.id:
            self.id = self.name
