from chemputerxdl.steps import *
from xdl.steps import *

CSSP13_TEXT = '''Triethylamine was added to a stirred solution of the pyranone in DMF (2.5 ml / mmol). The reaction mixture was heated at 80 °C for 24 hours. The Solvent was then removed in vacuo to give a brown oil. This material was purified by chromatography on silica-gel using petrol:ethyl acetate (2:1, v:v) as eluent. This gave a yellow oil which crystallised on standing to give the product as a white solid (38.4 g, 78%).'''

CSSP13_INFO = {
    'text': CSSP13_TEXT,
    'name': 'cssp13',
    'reagents': {
        'triethylamine': {
            'quantities': [],
        },
        'the pyranone': {
            'quantities': [],
        },
        'DMF': {
            'quantities': [],
        },
    },
    'steps': [
        Add,
        Add,
        HeatChill,
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
        # HeatChill
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
            'reagent': 'the pyranone DMF solution',
        },
        # Add
        {
            'reagent': 'triethylamine',
        },
        # HeatChill
        {
            'temp': 80.0,
            'time': 86400.0,
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Evaporate
        {
            'temp': 50,
            'pressure': 6.0,
            'time': 1800,
            'mode': 'auto',
        },
        # RunColumn
        {
            'column': 'column',
        },
    ],
}
