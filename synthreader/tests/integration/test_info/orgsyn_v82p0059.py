from chemputerxdl.steps import *
from xdl.steps import *
from synthreader.finishing.constants import DEFAULT_SLOW_ADDITION_DISPENSE_SPEED

ORGSYN_V82P0059_TEXT = '''A 1-L, three-necked, round-bottomed flask is equipped with a mechanical stirrer (Note 1), a vacuum take-off adapter attached to a nitrogen source, and a pressure equalizing dropping funnel closed with a glass stopper. The flask is flame-dried, cooled under nitrogen, and charged with tetrahydrofuran (THF) (250 mL) (Note 2) and tert-butyl isocyanide (12.4 mL, 110 mmol) (Note 3). To this homogeneous solution is added acetyl chloride (8.6 mL, 121 mmol) (Note 4) and the mixture is vigorously stirred for 15 min. A solution of 1,3-dimethylurea (24.2 g, 275 mmol) (Note 3) in 150 mL of THF is then introduced slowly and continuously through the dropping funnel. After 15-20 min, a white precipitate appears (Note 5). The reaction mixture is stirred for 14 h at room temperature, after which time the heterogeneous mixture is filtered through a Buchner funnel connected to vacuum. The white precipitate is washed with cold THF (Note 6) to remove excess urea, the acetylurea byproduct and colored impurities (Note 7). The product is dried in a vacuum oven at 50°C for 20 h to give 19-20 g (85-90%) of analytically pure product as a white powder (Notes 8-10). The hygroscopic product should be stored under nitrogen.'''

ORGSYN_V82P0059_INFO = {
    'text': ORGSYN_V82P0059_TEXT,
    'name': 'orgsyn_v82p0059',
    'reagents': {
        'tetrahydrofuran(THF)': {
            'quantities': ['250 mL'],
        },
        'tert-butyl isocyanide': {
            'quantities': ['12.4 mL', '110 mmol'],
        },
        'acetyl chloride': {
            'quantities': ['8.6 mL', '121 mmol'],
        },
        '1,3-dimethylurea': {
            'quantities': ['24.2 g', '275 mmol'],
        },
        'THF': {
            'quantities': ['150 mL'],
        },
        'urea': {
            'quantities': [],
        },
        'the acetylurea byproduct': {
            'quantities': [],
        },
    },
    'steps': [
        Dry,
        HeatChillToTemp,
        Add,
        Add,
        Add,
        Stir,
        Add,
        Stir,
        Filter,
        WashSolid,
        Dry,
    ],
    'vessels': [
        # Dry
        {
            'vessel': 'filter',
        },
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
        # Stir
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
        # Dry
        {},
        # HeatChillToTemp
        {
            'temp': 25,
        },
        # Add
        {
            'reagent': 'tetrahydrofuran(THF)',
            'volume': 250.0,
            'stir': False,
        },
        # Add
        {
            'reagent': 'tert-butyl isocyanide',
            'volume': 12.4,
            'stir': True,
        },
        # Add
        {
            'reagent': 'acetyl chloride',
            'volume': 8.6,
            'stir': True,
        },
        # Stir
        {
            'time': 900.0,
            'stir_speed': 600,
        },
        # Add
        {
            'reagent': '1,3-dimethylurea THF solution',
            'volume': 150.0,
            'dispense_speed': DEFAULT_SLOW_ADDITION_DISPENSE_SPEED,
            'stir': True,
        },
        # Stir
        {
            'time': 50400.0,
        },
        # Filter
        {
            'filter_vessel': 'filter',
        },
        # WashSolid
        {
            'solvent': 'THF',
            'temp': 10,
            'repeat': 1,
        },
        # Dry
        {
            'time': 72000.0,
            'temp': 50.0,
        },
    ],
}
