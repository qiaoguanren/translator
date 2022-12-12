from chemputerxdl.steps import *
from xdl.steps import *
from synthreader.finishing.constants import DEFAULT_SLOW_ADDITION_DISPENSE_SPEED

CSSP20_TEXT = '''The nitrile is mixed with water at 50°C. Sodium peroxide is added very slowly (usually about a few grains every 5 minutes) until the reaction is complete. The amount of sodium peroxide required varies. If added very slowly, only about 1.5 equivalents may be required. The reaction can be said to be complete when there is only one layer remaining (i.e. the product is miscible, but the nitrile is not), although continuing the addition for a little while after this point, then leaving to stir seems to improve the results. The mixture is extracted with ether, then slowly acidified to pH 5 with conc. HCl, and extracted with ether which, after drying, gives pure carboxylic acid (75%).'''

CSSP20_INFO = {
    'text': CSSP20_TEXT,
    'name': 'cssp20',
    'reagents': {
        'the nitrile': {
            'quantities': [],
        },
        'water': {
            'quantities': [],
        },
        'sodium peroxide': {
            'quantities': [],
        },
        'ether': {
            'quantities': [],
        },
        'concentrated HCl': {
            'quantities': [],
        },
        'pure carboxylic acid (75 %)': {
            'quantities': ['75 %'],
        },
    },
    'steps': [
        Add,
        HeatChillToTemp,
        Add,
        StopHeatChill,
        Add,
        Separate,
        Add,
        Separate,
        Dry
    ],
    'vessels': [
        # Add
        {
            'vessel': 'reactor',
        },
        # HeatChillToTemp
        {
            'vessel': 'reactor',
        },
        # Add
        {
            'vessel': 'reactor',
        },
        # StopHeatChill
        {
            'vessel': 'reactor',
        },
        # Add
        {
            'vessel': 'reactor',
        },
        # Separate
        {
            'from_vessel': 'reactor',
            'separation_vessel': 'separator',
            'to_vessel': 'separator',
        },
        # Add
        {
            'vessel': 'separator',
        },
        # Separate
        {
            'from_vessel': 'separator',
            'separation_vessel': 'separator',
            'to_vessel': 'reactor',
        },
        # Dry
        {}
    ],
    'properties': [
        # Add
        {
            'reagent': 'the nitrile',
        },
        # HeatChillToTemp
        {
            'temp': 50.0,
        },
        # Add
        {
            'reagent': 'water',
        },
        # StopHeatChill
        {},
        # Add
        {
            'reagent': 'sodium peroxide',
            'dispense_speed': DEFAULT_SLOW_ADDITION_DISPENSE_SPEED,
        },
        # Separate
        {
            'purpose': 'extract',
            'solvent': 'ether',
            'n_separations': 1,
        },
        # Add
        {
            'reagent': 'concentrated HCl',
            'dispense_speed': DEFAULT_SLOW_ADDITION_DISPENSE_SPEED,
        },
        # Separate
        {
            'purpose': 'extract',
            'solvent': 'ether',
            'n_separations': 1,
        },
        # Dry
        {}
    ],
}
