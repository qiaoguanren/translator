from chemputerxdl.steps import *
from xdl.steps import *
from synthreader.finishing.constants import DEFAULT_AUTO_EVAPORATION_TIME_LIMIT

ORGSYN_V87P0016_TEXT = '''A 1-L three-necked, round-bottomed flask equipped with a reflux condenser fitted with an argon inlet, a thermocouple probe (range -200 to +1370 °C) and a mechanical stirrer is charged with 2-thiophenecarboxaldehyde (11.21 g, 100.0 mmol, 1.00 equiv), K2CO3 (24.19 g, 175.0 mmol, 41.75 equiv), tosylmethylisocyanide (21.12 g, 100.0 mol, 1.00 equiv) and methanol (448 mL) (Note 1). The reaction mixture is heated at reflux (66 °C) for 4 h (Note 2). After cooling to room temperature, water (224 mL) is added and the mixture is stirred for 10 min at the same temperature. The resulting solution is transferred to a single-necked 2-L flask, and methanol is removed by rotary evaporation (45 °C, 75 mmHg). The residual liquid is transferred to a 1-L separatory funnel, and then extracted with MTBE (3 × 120 mL). The combined organic layers are washed with water (1 × 50 mL) and a saturated NaCl solution (1 × 50 mL), dried over anhydrous MgSO4, filtered, and concentrated by rotary evaporation (35 °C, 50 mmHg) (Note 3) to give a brown oil (15.31 g) as a crude product, which is vacuum distilled (60-62 °C, 0.4 mmHg) to afford the oxaozle 1 as a pale yellow oil (12.70 g, 84%) (Note 4).'''

ORGSYN_V87P0016_INFO = {
    'text': ORGSYN_V87P0016_TEXT,
    'name': 'orgsyn_v87p0016',
    'reagents': {
        '2-thiophenecarboxaldehyde': {
            'quantities': ['11.21 g', '100.0 mmol', '1.00 equiv'],
        },
        'K2CO3': {
            'quantities': ['24.19 g', '175.0 mmol', '41.75 equiv'],
        },
        'tosylmethylisocyanide': {
            'quantities': ['21.12 g', '100.0 mol', '1.00 equiv'],
        },
        'methanol': {
            'quantities': ['448 mL'],
        },
        'water': {
            'quantities': ['224 mL', '1 × 50 mL'],
        },
        'MTBE': {
            'quantities': ['3 × 120 mL'],
        },
        'saturated NaCl solution': {
            'quantities': ['1 × 50 mL'],
        },
        'anhydrous MgSO4': {
            'quantities': [],
        },
        'the oxaozle 1': {
            'quantities': [],
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
        Evaporate,
        Separate,
        Separate,
        Separate,
        Evaporate,
        Distill,
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
        # Transfer
        {
            'from_vessel': 'rotavap',
            'to_vessel': 'separator',
        },
        # Separate
        {
            'from_vessel': 'separator',
            'separation_vessel': 'separator',
            'to_vessel': 'separator',
        },
        # Separate
        {
            'from_vessel': 'separator',
            'separation_vessel': 'separator',
            'to_vessel': 'separator',
        },
        # Separate
        {
            'from_vessel': 'separator',
            'separation_vessel': 'separator',
            'to_vessel': 'rotavap',
            'through': 'anhydrous MgSO4',
        },
        # Evaporate
        {
            'rotavap_name': 'rotavap',
        },
        # Distill
        {},
    ],
    'properties': [
        # Add
        {
            'reagent': '2-thiophenecarboxaldehyde',
            'mass': 11.21,
            'stir': False,
        },
        # Add
        {
            'reagent': 'K2CO3',
            'mass': 24.19,
            'stir': False,
        },
        # Add
        {
            'reagent': 'tosylmethylisocyanide',
            'mass': 21.12,
            'stir': False,
        },
        # Add
        {
            'reagent': 'methanol',
            'volume': 448.0,
            'stir': False,
        },
        # HeatChill
        {
            'temp': 66.0,
            'time': 14400.0,
        },
        # HeatChillToTemp
        {
            'temp': 25,
        },
        # Add
        {
            'reagent': 'water',
            'volume': 224.0,
            'stir': True,
        },
        # Stir
        {
            'time': 600.0,
        },
        # Transfer
        {},
        # Evaporate
        {
            'temp': 45,
            'pressure': 99.9915,
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Separate
        {
            'purpose': 'extract',
            'product_bottom': False,
            'solvent': 'MTBE',
            'solvent_volume': 120.0,
            'n_separations': 3,
        },
        # Separate
        {
            'purpose': 'wash',
            'product_bottom': False,
            'solvent': 'water',
            'solvent_volume': 50.0,
            'n_separations': 1,
        },
        # Separate
        {
            'purpose': 'wash',
            'product_bottom': False,
            'solvent': 'saturated NaCl solution',
            'solvent_volume': 50.0,
            'n_separations': 1,
        },
        # Evaporate
        {
            'time': DEFAULT_AUTO_EVAPORATION_TIME_LIMIT,
            'temp': 35,
            'pressure': 66.661,
            'mode': 'auto',
        },
        # Distill
        {},
    ],
}
