from chemputerxdl.steps import *
from xdl.steps import *

ORGSYN_V80P0129_TEXT = '''A 250-mL, three-necked, round-bottomed flask, equipped with a magnetic stirring bar, thermometer and water condenser, is charged with copper(I) iodide (200 mg, 1.1 mmol) (Note 1) and hydriodic acid (57% aq, 40 mL) (Notes 2, 3). Propiolic acid (10 ml, 162 mmol) (Note 4) is added over 1 min via syringe (Note 5), during which time the reaction temperature rises to ≈100°C. The reaction mixture is immediately immersed in an oil bath, preheated with a thermostatically controlled stirrer-hotplate to 130°C (Note 6) and a gentle reflux (110°C) is reached after ≈4 min. The mixture is heated to reflux for a further 30 min, then the oil bath is removed and replaced with a room temperature water bath. The vigorously stirred reaction mixture is allowed to cool to 28°C over 15 min (Note 7), during which time a large quantity of white needles crystallizes from the reaction mixture (Note 8). The solution is stirred for a further 15 min at room temperature, then filtered through a sintered glass funnel. The crystals are washed with 3 × 70 mL of distilled water and dried with suction for ≈1 hr, then over phosphorus pentoxide in a vacuum desiccator to constant weight. Analytically and isomerically pure (E)-3-iodoprop-2-enoic acid [25.3 g (79%)] is obtained as white needles (Note 9).'''

ORGSYN_V80P0129_INFO = {
    'text': ORGSYN_V80P0129_TEXT,
    'name': 'orgsyn_v80p0129',
    'reagents': {
        'copper(I)iodide': {
            'quantities': ['200 mg', '1.1 mmol'],
        },
        'hydriodic acid': {
            'quantities': ['57 % aq', '40 mL'],
        },
        'propiolic acid': {
            'quantities': ['10 ml', '162 mmol'],
        },
        'distilled water': {
            'quantities': ['3 × 70 mL'],
        },
        'phosphorus pentoxide': {
            'quantities': [],
        },
        'isomerically pure(E)-3-iodoprop-2-enoic acid': {
            'quantities': [],
        },
    },
    'steps': [
        Add,
        Add,
        Add,
        HeatChillToTemp,
        HeatChill,
        HeatChillToTemp,
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
        # Add
        {
            'vessel': 'filter',
        },
        # HeatChillToTemp
        {
            'vessel': 'filter',
        },
        # HeatChill
        {
            'vessel': 'filter',
        },
        # HeatChillToTemp
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
            'reagent': 'copper(I)iodide',
            'mass': 0.2,
            'stir': False,
        },
        # Add
        {
            'reagent': 'hydriodic acid',
            'volume': 40.0,
            'stir': False,
        },
        # Add
        {
            'reagent': 'propiolic acid',
            'volume': 10.0,
            'time': 60.0,
            'stir': True,
        },
        # HeatChillToTemp
        {
            'temp': 130.0,
        },
        # HeatChill
        {
            'time': 1800.0,
            'temp': 100,
        },
        # HeatChillToTemp
        {
            'temp': 28,
            'active': True,
        },
        # HeatChill
        {
            'temp': 25.0,
            'time': 900.0,
        },
        # Filter
        {
            'filter_vessel': 'filter',
        },
        # WashSolid
        {
            'solvent': 'distilled water',
            'volume': 70.0,
            'repeat': 3,
        },
        # Dry
        {},
    ],
}
