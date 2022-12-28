import re

class PropLimit(object):
    """Convenience class for storing prop limit.

    Arguments:
        regex (str): Regex pattern that should match with valid values and not
            match with invalid values.
        hint (str): Optional. Useful hint for what valid value should look like.
        default (str): Optional. Default valid value.
        enum (List[str]): List of values that the prop can take.
    """
    def __init__(
        self,
        regex=None,
        hint='',
        default='',
        enum=[],
    ):
        if not regex and not enum:
            raise ValueError(
                'Either `regex` or `enum` argument must be given.')

        self.default = default

        # If enum given generate regex from this
        self.enum = enum
        if enum:
            if not regex:
                self.regex = self.generate_enum_regex()
            else:
                self.regex = regex

            if not hint:
                self.hint = self.generate_enum_hint()
            else:
                self.hint = hint

        # Otherwise just set regex as attribute
        else:
            self.regex = regex
            self.hint = hint

    def validate(self, value):
        return re.match(self.regex, value)

    def generate_enum_regex(self):
        regex = r'('
        for item in self.enum:
            regex += item + r'|'
        regex = regex[:-1] + r')'
        return regex

    def generate_enum_hint(self):
        s = 'Expecting one of '
        for item in self.enum[:-1]:
            s += f'"{item}", '
        s = s[:-2] + f' or "{self.enum[-1]}".'
        return s

##################
# Regex patterns #
##################

FLOAT_PATTERN = r'([-]?[0-9]+(?:[.][0-9]+)?)'
POSITIVE_FLOAT_PATTERN = r'([0-9]+(?:[.][0-9]+)?)'

BOOL_PATTERN = r'(false|False|true|True)'

VOLUME_UNITS_PATTERN = r'(l|L|litre|litres|liter|liters|ml|mL|cm3|cc|milliltre|millilitres|milliliter|milliliters|cl|cL|centiltre|centilitres|centiliter|centiliters|dl|dL|deciltre|decilitres|deciliter|deciliters|ul|uL|μl|μL|microlitre|microlitres|microliter|microliters)?'

MASS_UNITS_PATTERN = r'(g|gram|grams|kg|kilogram|kilograms|mg|milligram|milligrams|ug|μg|microgram|micrograms)?'

TEMP_UNITS_PATTERN = r'(°C|K|F)?'

TIME_UNITS_PATTERN = r'(days|day|h|hr|hrs|hour|hours|m|min|mins|minute|minutes|s|sec|secs|second|seconds)?'

PRESSURE_UNITS_PATTERN = r'(mbar|bar|torr|Torr|mmhg|mmHg|atm|Pa|pa)?'

ROTATION_SPEED_UNITS_PATTERN = r'(rpm|RPM)?'

DISTANCE_UNITS_PATTERN = r'(nm|µm|mm|cm|m|km)?'

MOL_UNITS_PATTERN = r'(mmol|mol)?'

###############
# Prop limits #
###############

def generate_quantity_units_pattern(
        quantity_pattern, units_pattern, hint='', default=''):
    return PropLimit(
        regex=r'^((' + quantity_pattern + r'[ ]?'\
            + units_pattern + r'$)|(^' + quantity_pattern + r'))$',
        hint=hint,
        default=default
    )

# NOTE: It is important here that defaults use the standard unit for that
# quantity type as XDL app uses this to add in default units.

VOLUME_PROP_LIMIT = PropLimit(
    regex=r'^(all|(' + POSITIVE_FLOAT_PATTERN + r'[ ]?'\
        + VOLUME_UNITS_PATTERN + r')|(' + POSITIVE_FLOAT_PATTERN + r'))$',
    hint='Expecting number followed by standard volume units, e.g. "5.5 mL"',
    default='0 mL',
)

MASS_PROP_LIMIT = generate_quantity_units_pattern(
    POSITIVE_FLOAT_PATTERN,
    MASS_UNITS_PATTERN,
    hint='Expecting number followed by standard mass units, e.g. "2.3 g"',
    default='0 g'
)

MOL_PROP_LIMIT = generate_quantity_units_pattern(
    POSITIVE_FLOAT_PATTERN,
    MOL_UNITS_PATTERN,
    hint='Expecting number followed by mol or mmol, e.g. "2.3 mol".',
    default='0 mol',
)

TEMP_PROP_LIMIT = generate_quantity_units_pattern(
    FLOAT_PATTERN,
    TEMP_UNITS_PATTERN,
    hint='Expecting number in degrees celsius or number followed by standard temperature units, e.g. "25", "25°C", "298 K".',
    default='25°C',
)

TIME_PROP_LIMIT = generate_quantity_units_pattern(
    POSITIVE_FLOAT_PATTERN,
    TIME_UNITS_PATTERN,
    hint='Expecting number followed by standard time units, e.g. "15 mins", "3 hrs".',
    default='0 secs'
)

PRESSURE_PROP_LIMIT = generate_quantity_units_pattern(
    POSITIVE_FLOAT_PATTERN,
    PRESSURE_UNITS_PATTERN,
    hint='Expecting number followed by standard pressure units, e.g. "50 mbar", "1 atm".',
    default='1013.25 mbar'
)

ROTATION_SPEED_PROP_LIMIT = generate_quantity_units_pattern(
    POSITIVE_FLOAT_PATTERN,
    ROTATION_SPEED_UNITS_PATTERN,
    hint='Expecting RPM value, e.g. "400 RPM".',
    default='400 RPM',
)

WAVELENGTH_PROP_LIMIT = generate_quantity_units_pattern(
    POSITIVE_FLOAT_PATTERN,
    DISTANCE_UNITS_PATTERN,
    hint='Expecting wavelength, e.g. "400 nm".',
    default='400 nm'
)

POSITIVE_INT_PROP_LIMIT = PropLimit(
    r'[0-9]+',
    hint='Expecting positive integer value, e.g. "3"',
    default='1',
)

POSITIVE_FLOAT_PROP_LIMIT = PropLimit(
    regex=POSITIVE_FLOAT_PATTERN,
    hint='Expecting positive float value, e.g. "3", "3.5"',
    default='0',
)

BOOL_PROP_LIMIT = PropLimit(
    BOOL_PATTERN,
    hint='Expecting one of "false" or "true".',
    default='false',
)

WASH_SOLID_STIR_PROP_LIMIT = PropLimit(
    r'(' + BOOL_PATTERN + r'|solvent)',
    enum=['true', 'solvent', 'false'],
    hint='Expecting one of "true", "false" or "solvent".',
    default='True'
)

SEPARATION_PURPOSE_PROP_LIMIT = PropLimit(enum=['extract', 'wash'])
SEPARATION_PRODUCT_PHASE_PROP_LIMIT = PropLimit(enum=['top', 'bottom'])

ADD_PURPOSE_PROP_LIMIT = PropLimit(
    enum=[
        'neutralize',
        'precipitate',
        'dissolve',
        'basify',
        'acidify',
        'dilute',
    ])

HEATCHILL_PURPOSE_PROP_LIMIT = PropLimit(
    enum=['control-exotherm', 'reaction', 'unstable-reagent']
)

STIR_PURPOSE_PROP_LIMIT = PropLimit(
    enum=['dissolve']
)

HEATCHILL_PURPOSE_PROP_LIMIT = PropLimit(
    enum=['reaction', 'control-exotherm', 'unstable-reagent']
)

REAGENT_ROLE_PROP_LIMIT = PropLimit(
    enum=[
        'solvent',
        'reagent',
        'catalyst',
        'substrate',
        'acid',
        'base',
        'activating-agent'
    ]
)

COMPONENT_TYPE_PROP_LIMIT = PropLimit(
    enum=['reactor', 'filter', 'separator', 'rotavap', 'flask']
)

_hundred_float = r'(100(?:[.][0]+)?)'
_ten_to_ninety_nine_float = r'([0-9][0-9](?:[.][0-9]+)?)'
_zero_to_ten_float = r'([0-9](?:[.][0-9]+)?)'
PERCENT_RANGE_PROP_LIMIT = PropLimit(
    r'^(' + _hundred_float + '|'\
        + _ten_to_ninety_nine_float + '|' + _zero_to_ten_float + ')$',
    hint='Expecting number from 0-100 representing a percentage, e.g. "50", "8.5".',
    default='0',
)
