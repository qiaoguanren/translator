from chemputerxdl.steps import *
from xdl.steps import *
from synthreader.finishing.constants import (
    DEFAULT_SEPARATION_VOLUME, DEFAULT_DROPWISE_DISPENSE_SPEED)

CSSP12_TEXT = '''The protocol was carried out under nitrogen. t-BuLi was added dropwise to the indole in THF at -78 °C. After 5 minutes Bu3SnCl was added at -78 °C, the solution was stirred for 20 minutes, then warmed to room temperature and the solvent evaporated. Water was added and the organic product was extracted with ether, followed by drying and evaporation. The product was purified by silica-gel chromatography using petroleum ether.'''

CSSP12_INFO = {
    'text': CSSP12_TEXT,
    'name': 'cssp12',
    'reagents': {
        't-BuLi': {
            'quantities': [],
        },
        'the indole': {
            'quantities': [],
        },
        'THF': {
            'quantities': [],
        },
        'Bu3SnCl': {
            'quantities': [],
        },
        'water': {
            'quantities': [],
        },
        'ether': {
            'quantities': [],
        },
        'petroleum ether': {
            'quantities': [],
        },
    },
    'steps': [
        HeatChillToTemp,
        Add,
        Add,
        Wait,
        Add,
        Stir,
        HeatChillToTemp,
        Evaporate,
        Add,
        Separate,
        Dry,
        Evaporate,
        RunColumn,
    ],
    'vessels': [
        # HeatChillToTemp
        {
            'vessel': 'reactor',
        },
        # Add
        {
            'vessel': 'reactor',
        },
        # Add
        {
            'vessel': 'reactor',
        },
        # Wait
        {},
        # Add
        {
            'vessel': 'reactor',
        },
        # Stir
        {
            'vessel': 'reactor',
        },
        # HeatChillToTemp
        {
            'vessel': 'reactor',
        },
        # Transfer
        {
            'from_vessel': 'reactor',
            'to_vessel': 'rotavap',
        },
        # Evaporate
        {
            'rotavap_name': 'rotavap',
        },
        # Add
        {
            'vessel': 'rotavap',
        },
        # Separate
        {
            'from_vessel': 'rotavap',
            'separation_vessel': 'separator',
            'to_vessel': 'rotavap',
        },
        # Dry
        {
            'vessel': 'rotavap',
        },
        # Evaporate
        {
            'rotavap_name': 'rotavap',
        },
        # RunColumn
        {
            'from_vessel': 'rotavap',
            'to_vessel': 'reactor',
        },
    ],
    'properties': [
        # HeatChillToTemp
        {
            'temp': -78.0,
        },
        # Add
        {
            'reagent': 'the indole THF solution',
        },
        # Add
        {
            'reagent': 't-BuLi',
            'dispense_speed': DEFAULT_DROPWISE_DISPENSE_SPEED,
        },
        # Wait
        {
            'time': 60 * 5,
        },
        # Add
        {
            'reagent': 'Bu3SnCl',
        },
        # Stir
        {
            'time': 1200.0,
        },
        # HeatChillToTemp
        {
            'temp': 25.0,
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Evaporate
        {
            'temp': 50,
            'pressure': 249.0,
            'time': 1800,
            'mode': 'auto',
        },
        # Add
        {
            'reagent': 'water',
        },
        # Separate
        {
            'purpose': 'extract',
            'solvent': 'ether',
            'product_bottom': False,
            'solvent_volume': DEFAULT_SEPARATION_VOLUME,
            'n_separations': 1,
        },
        # Dry
        {},
        # Evaporate
        {
            'temp': 50,
            'pressure': 376.3333333333333,
            'time': 1800,
            'mode': 'auto',
        },
        # RunColumn
        {
            'column': 'column',
        },
    ],
}
