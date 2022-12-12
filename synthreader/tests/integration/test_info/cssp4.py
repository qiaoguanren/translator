from chemputerxdl.steps import *
from xdl.steps import *
from synthreader.finishing.constants import DEFAULT_DROPWISE_DISPENSE_SPEED

CSSP4_TEXT = '''To a stirring solution of the maleimide and triphenylphosphine in THF at zero under nitrogen was added the alcohol in THF (10 ml) and then DEAD dropwise. The reaction was allowed to warm to room temperature and then left stirring for 2.5 hrs after which time the reaction mixture was concentrated in vacuo. The resultant crude product was purified by flash column chromatography.'''

CSSP4_INFO = {
    'text': CSSP4_TEXT,
    'name': 'cssp4',
    'reagents': {
        'the maleimide': {
            'quantities': [],
        },
        'triphenylphosphine': {
            'quantities': [],
        },
        'THF': {
            'quantities': ['10 ml'],
        },
        'the alcohol': {
            'quantities': [],
        },
        'DEAD': {
            'quantities': [],
        },
    },
    'steps': [
        HeatChillToTemp,
        Add,
        Add,
        Add,
        Add,
        HeatChillToTemp,
        Stir,
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
        # Add
        {
            'vessel': 'reactor',
        },
        # Add
        {
            'vessel': 'reactor',
        },
        # HeatChillToTemp
        {
            'vessel': 'reactor',
        },
        # Stir
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
        # RunColumn
        {
            'from_vessel': 'rotavap',
            'to_vessel': 'reactor',
        },
    ],
    'properties': [
        # HeatChillToTemp
        {
            'temp': 0,
        },
        # Add
        {
            'reagent': 'the maleimide and triphenylphosphine THF solution',

        },
        # Add
        {
            'reagent': 'the alcohol',
            'dispense_speed': DEFAULT_DROPWISE_DISPENSE_SPEED,
        },
        # Add
        {
            'reagent': 'THF',
            'volume': 10.0,
            'dispense_speed': DEFAULT_DROPWISE_DISPENSE_SPEED,
        },
        # Add
        {
            'reagent': 'DEAD',
            'dispense_speed': DEFAULT_DROPWISE_DISPENSE_SPEED,
        },
        # HeatChillToTemp
        {
            'temp': 18,
            'active': False,
            'continue_heatchill': False,
        },
        # Stir
        {
            'time': 9000.0,
        },
        # Transfer
        {},
        # Evaporate
        {
            'temp': 50,
            'pressure': 249.0,
            'time': 1800,
            'mode': 'auto',
        },
        # RunColumn
        {
            'column': 'column',
        },
    ],
}
