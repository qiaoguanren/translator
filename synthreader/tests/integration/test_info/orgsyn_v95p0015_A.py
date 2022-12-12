from chemputerxdl.steps import *
from xdl.steps import *
from synthreader.finishing.constants import DEFAULT_SLOW_ADDITION_DISPENSE_SPEED

ORGSYN_V95P0015_A_TEXT = '''A one-necked (B14, diameter: 4.5 cm) 25 mL round-bottomed flask is open to air, equipped with a 3 x 10 mm egg shaped magnetic stirring bar, and charged with tris(2,4-di-tert-butylphenyl)phosphite (1) (0.647 g, 1.00 mmol) and chloro(dimethyl sulfide)gold (2) (0.295 g, 1.00 mmol, 1.0 equiv) (Note 2). Dichloromethane (5 mL) is added via syringe (Note 3) and the flask is fitted with a glass stopper.
The resulting colorless solution (Figure 1) is stirred (800 rpm) at 23 °C for 1 h. The volatiles are removed by rotatory evaporation (300 mmHg, 30 °C bath temperature) and then, under a higher vacuum (1 mmHg) for 24 h to afford gold(I) chloride complex 3 (0.879 g, quantitative yield) as a white solid (Note 4) (Figure 2).'''

ORGSYN_V95P0015_A_INFO = {
    'text': ORGSYN_V95P0015_A_TEXT,
    'name': 'orgsyn_v95p0015_a',
    'reagents': {
        'A one-necked': {
            'quantities': [],
        },
        'tris(2,4-di-tert-butylphenyl)phosphite': {
            'quantities': ['0.647 g', '1.00 mmol'],
        },
        'chloro(dimethyl sulfide)gold': {
            'quantities': ['0.295 g', '1.00 mmol', '1.0 equiv'],
        },
        'dichloromethane': {
            'quantities': ['5 mL'],
        },
        'gold(I)chloride complex 3': {
            'quantities': [],
        },
    },
    'steps': [
        Add,
        Add,
        Add,
        HeatChill,
        Evaporate,
        Dry,
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
        # Dry
        {
            'vessel': 'rotavap',
        },
    ],
    'properties': [
        # Add
        {
            'reagent': 'tris(2,4-di-tert-butylphenyl)phosphite',
            'mass': 0.647,
            'stir': False,
        },
        # Add
        {
            'reagent': 'chloro(dimethyl sulfide)gold',
            'mass': 0.295,
            'stir': False,
        },
        # Add
        {
            'reagent': 'dichloromethane',
            'volume': 5.0,
            'dispense_speed': DEFAULT_SLOW_ADDITION_DISPENSE_SPEED,
            'stir': False,
        },
        # HeatChill
        {
            'temp': 23.0,
            'time': 3600.0,
            'stir_speed': 800.0,
        },
        # Transfer
        {
        },
        # Evaporate
        {
            'temp': 30.0,
            'pressure': 399.966,
            'time': 1800,
            'mode': 'auto',
        },
        # Dry
        {
            'time': 86400.0,
            'vacuum_pressure': 1.3332,
        },
    ],
}
