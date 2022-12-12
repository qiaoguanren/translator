from chemputerxdl.steps import *
from xdl.steps import *

ORGSYN_V95P0142_B_PARA2_TEXT = '''The filtrate is poured into a 2-L separatory funnel. MTBE (50 mL) is used to rinse the flask and ensure that no reagents are left on the side of the flask. The organic layer is separated and washed with H2O (3 x 150 mL) and saturated aqueous NaCl (2 x 250 mL). The organic layer is dried over MgSO4 (10 g) and filtered by suction using a fritted funnel. Methyl tert-butyl ether (MTBE) (50 mL) is used to wash the MgSO4 and the filtrate is concentrated by rotary evaporation into a 2-L round-bottomed flask (40 °C bath, 425-30 mmHg). The resulting oil containing 2 is transferred to a 250-mL round-bottomed flask using MTBE (10 mL), which is evaporated (40 °C bath, 425-30 mmHg) to provide the crude product (29.24 g, 89.8 mmol, 90.9%, purity <85%) (Note 7). The material is further purified by column chromatography to provide the desired compound (22.7 g, 69.8 mmol, 70.6% yield, 97.7% purity) as a pale yellow oil (Note 8 and 9).'''

ORGSYN_V95P0142_B_PARA2_INFO = {
    'text': ORGSYN_V95P0142_B_PARA2_TEXT,
    'name': 'orgsyn_v95p0142_b_para2',
    'reagents': {
        'MTBE': {
            'quantities': ['50 mL', '10 mL'],
        },
        'H2O': {
            'quantities': ['3 x 150 mL'],
        },
        'saturated aqueous NaCl': {
            'quantities': ['2 x 250 mL'],
        },
        'MgSO4': {
            'quantities': ['10 g'],
        },
        'methyl tert-butyl ether(MTBE)': {
            'quantities': ['50 mL'],
        },
        'the MgSO4': {
            'quantities': [],
        },
    },
    'steps': [
        Add,
        Separate,
        Separate,
        Separate,
        Add,
        Evaporate,
        Add,
        Evaporate,
        RunColumn,
    ],
    'vessels': [
        # Add
        {
            'vessel': 'reactor',
        },
        # Separate
        {
            'from_vessel': 'reactor',
            'to_vessel': 'separator',
            'separation_vessel': 'separator',
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
            'through': 'MgSO4',
        },
        # Add
        {
            'vessel': 'rotavap',
            'through': 'MgSO4',
        },
        # Evaporate
        {
            'rotavap_name': 'rotavap',
        },
        # Add
        {
            'vessel': 'rotavap',
        },
        # Evaporate
        {
            'rotavap_name': 'rotavap',
        },
        # RunColumn
        {
            'from_vessel': 'rotavap',
            'to_vessel': 'reactor',
            'column': 'column',
        },
    ],
    'properties': [
        # Add
        {
            'reagent': 'MTBE',
            'volume': 50.0,
            'stir': False,
        },
        # Separate
        {
            'purpose': 'extract',
            'product_bottom': False,
            'solvent': '',
            'n_separations': 1,
        },
        # Separate
        {
            'purpose': 'wash',
            'product_bottom': False,
            'solvent': 'H2O',
            'solvent_volume': 150.0,
            'n_separations': 3,
        },
        # Separate
        {
            'purpose': 'wash',
            'product_bottom': False,
            'solvent': 'saturated aqueous NaCl',
            'solvent_volume': 250.0,
            'n_separations': 2,
        },
        # Add
        {
            'reagent': 'methyl tert-butyl ether(MTBE)',
            'volume': 50.0,
            'stir': False,
        },
        # Evaporate
        {
            'temp': 40.0,
            'pressure': 303.30755,
            'time': 1800,
            'mode': 'auto',
        },
        # Add
        {
            'reagent': 'MTBE',
            'volume': 10.0,
            'stir': False,
        },
        # Evaporate
        {
            'temp': 40.0,
            'pressure': 303.30755,
            'time': 1800,
            'mode': 'auto',
        },
        # RunColumn
        {},
    ],
}
