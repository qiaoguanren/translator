from chemputerxdl.steps import *
from xdl.steps import *
from synthreader.finishing.constants import (
    DEFAULT_STIRRING_TIME,
    DEFAULT_AUTO_EVAPORATION_TIME_LIMIT
)

CSSP25_TEXT = '''The two alkynes are stirred together at 0 °C in pyrrolidine and the copper iodide is added in one portion, initially creating a green coloured solution which quickly turns red/brown. The reaction is stirred at this temperature for 30-60 mins until completion (TLC), then quenched with ammonium chloride solution, extracted 4 times with ether, washed with brine, dried over magnesium sulphate, filtered and concentrated. Purification is achieved by column chromatography eluting with 20-50% EtOAc/PE.'''

CSSP25_INFO = {
    'text': CSSP25_TEXT,
    'name': 'cssp25',
    'reagents': {
        'the 2 alkynes': {
            'quantities': [],
        },
        'pyrrolidine': {
            'quantities': [],
        },
        'the copper iodide': {
            'quantities': [],
        },
        'ammonium chloride solution': {
            'quantities': [],
        },
        'ether': {
            'quantities': [],
        },
        'brine': {
            'quantities': [],
        },
        'magnesium sulphate': {
            'quantities': [],
        },
        '35.0 % EtOAc/PE': {
            'quantities': [],
        },
    },
    'steps': [
        HeatChillToTemp,
        Add,
        Add,
        Stir,
        Add,
        Stir,
        Add,
        Separate,
        Separate,
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
        # Stir
        {
            'vessel': 'reactor',
        },
        # Add
        {
            'vessel': 'reactor',
        },
        # Stir
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
        # Separate
        {
            'from_vessel': 'separator',
            'separation_vessel': 'separator',
            'to_vessel': 'rotavap',
        },
        # Evaporate
        {
            'rotavap_name': 'rotavap',
        },
        # RunColumn
        {
            'from_vessel': 'rotavap',
            'to_vessel': 'reactor',
            'column': 'column',
        },
    ],
    'properties': [
        # HeatChillToTemp
        {
            'temp': 0.0,
        },
        # Add
        {
            'reagent': 'the 2 alkynes',
            'stir': True,
        },
        # Add
        {
            'reagent': 'pyrrolidine',
            'stir': True,
        },
        # Stir
        {
            'time': DEFAULT_STIRRING_TIME,
        },
        # Add
        {
            'reagent': 'the copper iodide',
            'stir': False,
        },
        # Stir
        {
            'time': 2700.0,
        },
        # Add
        {
            'reagent': 'ammonium chloride solution',
        },
        # Separate
        {
            'purpose': 'extract',
            'solvent': 'ether',
            'n_separations': 4,
        },
        # Separate
        {
            'purpose': 'wash',
            'solvent': 'brine',
            'n_separations': 1,
            'through': 'magnesium sulphate',
        },
        # Evaporate
        {
            'time': DEFAULT_AUTO_EVAPORATION_TIME_LIMIT,
            'mode': 'auto',
        },
        # RunColumn
        {},
    ],
}
