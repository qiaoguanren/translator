from chemputerxdl.steps import *
from xdl.steps import *

ORGSYN_V95P0097_A_TEXT = '''A 1000 mL, double-necked, round-bottomed flask is charged with a Teflon-coated magnetic stir bar (3 cm × 1 cm). To this flask are added biphenyl-2-carboxylic acid 1 (7.93 g, 40 mmol, 1 equiv) (Note 2), potassium peroxydisulfate (21.6 g, 80 mmol, 2 equiv) (Note 3), and silver nitrate (68 mg, 0.01 equiv) (Note 4), followed by water (200 mL) (Note 5) and acetonitrile (200 mL) (Note 6) under an air atmosphere. The flask is equipped with a water-cooling condenser (Note 7) (Figure 1) and a glass stopper. After stirring at 50 °C for 27 h (600 rpm) (Note 8), the reaction mixture is cooled to 23 °C (Figure 2). The reaction mixture is extracted with dichloromethane (3 x 200 mL) (Note 9) (Figure 3) and the combined organic extracts are concentrated on a rotary evaporator under reduced pressure to obtain an orange solid (Figure 4).

The residue is dissolved in ethyl acetate (50 mL) (Note 10), and the suspension is filtered through a short pad of silica gel (Note 11) (Figures 5 and 6) with the aid of ethyl acetate (100 mL). The organic solution is washed with 1 M NaOH solution (2 x 75 mL), followed by saturated NaCl solution (75 mL) (Figures 7, 8 and 9). The combined aqueous layers are back-extracted with ethyl acetate (100 mL). The combined organic extracts are dried over Na2SO4 (50 g) and filtered through cotton wool. The filtrate is concentrated on a rotary evaporator under reduced pressure.

The residual solid is dried in vacuo for 12 h at ambient temperature (23 °C) to yield 6H-benzo[c]chromen-6-one 2 as a pale-yellow solid (6.40 g, 82%) (Notes 12 and 13) (Figure 10).'''

ORGSYN_V95P0097_A_INFO = {
    'text': ORGSYN_V95P0097_A_TEXT,
    'name': 'orgsyn_v95p0097_a',
    'reagents': {
        'biphenyl-2-carboxylic acid 1': {
            'quantities': ['7.93 g', '40 mmol', '1 equiv'],
        },
        'potassium peroxydisulfate': {
            'quantities': ['21.6 g', '80 mmol', '2 equiv'],
        },
        'silver nitrate': {
            'quantities': ['68 mg', '0.01 equiv'],
        },
        'water': {
            'quantities': ['200 mL'],
        },
        'acetonitrile': {
            'quantities': ['200 mL'],
        },
        'dichloromethane': {
            'quantities': ['3 x 200 mL'],
        },
        'ethyl acetate': {
            'quantities': ['50 mL', '100 mL', '100 mL'],
        },
        '1 M NaOH solution': {
            'quantities': ['2 x 75 mL'],
        },
        'saturated NaCl solution': {
            'quantities': ['75 mL'],
        },
        'Na2SO4': {
            'quantities': ['50 g'],
        },
        '6H-benzo [ c ] chromen-6-one 2': {
            'quantities': [],
        },
    },
    'steps': [
        Add,
        Add,
        Add,
        Add,
        Add,
        HeatChill,
        HeatChillToTemp,
        Separate,
        Evaporate,
        Dissolve,
        FilterThrough,
        Separate,
        Separate,
        Separate,
        FilterThrough,
        Evaporate,
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
        # Separate
        {
            'from_vessel': 'reactor',
            'separation_vessel': 'separator',
            'to_vessel': 'rotavap',
        },
        # Evaporate
        {
            'rotavap_name': 'rotavap',
        },
        # Dissolve
        {
            'vessel': 'rotavap',
        },
        # FilterThrough
        {
            'from_vessel': 'rotavap',
            'to_vessel': 'separator',
        },
        # Separate
        {
            'from_vessel': 'separator',
            'separation_vessel': 'separator',
            'to_vessel': 'separator',
            'waste_phase_to_vessel': 'buffer_flask1',
        },
        # Separate
        {
            'from_vessel': 'separator',
            'separation_vessel': 'separator',
            'to_vessel': 'rotavap',
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
            'through': 'Na2SO4',
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
        # Dry
        {
            'vessel': 'rotavap',
        },
    ],
    'properties': [
        # Add
        {
            'reagent': 'biphenyl-2-carboxylic acid 1',
            'mass': 7.93,
            'stir': False,
        },
        # Add
        {
            'reagent': 'potassium peroxydisulfate',
            'mass': 21.6,
            'stir': False,
        },
        # Add
        {
            'reagent': 'silver nitrate',
            'mass': 0.068,
            'stir': False,
        },
        # Add
        {
            'reagent': 'water',
            'volume': 200.0,
            'stir': False,
        },
        # Add
        {
            'reagent': 'acetonitrile',
            'volume': 200.0,
            'stir': True,
        },
        # HeatChill
        {
            'temp': 50.0,
            'time': 97200.0,
            'stir_speed': 600.0,
        },
        # HeatChillToTemp
        {
            'temp': 23.0,
        },
        # Separate
        {
            'purpose': 'extract',
            'product_bottom': True,
            'solvent': 'dichloromethane',
            'solvent_volume': 200.0,
            'n_separations': 3,
        },
        # Evaporate
        {
            'temp': 50,
            'pressure': 298.0,
            'time': 1800,
            'mode': 'auto',
        },
        # Dissolve
        {
            'solvent': 'ethyl acetate',
            'volume': 50.0,
        },
        # FilterThrough
        {
            'through': 'silica',
            'eluting_solvent': 'ethyl acetate',
            'eluting_volume': 100
        },
        # Separate
        {
            'purpose': 'wash',
            'product_bottom': False,
            'solvent': '1 M NaOH solution',
            'solvent_volume': 75.0,
            'n_separations': 2,
        },
        # Separate
        {
            'purpose': 'wash',
            'product_bottom': False,
            'solvent': 'saturated NaCl solution',
            'solvent_volume': 75.0,
            'n_separations': 1,
        },
        # Transfer
        {
            'volume': 'all'
        },
        # Separate
        {
            'purpose': 'extract',
            'product_bottom': False,
            'solvent': 'ethyl acetate',
            'solvent_volume': 100.0,
            'n_separations': 1,
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
        # Dry
        {
            'time': 43200.0,
            'temp': 23.0,
        },
    ],
}
