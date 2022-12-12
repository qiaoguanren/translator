from chemputerxdl.steps import *
from xdl.steps import *

from synthreader.finishing.constants import (
    DEFAULT_DROPWISE_DISPENSE_SPEED,
    DEFAULT_AUTO_EVAPORATION_TIME_LIMIT,
)

DIAZIRINE_TEXT = '''Anhydrous MgSO4 (2 g) was added followed by methanolic ammonia solution (80 mL) and methanolic levulinic acid (9.3 mL, 8.83 M) at -10 °C. The mixture was stirred for 3 hours at this temperature, then the HOSA solution (60 mL) was added dropwise. The reaction mixture was then heated to 20°C,  stirred  for 15 hours,  filtered and concentrated.'''

DIAZIRINE_INFO = {
    'text': DIAZIRINE_TEXT,
    'name': 'diazirine',
    'reagents': {
        'anhydrous MgSO4': {
            'quantities': ['2 g'],
        },
        'methanolic ammonia solution': {
            'quantities': ['80 mL'],
        },
        'methanolic levulinic acid': {
            'quantities': ['9.3 mL', '8.83 M'],
        },
        'the HOSA solution': {
            'quantities': ['60 mL'],
        },
    },
    'steps': [
        HeatChillToTemp,
        Add,
        Add,
        Add,
        Stir,
        Add,
        HeatChillToTemp,
        Stir,
        Filter,
        Evaporate,
    ],
    'vessels': [
        # HeatChillToTemp
        {
            'vessel': 'filter',
        },
        # Add
        {
            'vessel': 'filter',
        },
        # Add
        {
            'vessel': 'filter',
        },
        # Add
        {
            'vessel': 'filter',
        },
        # Stir
        {
            'vessel': 'filter',
        },
        # Add
        {
            'vessel': 'filter',
        },
        # HeatChillToTemp
        {
            'vessel': 'filter',
        },
        # Stir
        {
            'vessel': 'filter',
        },
        # Filter
        {},
        # Transfer
        {
            'from_vessel': 'filter',
            'to_vessel': 'rotavap',
        },
        # Evaporate
        {
            'rotavap_name': 'rotavap',
        },
    ],
    'properties': [
        # HeatChillToTemp
        {
            'temp': -10.0,
        },
        # Add
        {
            'reagent': 'anhydrous MgSO4',
            'mass': 2.0,
            'stir': False,
        },
        # Add
        {
            'reagent': 'methanolic ammonia solution',
            'volume': 80.0,
            'stir': False,
        },
        # Add
        {
            'reagent': 'methanolic levulinic acid',
            'volume': 9.3,
            'stir': True,
        },
        # Stir
        {
            'time': 10800.0,
        },
        # Add
        {
            'reagent': 'the HOSA solution',
            'volume': 60.0,
            'dispense_speed': DEFAULT_DROPWISE_DISPENSE_SPEED,
            'stir': True,
        },
        # HeatChillToTemp
        {
            'temp': 20.0,
        },
        # Stir
        {
            'time': 54000.0,
        },
        # Filter
        {
            'filter_vessel': 'filter',
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Evaporate
        {
            'time': DEFAULT_AUTO_EVAPORATION_TIME_LIMIT,
            'mode': 'auto',
        },
    ],
}
