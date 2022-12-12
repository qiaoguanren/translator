from chemputerxdl.steps import *
from xdl.steps import *
from synthreader.finishing.constants import DEFAULT_SLOW_ADDITION_DISPENSE_SPEED

ORGSYN_V95P0080_C_TEXT = '''A 250-mL, two-necked, round-bottomed flask (Note 2) is equipped with a 1-cm, Teflon-coated magnetic stir bar and two rubber septa, through one of which a needle connected to a manifold under dry nitrogen is inserted. One septum is removed and the flask is charged sequentially with N,N-dibenzyl-O-pivaloylhydroxylamine (1, 9.09 g, 30.6 mmol, 1.2 equiv), copper(II) acetate (46 mg, 0.25 mmol, 0.010 equiv), (S)-DTBM-SEGPHOS (330 mg, 0.28 mmol, 0.011 equiv), triphenylphosphine (74 mg, 0.28 mmol, 0.011 equiv), and 2,3,3-trimethyl-1-butene (2.50 g, 3.55 mL, 25.5 mmol, 1 equiv) (Notes 8 and 14) under nitrogen flow. The flask is resealed with the septum, THF (25 mL) (Note 9) is added by syringe, and the flask is partially submerged in an oil bath heated to 40 °C (Note 9). Once the mixture has become homogeneous, using a 6-mL plastic syringe, dimethoxy(methyl)silane (6.27 mL, 5.41 g, 50.9 mmol, 2 equiv) (Note 10) is added dropwise over 10 min, during which the color of the solution gradually changes from blue to green to bright yellow to orange. The reaction mixture is allowed to stir for additional 12 h at 40 °C. The reaction is cooled to room temperature (23 °C), the septum is removed and saturated aqueous sodium carbonate (50 mL) is slowly added, followed by the addition of ethyl acetate (50 mL). After transferring the mixture to a 250-mL separatory funnel, the organic layer is separated and retained, and the aqueous layer is extracted with additional ethyl acetate (2 × 50 mL). The combined organic layers are concentrated with the aid of a rotary evaporator (35 °C water bath temperature, 50 mmHg) and purified by flash column chromatography (Note 15) to yield 3 as a colorless, viscous oil (6.54 g, 87%) in 90% enantiomeric excess (Figure 7) (Note 16).'''

ORGSYN_V95P0080_C_INFO = {
    'text': ORGSYN_V95P0080_C_TEXT,
    'name': 'orgsyn_v95p0080_c',
    'reagents': {
        'N,N-dibenzyl-O-pivaloylhydroxylamine': {
            'quantities': ['9.09 g', '30.6 mmol', '1.2 equiv'],
        },
        'copper(II)acetate': {
            'quantities': ['46 mg', '0.25 mmol', '0.010 equiv'],
        },
        '(S)-DTBM-SEGPHOS': {
            'quantities': ['330 mg', '0.28 mmol', '0.011 equiv'],
        },
        'triphenylphosphine': {
            'quantities': ['74 mg', '0.28 mmol', '0.011 equiv'],
        },
        '2,3,3-trimethyl-1-butene': {
            'quantities': ['2.50 g', '3.55 mL', '25.5 mmol', '1 equiv'],
        },
        'THF': {
            'quantities': ['25 mL'],
        },
        'dimethoxy(methyl)silane': {
            'quantities': ['6.27 mL', '5.41 g', '50.9 mmol', '2 equiv'],
        },
        'saturated aqueous sodium carbonate': {
            'quantities': ['50 mL'],
        },
        'ethyl acetate': {
            'quantities': ['50 mL', '2 × 50 mL'],
        },
    },
    'steps': [
        Add,
        Add,
        Add,
        Add,
        Add,
        Add,
        HeatChillToTemp,
        Add,
        Stir,
        HeatChillToTemp,
        Add,
        Add,
        Separate,
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
        # HeatChillToTemp
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
        # Separate
        {
            'from_vessel': 'reactor',
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
            'reagent': 'N,N-dibenzyl-O-pivaloylhydroxylamine',
            'mass': 9.09,
            'stir': False,
        },
        # Add
        {
            'reagent': 'copper(II)acetate',
            'mass': 0.046,
            'stir': False,
        },
        # Add
        {
            'reagent': '(S)-DTBM-SEGPHOS',
            'mass': 0.33,
            'stir': False,
        },
        # Add
        {
            'reagent': 'triphenylphosphine',
            'mass': 0.074,
            'stir': False,
        },
        # Add
        {
            'reagent': '2,3,3-trimethyl-1-butene',
            'volume': 3.55,
            'stir': False,
        },
        # Add
        {
            'reagent': 'THF',
            'volume': 25.0,
            'dispense_speed': DEFAULT_SLOW_ADDITION_DISPENSE_SPEED,
            'stir': True,
        },
        # HeatChillToTemp
        {
            'temp': 40.0,
        },
        # Add
        {
            'reagent': 'dimethoxy(methyl)silane',
            'volume': 6.27,
            'time': 600.0,
            'stir': True,
        },
        # Stir
        {
            'time': 43200.0,
        },
        # HeatChillToTemp
        {
            'temp': 23.0,
        },
        # Add
        {
            'reagent': 'saturated aqueous sodium carbonate',
            'volume': 50.0,
            'dispense_speed': DEFAULT_SLOW_ADDITION_DISPENSE_SPEED,
            'stir': True,
        },
        # Add
        {
            'reagent': 'ethyl acetate',
            'volume': 50.0,
            'stir': True,
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
            'purpose': 'extract',
            'product_bottom': False,
            'solvent': 'ethyl acetate',
            'solvent_volume': 50.0,
            'n_separations': 2,
        },
        # Evaporate
        {
            'temp': 35.0,
            'pressure': 66.661,
            'time': 1800,
            'mode': 'auto',
        },
        # RunColumn
        {},
    ],
}
