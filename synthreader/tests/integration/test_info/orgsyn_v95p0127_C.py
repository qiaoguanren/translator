from chemputerxdl.steps import *
from xdl.steps import *
from synthreader.finishing.constants import DEFAULT_SLOW_ADDITION_DISPENSE_SPEED

ORGSYN_V95P0127_C_TEXT = '''To the dry and argon-flushed 1 L flask, containing the solid pyridine-3-ylzinc pivalate (27.2 g, 32.6 mmol, 1.20 mmol g-1, 1.15 equiv), a 5×2-cm Teflon-coated magnetic stirring bar and a septum, is added dry THF (65 mL, 0.44 M). Ethyl 4-bromobenzoate (4.6 mL, 6.45 g, 28.2 mmol, 1 equiv) (Note 17) is added via syringe. The septum is temporarily removed and PEPPSI-IPr (193 mg, 0.28 mmol, 1 mol%)2 added, after which the septum is reconnected and the flask flushed with argon. The red solution is stirred for 2 h at room temperature (25 °C) under an atmosphere of argon (Note 18). Then sat. aq. NH4Cl (50 mL) is added and the aqueous layer is extracted with EtOAc (3 × 70 mL). The combined organic phases are dried (12 g MgSO4). After filtration and evaporation of the solvent in vacuo, purification by column chromatography (hexane:EtOAc:NEt3 = 50:10:1 → 50:25:1) (Note 19) afforded ethyl 4-(pyridin-3-yl)benzoate (6.02 g, 26.5 mmol, 94%) as a yellow solid (Notes 20, 21, and 22).'''

ORGSYN_V95P0127_C_INFO = {
    'text': ORGSYN_V95P0127_C_TEXT,
    'name': 'orgsyn_v95p0127_c',
    'reagents': {
        'the solid pyridine-3-ylzinc pivalate': {
            'quantities': [],
        },
        'dry THF': {
            'quantities': ['65 mL', '0.44 M'],
        },
        'ethyl 4-bromobenzoate': {
            'quantities': ['4.6 mL', '6.45 g', '28.2 mmol', '1 equiv'],
        },
        'PEPPSI-IPr': {
            'quantities': ['193 mg', '0.28 mmol', '1 mol %'],
        },
        'aqueous NH4Cl': {
            'quantities': ['50 mL'],
        },
        'EtOAc': {
            'quantities': ['3 × 70 mL'],
        },
        'ethyl 4-(pyridin-3-yl)benzoate (94 %)': {
            'quantities': ['6.02 g', '26.5 mmol', '94 %'],
        },
    },
    'steps': [
        Add,
        Add,
        Add,
        HeatChill,
        Add,
        Separate,
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
        # Add
        {
            'vessel': 'reactor',
        },
        # HeatChill
        {
            'vessel': 'reactor',
        },
        # Add
        {
            'vessel': 'reactor',
        },
        # Separate
        {
            'from_vessel': 'reactor',
            'separation_vessel': 'separator',
            'to_vessel': 'rotavap',
            'through': 'MgSO4',
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
            'reagent': 'dry THF',
            'volume': 65.0,
            'stir': False,
        },
        # Add
        {
            'reagent': 'ethyl 4-bromobenzoate',
            'volume': 4.6,
            'dispense_speed': DEFAULT_SLOW_ADDITION_DISPENSE_SPEED,
            'stir': True,
        },
        # Add
        {
            'reagent': 'PEPPSI-IPr',
            'mass': 0.193,
            'stir': True,
        },
        # HeatChill
        {
            'temp': 25.0,
            'time': 7200.0,
        },
        # Add
        {
            'reagent': 'aqueous NH4Cl',
            'volume': 50.0,
            'stir': True,
        },
        # Separate
        {
            'purpose': 'extract',
            'product_bottom': False,
            'solvent': 'EtOAc',
            'solvent_volume': 70.0,
            'n_separations': 3,
        },
        # Evaporate
        {
            'time': 1800,
            'mode': 'auto',
        },
        # RunColumn
        {},
    ],
}
