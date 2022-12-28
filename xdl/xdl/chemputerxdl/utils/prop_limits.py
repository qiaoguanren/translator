"""
.. module:: utils.prop_limits
    :platforms: Unix, Windows
    :synopsis: Limit objects to check the ranges of certain properties in
                XDL steps

"""

from xdl.utils.prop_limits import PropLimit

# Limits for the Valve ports
# -1, 1, 2, 3, 4, 5
VALVE_PORT_PROP_LIMIT = PropLimit(
    enum=['0', '1', '2', '3', '4', '5'],
    default='0',
)

# Limits for the Pneumatic Controller ports
PNEUMATIC_CONTROLLER_PORT_PROP_LIMIT = PropLimit(
    enum=['1', '2', '3', '4', '5', '6'],
    default='1',
)

PNEUMATIC_CONTROLLER_PRESSURE_PROP_LIMIT = PropLimit(
    enum=['low', 'high'],
    default='low'
)

# Limits for the different types of port supported
# -1, 1, 2, 3, 4, 5, top, bottom, evaporate, collect, in, out
PORT_PROP_LIMIT = PropLimit(

    enum=[
        '0', '1', '2', '3', '4', '5', 'top', 'bottom', 'evaporate',
        'collect', 'in', 'out'
    ],
    default='0',
)

# Limits for the vessel types
VESSEL_TYPE_PROP_LIMIT = PropLimit(
    enum=['filter', 'reactor', 'separator', 'rotavap', 'flask']
)

# Limits for the vessel classes
VESSEL_CLASS_PROP_LIMIT = PropLimit(
    enum=[
        'ChemputerFilter', 'ChemputerReactor', 'ChemputerPump',
        'ChemputerValve', 'ChemputerSeparator', 'ChemputerFlask',
        'ChemputerWaste', 'ChemputerVacuum', 'ChemputerCartridge',
        'JULABOCF41', 'Huber', 'IKARCTDigital', 'IKARETControlVisc',
        'IKARV10', 'CVC3000', 'IKAmicrostar75', 'RZR_2052', 'HeiTORQUE_100'
    ],
)

# Limits for int (unsigned char)
INT_0_255_PROP_LIMIT = PropLimit(
    r'^(2[0-5][0-5]|1[0-9][0-9]|[0-9]?[0-9])$',
    hint='Expecting int from 0-255, e.g. "128".',
    default='0',
)
