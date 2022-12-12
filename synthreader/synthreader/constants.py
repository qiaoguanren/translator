from typing import Dict, List

##############
# Unit codes #
##############

TIME_SECOND = 0
TIME_MIN = 1
TIME_HOUR = 2
TIME_DAY = -1

TEMP_CELSIUS = 3
TEMP_FAHRENHEIT = 4
TEMP_KELVIN = 5

PERCENT = 6
MOL = 7
MMOL = 8
MOL_PER_L = 9

VOLUME_ML = 10
VOLUME_L = 11
VOLUME_UL = 12
VOLUME_CL = 13
VOLUME_DL = 14

MASS_KG = 15
MASS_G = 16
MASS_MG = 17
MASS_UG = 18
MOL_PERCENT = 19
EQUIVALENTS = 20

PRESSURE_MBAR = 21
PRESSURE_PASCAL = 22
PRESSURE_MMHG = 23
PRESSURE_ATM = 24
PRESSURE_TORR = 25
PRESSURE_BAR = 26

STIR_SPEED_RPM = 27

LENGTH_CM = 28
LENGTH_MM = 29

TIME_UNIT_CODES = [TIME_SECOND, TIME_MIN, TIME_HOUR, TIME_DAY]
TEMP_UNIT_CODES = [TEMP_CELSIUS, TEMP_FAHRENHEIT, TEMP_KELVIN]
MOL_UNIT_CODES = [MOL, MMOL]
CONC_UNIT_CODES = [MOL_PER_L, MOL_PERCENT]
VOLUME_UNIT_CODES = [VOLUME_L, VOLUME_ML, VOLUME_UL, VOLUME_DL, VOLUME_CL]
MASS_UNIT_CODES = [MASS_G, MASS_KG, MASS_MG, MASS_UG]
PERCENT_UNIT_CODES = [PERCENT]
EQUIVALENTS_UNIT_CODES = [EQUIVALENTS]
PRESSURE_UNIT_CODES = [
    PRESSURE_MBAR,
    PRESSURE_PASCAL,
    PRESSURE_MMHG,
    PRESSURE_ATM,
    PRESSURE_TORR,
    PRESSURE_BAR,
]
STIR_SPEED_UNIT_CODES = [STIR_SPEED_RPM]
LENGTH_UNIT_CODES = [LENGTH_CM, LENGTH_MM]
MOL_PERCENT_UNIT_CODES = [MOL_PERCENT]

WORD_UNIT_DICT = {
    's': TIME_SECOND,
    'sec': TIME_SECOND,
    'secs': TIME_SECOND,
    'second': TIME_SECOND,
    'seconds': TIME_SECOND,

    'm': TIME_MIN,
    'min': TIME_MIN,
    'mins': TIME_MIN,
    'minute': TIME_MIN,
    'minutes': TIME_MIN,

    'h': TIME_HOUR,
    'hr': TIME_HOUR,
    'hrs': TIME_HOUR,
    'hour': TIME_HOUR,
    'hours': TIME_HOUR,

    'day': TIME_DAY,
    'days': TIME_DAY,

    'mol': MOL,
    'mole': MOL,
    'moles': MOL,
    'mmol': MMOL,
    'mmole': MMOL,
    'mmoles': MMOL,

    'molpercent': MOL_PERCENT,
    'mol %': MOL_PERCENT,
    'mol%': MOL_PERCENT,

    'M': MOL_PER_L,
    'N': MOL_PER_L,

    'cc': VOLUME_ML,
    'ml': VOLUME_ML,
    'mL': VOLUME_ML,
    'cm3': VOLUME_ML,
    'millilitre': VOLUME_ML,
    'milliliter': VOLUME_ML,
    'millilitres': VOLUME_ML,
    'milliliters': VOLUME_ML,

    'l': VOLUME_L,
    'L': VOLUME_L,
    'litre': VOLUME_L,
    'liter': VOLUME_L,
    'litres': VOLUME_L,
    'liters': VOLUME_L,

    'cl': VOLUME_CL,
    'cL': VOLUME_CL,
    'centilitre': VOLUME_CL,
    'centiliter': VOLUME_CL,
    'centilitres': VOLUME_CL,
    'centiliters': VOLUME_CL,

    'dl': VOLUME_DL,
    'dL': VOLUME_DL,
    'deciliter': VOLUME_DL,
    'decilitre': VOLUME_DL,
    'deciliters': VOLUME_DL,
    'decilitres': VOLUME_DL,

    'μL': VOLUME_UL,
    'μl': VOLUME_UL,
    'µL': VOLUME_UL,  # This is different to the μ above
    'µl': VOLUME_UL,  # This is different to the μ above
    'ul': VOLUME_UL,
    'uL': VOLUME_UL,
    'microlitre': VOLUME_UL,
    'microliter': VOLUME_UL,
    'microlitres': VOLUME_UL,
    'microliters': VOLUME_UL,

    'kg': MASS_KG,
    'kilogram': MASS_KG,
    'kilograms': MASS_KG,

    'g': MASS_G,
    'gram': MASS_G,
    'grams': MASS_G,

    'mg': MASS_MG,
    'milligram': MASS_MG,
    'milligrams': MASS_MG,

    'ug': MASS_UG,
    'microgram': MASS_UG,
    'micrograms': MASS_UG,

    '°C': TEMP_CELSIUS,
    '° C': TEMP_CELSIUS,
    'F': TEMP_FAHRENHEIT,
    'K': TEMP_KELVIN,

    '%': PERCENT,
    'percent': PERCENT,

    'equivalent': EQUIVALENTS,
    'equivalents': EQUIVALENTS,
    'equiv.': EQUIVALENTS,
    'equiv': EQUIVALENTS,
    'eq.': EQUIVALENTS,
    'eq': EQUIVALENTS,

    'mbar': PRESSURE_MBAR,
    'bar': PRESSURE_BAR,
    'mmHg': PRESSURE_MMHG,
    'atm': PRESSURE_ATM,
    'torr': PRESSURE_TORR,
    'Pa': PRESSURE_PASCAL,

    'rpm': STIR_SPEED_RPM,
    'RPM': STIR_SPEED_RPM,

    'cm': LENGTH_CM,
    'mm': LENGTH_MM,
}

TIME_UNITS = [word
              for word, code in WORD_UNIT_DICT.items()
              if code in TIME_UNIT_CODES]

TEMP_UNITS = [word
              for word, code in WORD_UNIT_DICT.items()
              if code in TEMP_UNIT_CODES]

MOL_UNITS = [word
             for word, code in WORD_UNIT_DICT.items()
             if code in MOL_UNIT_CODES]

CONC_UNITS = [word
              for word, code in WORD_UNIT_DICT.items()
              if code in CONC_UNIT_CODES]

VOLUME_UNITS = [word
                for word, code in WORD_UNIT_DICT.items()
                if code in VOLUME_UNIT_CODES]

MASS_UNITS = [word
              for word, code in WORD_UNIT_DICT.items()
              if code in MASS_UNIT_CODES]

EQUIVALENTS_UNITS = [word
                     for word, code in WORD_UNIT_DICT.items()
                     if code in EQUIVALENTS_UNIT_CODES]

PERCENT_UNITS = [word
                 for word, code in WORD_UNIT_DICT.items()
                 if code in PERCENT_UNIT_CODES]

PRESSURE_UNITS = [word
                  for word, code in WORD_UNIT_DICT.items()
                  if code in PRESSURE_UNIT_CODES]

STIR_SPEED_UNITS = [word
                    for word, code in WORD_UNIT_DICT.items()
                    if code in STIR_SPEED_UNIT_CODES]

LENGTH_UNITS = [word
                for word, code in WORD_UNIT_DICT.items()
                if code in LENGTH_UNIT_CODES]

MOL_PERCENT_UNITS = [word
                     for word, code in WORD_UNIT_DICT.items()
                     if code in MOL_PERCENT_UNIT_CODES]

float_regex_pattern = r'([-]?[0-9]+(?:[.][0-9]+)?)'

ratio_regex_pattern = (
    r'^' + float_regex_pattern + r':' + float_regex_pattern + '$')

range_float_regex_pattern = (
    float_regex_pattern + r'([ ]?[-−–][ ]?)' + float_regex_pattern)

multiplier_regex_pattern = float_regex_pattern + r'[xX×]'

conc_regex_pattern = float_regex_pattern + r'[ ]?M'

#: Used by MultiplierWord __init__ and multiplier pattern matching.
LITERAL_MULTIPLIER_DICT: Dict[str, int] = {
    'once': 1,
    'twice': 2,
    'three times': 3,
    'four times': 4,
    'five times': 5,
    'six times': 6,
    'seven times': 7,
    'eight times': 8,
    'nine times': 9,
    'ten times': 10,
}

TO_PREPOSITIONS = ['to', 'to the', 'into', 'onto']
WITH_PREPOSITIONS = ['with', 'with an additional']

#: Words that indicate fast stirring
FAST_STIRRING_WORDS: List[str] = ['vigorous', 'rapid', 'shaking']

#: Words meaning reagent is cold
COLD_WORDS: List[str] = ['cold']

#: Words meaning reagent is icecold
ICECOLD_WORDS: List[str] = ['icecold', 'ice', 'ice-cold']

#: Words meaning reagent is warm
WARM_WORDS: List[str] = ['warm']

#: Words meaning reagent is hot
HOT_WORDS: List[str] = ['hot', 'boiling']

#: Words that should be ignored at start of reagent name
MISC_REAGENT_NAME_START_WORDS: List[str] = ['more']

#: Words meaning use minimum volume
MINIMUM_VOLUME_WORDS: List[str] = ['minimum']

DEFAULT_SLOW_STIR_SPEED: int = 50

#: Default speed in RPM for 'stirred vigorously'
DEFAULT_FAST_STIR_SPEED: float = 600

#: Placeholder value for reflux temperatures that will be filled in later
REFLUX_PLACEHOLDER_TEMP: float = 97.97979797979797

#: Default time if time given as 'overnight'
DEFAULT_OVERNIGHT_TIME: int = 16 * 60 * 60

#: Amount to decrease temp by if procedure says 'below 5 °C'
DEFAULT_BELOW_TEMP_REDUCTION: int = 3
