from chemputerxdl.steps import *
from xdl.steps import *

ORGSYN_V95P0001_A_TEXT = '''A 250-mL, two-necked round-bottomed flask equipped with a Teflon-coated magnetic stir bar (oval, 20 x 10 mm) is charged with acetophenone (9.33 mL, 80.0 mmol, 1 equiv) (Note 2), pyridine (18 mL, 223 mmol, 2.8 equiv) (Note 3), ethanol (40 mL) (Note 4), and hydroxylamine hydrochloride (8.33 g, 120 mmol, 1.5 equiv) (Note 5). The resulting mixture is stirred at 60 °C for 75 min (Notes 6 and 7) (Figure 1) and then cooled to 22 °C. Water (80 mL) is added, and the resulting biphasic mixture is transferred to a 500-mL separatory funnel. The mixture is partitioned, and the aqueous layer is extracted with ethyl acetate (2 x 80 mL). The organic extracts are combined, washed successively with 1 M HCl (50 mL) and brine (50 mL), and dried over anhydrous MgSO4 (10 g) for 15 min. The extracts are gravity filtered through a filter paper and concentrated on a rotary evaporator (35 °C, 30 mmHg).

The residue is transferred to a 250-mL, one-necked round-bottomed flask and dried further for 1 h under reduced pressure (1.5 mmHg, 22 °C) (Notes 8 and 9). A Teflon-coated stir bar (15 x 6 mm) is placed in the flask. To the flask are added N,N-dimethylaminopyridine (20 mg, 0.16 mmol, 0.002 equiv) (Note 10), pyridine (35 mL) (Note 2), and acetic anhydride (15 mL, 160 mmol, 2 equiv) (Note 11). The resulting mixture is stirred at room temperature (24 °C) for 1 h (Note 12). The volatile materials are removed on a rotary evaporator (45 °C, 35 mmHg). To the residue is added water (50 mL), and the mixture is transferred to a 250-mL separatory funnel. The mixture is partitioned, and the aqueous layer is extracted with ethyl acetate (2 x 50 mL). The organic extracts are combined, washed successively with 1 M HCl (50 mL) and brine (50 mL), and dried over anhydrous MgSO4 (10 g) for 15 min. The extracts are filtered through a filter paper and concentrated on a rotary evaporator (35 °C, 30 mmHg). Recrystallization of the residual white solid from ethyl acetate (Note 13) affords (E)-acetophenone O-acetyl oxime (1) as white crystals (9.41 g, 53.1 mmol, 66%) (Figure 2) (Notes 14, 15, and 16.
'''

ORGSYN_V95P0001_A_INFO = {
    'text': ORGSYN_V95P0001_A_TEXT,
    'name': 'orgsyn_v95p0001_a',
    'reagents': {
        'acetophenone': {
            'quantities': ['9.33 mL', '80.0 mmol', '1 equiv'],
        },
        'pyridine': {
            'quantities': ['18 mL', '223 mmol', '2.8 equiv', '35 mL'],
        },
        'ethanol': {
            'quantities': ['40 mL'],
        },
        'hydroxylamine hydrochloride': {
            'quantities': ['8.33 g', '120 mmol', '1.5 equiv'],
        },
        'water': {
            'quantities': ['80 mL', '50 mL'],
        },
        'ethyl acetate': {
            'quantities': ['2 x 80 mL', '2 x 50 mL'],
        },
        '1 M HCl': {
            'quantities': ['50 mL', '50 mL'],
        },
        'brine': {
            'quantities': ['50 mL', '50 mL'],
        },
        'anhydrous MgSO4': {
            'quantities': ['10 g', '10 g'],
        },
        'N,N-dimethylaminopyridine': {
            'quantities': ['20 mg', '0.16 mmol', '0.002 equiv'],
        },
        'acetic anhydride': {
            'quantities': ['15 mL', '160 mmol', '2 equiv'],
        },
        'ethyl acetate affords(E)-acetophenone O-acetyl oxime': {
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
        Separate,
        Separate,
        Separate,
        Separate,
        Evaporate,
        Dry,
        Add,
        Add,
        Add,
        HeatChill,
        Evaporate,
        Add,
        Separate,
        Separate,
        Separate,
        Separate,
        Evaporate,
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
        # Transfer
        {
            'from_vessel': 'reactor',
            'to_vessel': 'separator',
        },
        # Separate
        {
            'from_vessel': 'separator',
            'separation_vessel': 'separator',
            'to_vessel': 'buffer_flask1',
            'waste_phase_to_vessel': 'separator',
        },
        # Separate
        {
            'from_vessel': 'separator',
            'separation_vessel': 'separator',
            'to_vessel': 'separator',
        },
        # Transfer
        {
            'from_vessel': 'buffer_flask1',
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
        # Dry
        {
            'vessel': 'rotavap',
        },
        # Transfer
        {
            'from_vessel': 'rotavap',
            'to_vessel': 'reactor',
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
        # Transfer
        {
            'from_vessel': 'reactor',
            'to_vessel': 'rotavap',
        },
        # Evaporate
        {
            'rotavap_name': 'rotavap',
        },
        # Add
        {
            'vessel': 'rotavap',
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
            'to_vessel': 'buffer_flask1',
            'waste_phase_to_vessel': 'separator',
        },
        # Separate
        {
            'from_vessel': 'separator',
            'separation_vessel': 'separator',
            'to_vessel': 'separator',
        },
        # Transfer
        {
            'from_vessel': 'buffer_flask1',
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
    ],
    'properties': [
        # Add
        {
            'reagent': 'acetophenone',
            'volume': 9.33,
            'stir': False,
        },
        # Add
        {
            'reagent': 'pyridine',
            'volume': 18.0,
            'stir': True,
        },
        # Add
        {
            'reagent': 'ethanol',
            'volume': 40.0,
            'stir': True,
        },
        # Add
        {
            'reagent': 'hydroxylamine hydrochloride',
            'mass': 8.33,
            'stir': True,
        },
        # HeatChill
        {
            'temp': 60.0,
            'time': 4500.0,
        },
        # HeatChillToTemp
        {
            'temp': 22.0,
        },
        # Add
        {
            'reagent': 'water',
            'volume': 80.0,
            'stir': True,
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Separate
        {
            'purpose': 'extract',
            'product_bottom': False,
            'n_separations': 1,
        },
        # Separate
        {
            'purpose': 'extract',
            'product_bottom': False,
            'solvent': 'ethyl acetate',
            'solvent_volume': 80.0,
            'n_separations': 2,
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Separate
        {
            'purpose': 'wash',
            'product_bottom': False,
            'solvent': '1 M HCl',
            'solvent_volume': 50.0,
            'n_separations': 1,
        },
        # Separate
        {
            'purpose': 'wash',
            'product_bottom': False,
            'solvent': 'brine',
            'solvent_volume': 50.0,
            'n_separations': 1,
        },
        # Evaporate
        {
            'time': 1800,
            'mode': 'auto',
        },
        # Dry
        {},
        # Transfer
        {
            'volume': 'all',
        },
        # Add
        {
            'reagent': 'N,N-dimethylaminopyridine',
            'mass': 0.02,
            'stir': False,
        },
        # Add
        {
            'reagent': 'pyridine',
            'volume': 35.0,
            'stir': False,
        },
        # Add
        {
            'reagent': 'acetic anhydride',
            'volume': 15.0,
            'stir': True,
        },
        # HeatChill
        {
            'temp': 24.0,
            'time': 3600.0,
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Evaporate
        {
            'time': 1800,
            'mode': 'auto',
        },
        # Add
        {
            'reagent': 'water',
            'volume': 50.0,
            'stir': False,
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Separate
        {
            'purpose': 'extract',
            'product_bottom': False,
            'n_separations': 1,
        },
        # Separate
        {
            'purpose': 'extract',
            'product_bottom': False,
            'solvent': 'ethyl acetate',
            'solvent_volume': 50.0,
            'n_separations': 2,
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Separate
        {
            'purpose': 'wash',
            'product_bottom': False,
            'solvent': '1 M HCl',
            'solvent_volume': 50.0,
            'n_separations': 1,
        },
        # Separate
        {
            'purpose': 'wash',
            'product_bottom': False,
            'solvent': 'brine',
            'solvent_volume': 50.0,
            'n_separations': 1,
        },
        # Evaporate
        {
            'time': 1800,
            'mode': 'auto',
        },
    ],
}
