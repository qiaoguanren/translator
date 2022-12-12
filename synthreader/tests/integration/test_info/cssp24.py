from chemputerxdl.steps import *
from xdl.steps import *
from synthreader.finishing.constants import (
    DEFAULT_STIRRING_TIME,
    DEFAULT_AUTO_EVAPORATION_TIME_LIMIT
)

# Text altered http://cssp.chemspider.com/24
CSSP24_TEXT = '''To iodoform in THF is added triphenylphosphine and 1 equivalent of potassium t-butoxide and the brown mixture is stirred for 1 minute. Cinnamaldehyde is added and the reaction stirred for 15 minutes, then cooled to -78 °C. The remaining potassium t-butoxide is then added and the reaction stirred until completion (TLC immediately after the second addition of potassium t-butoxide in order to ascertain which spot is the intermediate). It was then quenched with brine, extracted twice with ether, dried over magnesium sulphate, filtered, concentrated and purified by column chromatography eluting with 10% Et2O/PE.'''

CSSP24_INFO = {
    'text': CSSP24_TEXT,
    'name': 'cssp24',
    'reagents': {
        'iodoform': {
            'quantities': [],
        },
        'THF': {
            'quantities': [],
        },
        'triphenylphosphine': {
            'quantities': [],
        },
        'potassium t-butoxide': {
            'quantities': ['1 equivalent'],
        },
        'cinnamaldehyde': {
            'quantities': [],
        },
        'brine': {
            'quantities': [],
        },
        'ether': {
            'quantities': [],
        },
        'magnesium sulphate': {
            'quantities': [],
        },
        '10 % Et2O/PE': {
            'quantities': [],
        },
    },
    'steps': [
        Add,
        Add,
        Add,
        Stir,
        Add,
        Stir,
        HeatChillToTemp,
        Add,
        Stir,
        Add,
        Separate,
        Evaporate,
        RunColumn,
    ],
    'vessels': [
        # Add
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
        # HeatChillToTemp
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
        # Add
        {
            'reagent': 'iodoform THF solution',
        },
        # Add
        {
            'reagent': 'triphenylphosphine',
        },
        # Add
        {
            'reagent': 'potassium t-butoxide',
        },
        # Stir
        {
            'time': 60.0,
        },
        # Add
        {
            'reagent': 'cinnamaldehyde',
        },
        # Stir
        {
            'time': 900.0,
        },
        # HeatChillToTemp
        {
            'temp': -78.0,
        },
        # Add
        {
            'reagent': 'potassium t-butoxide',
        },
        # Stir
        {
            'time': DEFAULT_STIRRING_TIME,
        },
        # Add
        {
            'reagent': 'brine',

        },
        # Separate
        {
            'purpose': 'extract',
            'solvent': 'ether',
            'n_separations': 2,
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
