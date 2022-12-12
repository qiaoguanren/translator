from typing import Union, Dict, Callable
import re
from .prop_limits import (
    POSITIVE_FLOAT_PROP_LIMIT,
    POSITIVE_INT_PROP_LIMIT,
    BOOL_PROP_LIMIT,
    PropLimit
)

#############
# Constants #
#############

#: Default prop limits to use for types if no prop limit is given.
DEFAULT_PROP_LIMITS: [type, PropLimit] = {
    float: POSITIVE_FLOAT_PROP_LIMIT,
    int: POSITIVE_INT_PROP_LIMIT,
    bool: BOOL_PROP_LIMIT,
}

#: Regex pattern to match all of '1', '-1', '1.0', '-1.0' etc
FLOAT_REGEX_PATTERN = r'([-]?[0-9]+(?:[.][0-9]+)?)'

#: Regex pattern to match optional units in quantity strings
#: e.g. match 'mL' in '5 mL'
#: The 3 is there to match 'cm3'
UNITS_REGEX_PATTERN = r'[a-zA-Zμ°]+[3]?'

#########
# Utils #
#########

def parse_bool(s: str) -> bool:
    """Parse bool from string.

    Args:
        s (str): str representing bool.

    Returns:
        bool: True is s lower case is 'true' or '1', otherwise False.

    Raises:
        ValueError: If s.lower() is not 'true' or 'false'.
    """
    if type(s) == bool:
        return s
    elif type(s) == str:
        if s.lower() == 'true':
            return True
        elif s.lower() == 'false':
            return False
    else:
        return None

########################
# Unit Standardisation #
########################

def days_to_seconds(x):
    return x * 60 * 60 * 24

def minutes_to_seconds(x):
    return x * 60

def hours_to_seconds(x):
    return x * 60 * 60

def no_conversion(x):
    return x

def cl_to_ml(x):
    return x * 10

def dl_to_ml(x):
    return x * 10**2

def l_to_ml(x):
    return x * 10**3

def ul_to_ml(x):
    return x * 10**-3

def kilogram_to_grams(x):
    return x * 10**3

def milligram_to_grams(x):
    return x * 10**-3

def microgram_to_grams(x):
    return x * 10**-6


#: Dict of units in lower case and functions to convert them to standard units.
#: Standard units:
UNIT_CONVERTERS: Dict[str, Callable] = {
    'ml': no_conversion,
    'millilitre': no_conversion,
    'milliliter': no_conversion,
    'milliliters': no_conversion,
    'millilitres': no_conversion,
    'cm3': no_conversion,
    'cc': no_conversion,

    'cl': cl_to_ml,
    'centilitre': cl_to_ml,
    'centiliter': cl_to_ml,
    'centilitres': cl_to_ml,
    'centiliters': cl_to_ml,

    'dl': dl_to_ml,
    'decilitre': dl_to_ml,
    'deciliter': dl_to_ml,
    'decilitres': dl_to_ml,
    'deciliters': dl_to_ml,

    'l': l_to_ml,
    'liter': l_to_ml,
    'litre': l_to_ml,
    'liters': l_to_ml,
    'litres': l_to_ml,

    'μl': ul_to_ml,
    'ul': ul_to_ml,
    'microlitre': ul_to_ml,
    'microliter': ul_to_ml,
    'microlitres': ul_to_ml,
    'microliters': ul_to_ml,

    'kg': kilogram_to_grams,
    'kilogram': kilogram_to_grams,
    'kilograms': kilogram_to_grams,
    'g': no_conversion,
    'gram': no_conversion,
    'grams': no_conversion,
    'mg': milligram_to_grams,
    'milligram': milligram_to_grams,
    'milligrams': milligram_to_grams,
    'ug': microgram_to_grams,
    'μg': microgram_to_grams,
    'microgram': microgram_to_grams,
    'micrograms': microgram_to_grams,

    '°c': lambda x: x,
    'k': lambda x: x - 273.15,
    'f': lambda x: (x - 32) / 1.8,

    'days': days_to_seconds,
    'day': days_to_seconds,

    'h': hours_to_seconds,
    'hour': hours_to_seconds,
    'hours': hours_to_seconds,
    'hr': hours_to_seconds,
    'hrs': hours_to_seconds,

    'm': minutes_to_seconds,
    'min': minutes_to_seconds,
    'mins': minutes_to_seconds,
    'minute': minutes_to_seconds,
    'minutes': minutes_to_seconds,

    's': no_conversion,
    'sec': no_conversion,
    'secs': no_conversion,
    'second': no_conversion,
    'seconds': no_conversion,

    'mbar': no_conversion,
    'bar': lambda x: x * 10**3,
    'torr': lambda x: x * 1.33322,
    'mmhg': lambda x: x * 1.33322,
    'atm': lambda x: x * 1013.25,
    'pa': lambda x: x * 0.01,

    'rpm': lambda x: x,

    'nm': lambda x: x,
}

def convert_val_to_std_units(val: Union[str, float]) -> float:
    """Given str of value with/without units, convert it into standard unit and
    return float value. If given value is float, return unchanged.

    Standard units:

    time      seconds
    volume    mL
    pressure  mbar
    temp      °c
    mass      g

    Arguments:
        val (Union[str, float]): Value (and units) as str, or float. If no units
            are specified it is assumed value is already in default units. If
            value if float it is returned unchanged.

    Returns:
        float: Value in default units.
    """
    # Val is already float, just return it.
    if type(val) != str:
        return val

    # Get number from string
    number_search = re.search(FLOAT_REGEX_PATTERN, val)
    if number_search:
        number = float(number_search[0])

        # Get unit from string
        unit_search = re.search(UNITS_REGEX_PATTERN, val)
        if unit_search:
            unit = unit_search[0]

            # Convert number to standard units
            return UNIT_CONVERTERS[unit.lower()](number)

        # No unit found, just return number
        else:
            return number

    # Can't even find number in string, return val unchanged.
    return val
