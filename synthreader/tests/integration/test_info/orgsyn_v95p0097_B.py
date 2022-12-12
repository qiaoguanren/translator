from chemputerxdl.steps import *
from xdl.steps import *

ORGSYN_V95P0097_B_TEXT = '''A 500 mL, single-necked, round-bottomed flask is charged with a Teflon-coated magnetic stir bar (3 cm × 1 cm). Acetonitrile (60 mL), 6H-benzo[c]chromen-6-one 2 (5.89 g, 30 mmol, 1 equiv), and iodomethane (42.6 g, 18.7 mmol, 10 equiv) (Note 14) are added and stirred to form a solution. Potassium hydroxide (KOH) pellets (9.9 g, 150 mmol, 5 equiv) (Note 15) are added to the flask under an atmosphere of air. The flask is sealed with a rubber septum (Figure 11), in which is inserted a needle that is connected to air (Note 16) (Figure 12). After stirring for 24 h (600 rpm) at 23 °C (Note 17) (Figure 13), the reaction mixture is concentrated on a rotary evaporator under reduced pressure to remove solvent and excess of iodomethane (Note 18) (Figure 14). Dichloromethane (50 mL) and deionized water (50 mL) are added to the residue (Figure 15). After the mixture is partitioned, the aqueous layer is extracted with dichloromethane (3 x 50 mL), and the combined organic extracts are washed with saturated NaCl solution (100 mL) (Figure 16). The aqueous phase is back extracted with dichloromethane (50 mL). The combined organic extracts are dried over Na2SO4 (50 g) and filtered through cotton wool. The filtrate is concentrated on a rotary evaporator under reduced pressure. The residual yellow oil is purified by column chromatography (Note 19) to yield methyl 2'-methoxy-[1,1'-biphenyl]-2-carboxylate 3 as a light yellow oil (6.50 g, 89%) (Notes 20 and 21) (Figure 17).'''

ORGSYN_V95P0097_B_INFO = {
    'text': ORGSYN_V95P0097_B_TEXT,
    'name': 'orgsyn_v95p0097_b',
    'reagents': {
        'acetonitrile': {
            'quantities': ['60 mL'],
        },
        '6H-benzo [ c ] chromen-6-one 2': {
            'quantities': ['5.89 g', '30 mmol', '1 equiv'],
        },
        'iodomethane': {
            'quantities': ['42.6 g', '18.7 mmol', '10 equiv'],
        },
        'potassium hydroxide(KOH)pellets': {
            'quantities': ['9.9 g', '150 mmol', '5 equiv'],
        },
        'dichloromethane': {
            'quantities': ['50 mL', '3 x 50 mL', '50 mL'],
        },
        'deionized water': {
            'quantities': ['50 mL'],
        },
        'saturated NaCl solution': {
            'quantities': ['100 mL'],
        },
        'Na2SO4': {
            'quantities': ['50 g'],
        },
        "methyl 2'-methoxy- [ 1,1'-biphenyl ] -2-carboxylate 3": {
            'quantities': [],
        },
    },
    'steps': [
        Add,
        Add,
        Add,
        Stir,
        Add,
        HeatChill,
        Evaporate,
        Add,
        Add,
        Separate,
        Separate,
        Separate,
        Separate,
        FilterThrough,
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
        # Stir
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
        # Add
        {
            'vessel': 'rotavap',
        },
        # Separate
        {
            'from_vessel': 'rotavap',
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
            'to_vessel': 'rotavap',
            'waste_phase_to_vessel': 'separator',
        },
        # Separate
        {
            'from_vessel': 'separator',
            'separation_vessel': 'separator',
            'to_vessel': 'rotavap',
        },
        # FilterThrough
        {
            'from_vessel': 'rotavap',
            'to_vessel': 'rotavap'
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
            'reagent': 'acetonitrile',
            'volume': 60.0,
            'stir': False,
        },
        # Add
        {
            'reagent': '6H-benzo [ c ] chromen-6-one 2',
            'mass': 5.89,
            'stir': True,
        },
        # Add
        {
            'reagent': 'iodomethane',
            'mass': 42.6,
            'stir': True,
        },
        # Stir
        {
            'time': 300.0,
        },
        # Add
        {
            'reagent': 'potassium hydroxide(KOH)pellets',
            'mass': 9.9,
            'stir': True,
        },
        # HeatChill
        {
            'temp': 23.0,
            'time': 86400.0,
            'stir_speed': 600.0,
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Evaporate
        {
            'temp': 50,
            'pressure': 153.0,
            'time': 1800,
            'mode': 'auto',
        },
        # Add
        {
            'reagent': 'dichloromethane',
            'volume': 50.0,
            'stir': False,
        },
        # Add
        {
            'reagent': 'deionized water',
            'volume': 50.0,
            'stir': True,
        },
        # Separate
        {
            'purpose': 'extract',
            'product_bottom': True,
            'solvent': '',
            'n_separations': 1,
        },
        # Separate
        {
            'purpose': 'extract',
            'product_bottom': True,
            'solvent': 'dichloromethane',
            'solvent_volume': 50.0,
            'n_separations': 3,
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Separate
        {
            'purpose': 'wash',
            'product_bottom': True,
            'solvent': 'saturated NaCl solution',
            'solvent_volume': 100.0,
            'n_separations': 1,
            'through': 'Na2SO4',
        },
        # Separate
        {
            'purpose': 'extract',
            'product_bottom': True,
            'solvent': 'dichloromethane',
            'solvent_volume': 50.0,
            'n_separations': 1,
            'through': 'Na2SO4',
        },
        # FilterThrough
        {
            'through': 'cotton wool',
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
