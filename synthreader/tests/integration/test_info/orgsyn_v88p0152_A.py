from chemputerxdl.steps import *
from xdl.steps import *

ORGSYN_V88P0152_A_TEXT = '''A 500-mL three-necked round-bottomed flask equipped with an overhead mechanical stirrer (teflon paddle, 75 × 20 mm), a glass stopper, and a reflux condenser fitted with an inert gas inlet (Note 1) is charged with benzyl carbamate (30.23 g, 200 mmol, 1.0 equiv) (Note 2) and glyoxylic acid monohydrate (20.25 g, 220 mmol, 1.1 equiv) (Note 3). The flask is evacuated and backfilled with inert gas, the glass stopper is removed under a stream of inert gas and the flask is charged with anhydrous Et2O (200 mL) (Note 4). The resulting translucent solution is heated under reflux for 12 h (Note 5) with stirring at a rate of 200 rpm. Over this time, the product precipitates to give a white suspension. The white precipitate is collected by filtration, washed with hexanes-Et2O (1:1) (6 × 10 mL) (Note 6), and dried in vacuo to yield α-hydroxy-N-benzyloxycarbonylglycine as fine white crystals (32.80-35.37 g, 73-79%) (Note 7).'''

ORGSYN_V88P0152_A_INFO = {
    'text': ORGSYN_V88P0152_A_TEXT,
    'name': 'orgsyn_v88p0152_a',
    'reagents': {
        'benzyl carbamate': {
            'quantities': ['30.23 g', '200 mmol', '1.0 equiv'],
        },
        'glyoxylic acid monohydrate': {
            'quantities': ['20.25 g', '220 mmol', '1.1 equiv'],
        },
        'anhydrous Et2O': {
            'quantities': ['200 mL'],
        },
        'hexanes-Et2O': {
            'quantities': [],
        },
        'α-hydroxy-N-benzyloxycarbonylglycine': {
            'quantities': [],
        },
    },
    'steps': [
        Add,
        Add,
        Evacuate,
        Add,
        HeatChill,
        Filter,
        WashSolid,
        Dry,
    ],
    'vessels': [
        # Add
        {
            'vessel': 'filter',
        },
        # Add
        {
            'vessel': 'filter',
        },
        # Evacuate
        {
            'vessel': 'filter',
        },
        # Add
        {
            'vessel': 'filter',
        },
        # HeatChill
        {
            'vessel': 'filter',
        },
        # Filter
        {},
        # WashSolid
        {
            'vessel': 'filter',
        },
        # Dry
        {
            'vessel': 'filter',
        },
    ],
    'properties': [
        # Add
        {
            'reagent': 'benzyl carbamate',
            'mass': 30.23,
            'stir': False,
        },
        # Add
        {
            'reagent': 'glyoxylic acid monohydrate',
            'mass': 20.25,
            'stir': False,
        },
        # Evacuate
        {},
        # Add
        {
            'reagent': 'anhydrous Et2O',
            'volume': 200.0,
            'stir': False,
        },
        # HeatChill
        {
            'temp': 34.5,
            'time': 43200.0,
            'stir_speed': 200.0,
        },
        # Filter
        {
            'filter_vessel': 'filter',
        },
        # WashSolid
        {
            'solvent': 'hexanes-Et2O',
            'volume': 10.0,
            'repeat': 6,
        },
        # Dry
        {},
    ],
}
