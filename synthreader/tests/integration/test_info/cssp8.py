from chemputerxdl.steps import *
from xdl.steps import *

CSSP8_TEXT = '''A 250 ml round bottomed flask with a sidearm was charged with Cu2O (3.64 g 25.4 mmol) and a stirrer bar. The round bottomed flask was evacuated and flushed with argon. Benzene (150 ml) was added via cannula and trifluoromethanesulphonic anhydride (10.0 g 35.4 mmol) was syringed into the stirred suspension. The reaction mixture was refluxed for several hours (overnight) with a double surface water condenser attached and argon gently passing across the top of the condenser. The solution gradually changed colour from bright red to a "grey" solution. The hot solution was filtered through a very small amount of dry Celite on a wide frit (we use a 5 cm diameter), to remove any insoluble matter. On cooling a white solid precipitated from the solution. The solvent was removed by filtration and the off-white solid was washed with benzene (2 x 20 ml). The solid was dried in vacuo and stored in an inert atmosphere (argon glovebox). Yield close to quantitative.'''

CSSP8_INFO = {
    'text': CSSP8_TEXT,
    'name': 'cssp8',
    'reagents': {
        'Cu2O': {
            'quantities': ['3.64 g', '25.4 mmol'],
        },
        'benzene': {
            'quantities': ['150 ml'],
        },
        'trifluoromethanesulphonic anhydride': {
            'quantities': ['10.0 g', '35.4 mmol'],
        },
        'water': {
            'quantities': [],
        },
        'benzene': {
            'quantities': ['2 x 20 ml'],
        },
    },
    'steps': [
        Add,
        Evacuate,
        Add,
        Add,
        HeatChill,
        FilterThrough,
        Filter,
        WashSolid,
        Dry,
    ],
    'vessels': [
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
        # Add
        {
            'vessel': 'filter',
        },
        # HeatChill
        {
            'vessel': 'filter',
        },
        # FilterThrough
        {
            'from_vessel': 'filter',
            'to_vessel': 'filter',
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
            'reagent': 'Cu2O',
            'mass': 3.64,
            'stir': False,
        },
        # Evacuate
        {},
        # Add
        {
            'reagent': 'benzene',
            'volume': 150.0,
            'stir': False,
        },
        # Add
        {
            'reagent': 'trifluoromethanesulphonic anhydride',
            'mass': 10.0,
            'stir': True,
        },
        # HeatChill
        {
            'temp': 80.1,
            'time': 60 * 60 * 16, # 16 hours (overnight)
        },
        # FilterThrough
        {
            'through': 'celite',
        },
        # Filter
        {
            'filter_vessel': 'filter',
        },
        # WashSolid
        {
            'solvent': 'benzene',
            'repeat': 2,
        },
        # Dry
        {},
    ],
}
