from chemputerxdl.steps import *
from xdl.steps import *

ORGSYN_V81P0262_TEXT = '''A flame-dried, 200-mL, three-necked, round-bottomed flask is equipped with two glass stoppers, a vacuum-jacketed Dean-Stark trap topped with a reflux condenser fitted with a nitrogen inlet, and a Teflon-coated magnetic stirring bar. The reaction vessel is charged with 4-phenylbutyric acid (4.92 g, 30 mmol) (Note 1), boric acid (0.020 g, 0.30 mmol) (Note 2), and 88 mL of toluene (Note 3). To the stirred colorless reaction mixture is added benzylamine (3.32 g, 31 mmol) (Note 4) in one portion. The reaction mixture is heated at reflux for 16 hr and ca. 0.6 mL of water is collected in the Dean-Stark trap (Notes 5, 6, 7, 8). The mixture is allowed to cool to ambient temperature and then is poured with stirring into 500 mL of hexanes leading to the immediate precipitation of a white solid. Stirring is continued for an additional 30 min and then the precipitate is filtered off with suction through a sintered glass filter funnel. The collected solid is successively washed with two 60-mL portions of hexanes and two 60-mL portions of distilled water (Note 9) and then is dried in vacuo at room temperature for 12 hr to afford 6.90 g (91%) of N-benzyl-4-phenylbutyramide as a white solid (Notes 10, 11).'''

ORGSYN_V81P0262_INFO = {
    'text': ORGSYN_V81P0262_TEXT,
    'name': 'orgsyn_v81p0262',
    'reagents': {
        '4-phenylbutyric acid': {
            'quantities': ['4.92 g', '30 mmol'],
        },
        'boric acid': {
            'quantities': ['0.020 g', '0.30 mmol'],
        },
        'toluene': {
            'quantities': ['88 mL'],
        },
        'benzylamine': {
            'quantities': ['3.32 g', '31 mmol'],
        },
        'water': {
            'quantities': ['0.6 mL'],
        },
        'hexanes': {
            'quantities': ['500 mL', '60 mL'],
        },
        'distilled water': {
            'quantities': ['60 mL'],
        },
        'n-benzyl-4-phenylbutyramide (91 %)': {
            'quantities': ['6.90 g', '91 %'],
        },
    },
    'steps': [
        Add,
        Add,
        Add,
        Add,
        HeatChill,
        HeatChillToTemp,
        Add,
        Stir,
        Filter,
        WashSolid,
        WashSolid,
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
        # Add
        {
            'vessel': 'reactor',
        },
        # HeatChill
        {
            'vessel': 'reactor',
        },
        # HeatChillToTemp
        {
            'vessel': 'reactor',
        },
        # Add
        {
            'vessel': 'filter',
        },
        # Transfer
        {
            'from_vessel': 'reactor',
            'to_vessel': 'filter',
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
            'reagent': '4-phenylbutyric acid',
            'mass': 4.92,
            'stir': False,
        },
        # Add
        {
            'reagent': 'boric acid',
            'mass': 0.02,
            'stir': False,
        },
        # Add
        {
            'reagent': 'toluene',
            'volume': 88.0,
            'stir': False,
        },
        # Add
        {
            'reagent': 'benzylamine',
            'mass': 3.32,
            'stir': True,
        },
        # HeatChill
        {
            'temp': 110.6,
            'time': 57600.0,
        },
        # HeatChillToTemp
        {
            'temp': 25.0,
            'active': False,
            'continue_heatchill': False,
        },
        # Add
        {
            'reagent': 'hexanes',
            'volume': 500.0,
            'stir': False,
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Stir
        {
            'time': 1800.0,
        },
        # Filter
        {
            'filter_vessel': 'filter',
        },
        # WashSolid
        {
            'solvent': 'hexanes',
            'volume': 60.0,
            'repeat': 2,
        },
        # WashSolid
        {
            'solvent': 'distilled water',
            'volume': 60.0,
            'repeat': 2,
        },
        # Dry
        {
            'time': 43200.0,
            'temp': 25.0,
        },
    ],
}
