from chemputerxdl.steps import *
from xdl.steps import *

CSSP5_TEXT = '''2,2'-dinitro-6,6'-dimethylbiphenyl (39 g, 0.14 mol) was dissolved in 100 ml ethyl acetate in a hydrogenation vessel. Palladium on Carbon (10%, 5.5 g) was added. The system was evacuated and H2 added to a pressure of 28 psi. The reaction was left until no further uptake of H2 could be detected. The solution was filtered through celite and the solvent evaporated to give the product diamine in 100% yield.'''

CSSP5_INFO = {
    'text': CSSP5_TEXT,
    'name': 'cssp5',
    'reagents': {
        "2,2'-dinitro-6,6'-dimethylbiphenyl": {
            'quantities': ['39 g', '0.14 mol'],
        },
        'ethyl acetate': {
            'quantities': ['100 ml'],
        },
        'palladium on Carbon (10 %)': {
            'quantities': ['10 %', '5.5 g'],
        },
        'H2': {
            'quantities': [],
        },
        'diamine': {
            'quantities': [],
        },
    },
    'steps': [
        Confirm,
        Dissolve,
        Add,
        Evacuate,
        Add,
        FilterThrough,
        Evaporate,
    ],
    'vessels': [
        # Confirm
        {},
        # Dissolve
        {
            'vessel': 'reactor',
        },
        # Add
        {
            'vessel': 'reactor',
        },
        # Evacuate
        {
            'vessel': 'reactor',
        },
        # Add
        {
            'vessel': 'reactor',
        },
        # FilterThrough
        {
            'from_vessel': 'reactor',
            'to_vessel': 'rotavap',
        },
        # Evaporate
        {
            'rotavap_name': 'rotavap',
        },
    ],
    'properties': [
        # Confirm
        {
            'msg': "Is 2,2'-dinitro-6,6'-dimethylbiphenyl ( 39 g , 0.14 mol ) in the correct vessel?",
        },
        # Dissolve
        {
            'solvent': 'ethyl acetate',
            'volume': 100.0,
        },
        # Add
        {
            'reagent': 'palladium on Carbon (10 %)',
            'mass': 5.5,
            'stir': True,
        },
        # Evacuate
        {},
        # Add
        {
            'reagent': 'H2',
        },
        # FilterThrough
        {
            'through': 'celite',
        },
        # Evaporate
        {
            'time': 1800,
            'mode': 'auto',
        },
    ],
}
