from chemputerxdl.steps import *
from xdl.steps import *

# Text altered
CSSP11_TEXT = '''TBTH (0.5 mmol) and AIBN (0.25 mmol) in toluene (2 ml) was added to the substrate (0.27 mmol) in toluene at reflux and heated until the reaction was complete, 1 hour. The solvent was removed in vacuo. The product was purified by column chromatography (SiO2). Yield 0.28 mmol'''

CSSP11_INFO = {
    'text': CSSP11_TEXT,
    'name': 'cssp11',
    'reagents': {
        'TBTH': {
            'quantities': ['0.5 mmol'],
        },
        'AIBN': {
            'quantities': ['0.25 mmol'],
        },
        'toluene': {
            'quantities': ['2 ml'],
        },
    },
    'steps': [
        Add,
        HeatChillToTemp,
        Add,
        Stir,
        Evaporate,
        RunColumn,
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
        # Add
        {
            'reagent': 'unknown_reagent toluene solution',
        },
        # HeatChillToTemp
        {
            'temp': 110.6,
        },
        # Add
        {
            'reagent': 'TBTH and AIBN toluene solution',
            'volume': 2.0,
        },
        # Stir
        {
            'time': 3600.0,
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Evaporate
        {
            'temp': 50,
            'pressure': 48.0,
            'time': 1800,
            'mode': 'auto',
        },
        # RunColumn
        {
            'column': 'column',
        },
    ],
}
