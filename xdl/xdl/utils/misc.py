from typing import Any, Optional
from tabulate import tabulate

from .prop_limits import (
    PropLimit,
    TEMP_PROP_LIMIT,
    TIME_PROP_LIMIT,
    ROTATION_SPEED_PROP_LIMIT,
    VOLUME_PROP_LIMIT,
    MASS_PROP_LIMIT,
    PRESSURE_PROP_LIMIT,
)
from ..errors import XDLError
if False:
    from ..steps import Step

def get_port_str(port: str) -> str:
    """Get str representing port for using in human_readable strings.

    Args:
        port (str): Port name

    Returns:
        str: if port is 'top' return '(port top)' if port is None return ''
    """
    if port:
        return '(port {0})'.format(port)
    return ''

def format_property(
    prop: str,
    val: Any,
    prop_type: type,
    prop_limit: PropLimit,
    human_readable: Optional[bool] = True
) -> str:
    """Given property key and value in standard units, convert value
    to sensitive units and return str ready for putting in XDL.
    E.g. time: 3600 -> '1 hr', volume 2000 -> '2 l'.
    If no modifications are required just return str of val.

    Args:
        prop (str): Property name.
        val (Any): Property value.
        human_readable (Optional[bool]): If True, ports will be represented as
            (port top) as they should be in human readable sentences, if False,
            will be unaltered as it is for XDL file generation.

    Returns:
        str: Value converted to nice units if necessary and returned
            as neat str ready for outputting.
    """
    if val is None:
        return None

    if prop_limit is TIME_PROP_LIMIT:
        return format_time(val)

    elif prop == 'remove_dead_volume':
        return str(val)

    # endswith must be used as 'dead_volume_target' isn't a volume.
    elif prop_limit is VOLUME_PROP_LIMIT:
        return format_volume(val)

    elif prop_limit is MASS_PROP_LIMIT:
        return format_mass(val)

    elif prop is TEMP_PROP_LIMIT:
        return format_temp(val)

    elif prop is PRESSURE_PROP_LIMIT:
        return format_pressure(val)

    elif 'port' in prop and human_readable:
        return get_port_str(val)

    elif prop is ROTATION_SPEED_PROP_LIMIT:
        return format_stir_rpm(val)

    elif prop_type == int:
        return format_int(val)

    elif type(val) == list:
        return ' '.join([str(item) for item in val])

    return str(val)

def format_int(val) -> str:
    if val is not None:
        return str(int(val))

def format_stir_rpm(val: float) -> str:
    """Return formatted stir speed in RPM.

    Args:
        val (float): Stir speed in RPM.

    Returns:
        str: Formatted stir speed in RPM.
    """
    return f'{format_val(val)} RPM'

def format_pressure(val_mbar: float) -> str:
    """Return formatted pressure in sensible units.

    Args:
        val_mbar (float): Pressure in mbar.

    Returns:
        str: Formatted pressure in sensible units.
    """
    if type(val_mbar) in [float, int]:
        return f'{format_val(val_mbar)} mbar'
    # 'low' or 'high' in pneumatic controller step.
    else:
        return val_mbar

def format_volume(val_ml: float) -> str:
    """Return formatted volume in sensible units.

    Args:
        val_ml (float): Volume in mL.

    Returns:
        str: Formatted volume in sensible units.
    """
    if val_ml == 'all':
        return val_ml
    elif val_ml == 0:
        return '0'
    # litres
    if val_ml > 1000:
        litres = val_ml / 1000
        return f'{format_val(litres)} l'
    # microlitres
    elif val_ml < 0.1:
        ul = val_ml * 1000
        return f'{format_val(ul)} ul'
    # millilitres
    return f'{format_val(val_ml)} mL'

def format_time(val_seconds: float) -> str:
    """Return formatted time in sensible units.

    Args:
        val_seconds (float): Time in seconds.

    Returns:
        str: Formatted time in sensible units.
    """
    val = val_seconds
    if val_seconds > 60:
        minutes = val_seconds / 60
        # hours
        if minutes > 60:
            hours = minutes / 60
            val_str = f'{format_val(hours)} hrs'
            val = hours
        # minutes
        else:
            val_str = f'{format_val(minutes)} mins'
            val = minutes
    # seconds
    else:
        val_str = f'{format_val(val_seconds)} secs'
    # Convert '1 hrs' to '1 hr'.
    if val == 1:
        val_str = val_str[:-1]
    return val_str

def format_mass(val_grams: float) -> str:
    """Return formatted mass in sensible units.

    Args:
        val_grams (float): Mass in grams.

    Returns:
        str: Formatted mass in sensible units.
    """
    if val_grams > 1000:
        # kilograms
        kg = val_grams / 1000
        return f'{format_val(kg)} kg'
    elif val_grams < 0.1:
        # milligrams
        mg = val_grams * 1000
        return f'{format_val(mg)} mg'
    # grams
    return f'{format_val(val_grams)} g'

def format_temp(val_celsius: float) -> str:
    """Return formatted temperature.

    Args:
        val_celsius (float): Temperature in °C.

    Returns:
        str: Formatted temperature.
    """
    if type(val_celsius) == str:  # 'reflux' or 'None'
        return val_celsius
    else:
        return f'{format_val(val_celsius)}°C'

def format_val(val: float) -> str:
    """Format float and return as str. Rules are round to two decimal places,
    then remove any trailing 0s and decimal point if necessary.

    Args:
        val (float): Number to format.

    Returns:
        str: Number rounded to two decimal places with trailing '0' and '.'
            removed.
    """
    return f'{val:.4f}'.rstrip('0').rstrip('.')

class SanityCheck(object):
    """Class for Step sanity checks."""
    def __init__(
        self, condition: bool, error_msg: str = '', step: 'Step' = None
    ) -> None:
        self.condition = condition
        self.error_msg = error_msg

    def run(self, step):
        try:
            assert self.condition
        except AssertionError:
            raise XDLError(
                f'{self.error_msg}\n\n\
 {str(step.name)}\n\n\
 {str(step.properties)}'
            )

def steps_are_equal(step, other_step):
    """Return True if given two Step objects are equal in terms of type,
    properties and children, otherwise return False.
    """
    accepted_none_values = [None, '']
    if step.name != other_step.name:
        return False
    for prop, val in step.properties.items():
        if prop != 'children':
            # Accept '' and None as being equal, otherwise JSON loading and
            # XML loading differ as JSON converts empty strings to None.
            if (val in accepted_none_values
                    and step.properties[prop] in accepted_none_values):
                continue
            if val != other_step.properties[prop]:
                return False
    if 'children' in step.properties and step.children:
        if 'children' not in other_step.properties:
            return False
        if len(step.children) != len(other_step.children):
            return False
        for j, child in enumerate(step.children):
            if not steps_are_equal(child, other_step.children[j]):
                return False
    return True

def xdl_elements_are_equal(xdl_element, other_xdl_element):
    """Return True if given Reagent or Component objects are equal in terms of
    type and properties, otherwise return False.
    """
    accepted_none_values = [None, '']
    if xdl_element.name != other_xdl_element.name:
        return False
    for prop, val in xdl_element.properties.items():
        # Accept '' and None as being equal, otherwise JSON loading and
        # XML loading differ as JSON converts empty strings to None.
        if (val in accepted_none_values
                and xdl_element.properties[prop] in accepted_none_values):
            continue
        if val != other_xdl_element.properties[prop]:
            return False
    return True

def reagent_volumes_table(reagent_volumes) -> str:
    """Pretty print table of reagent volumes used in procedure."""

    if not reagent_volumes:
        return ''

    # Convert reagent volumes to list of tuples
    reagent_volumes = [
        (reagent, volume)
        for reagent, volume in reagent_volumes.items()
    ]
    # Sort reagent volumes by decreasing volume
    reagent_volumes = sorted(reagent_volumes, key=lambda x: 1 / x[1])

    # Convert volumes to formatted strings
    table = []
    for reagent, volume in reagent_volumes:
        unit = 'mL'
        if volume > 1000:
            unit = 'L'
            volume /= 1000
        elif volume < 0.1:
            volume *= 1000
            unit = 'µL'
        fmt_volume = f'{volume:.2f}'.rstrip('0').rstrip('0').rstrip('.')
        fmt_volume += f' {unit}'
        table.append((reagent, fmt_volume))

    # Create table
    return tabulate(
        table,
        headers=['Reagent', 'Volume Used'],
        tablefmt='pretty'
    )
