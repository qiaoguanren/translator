from chemputerxdl.steps import *
from xdl.steps import *
from synthreader.finishing.constants import DEFAULT_SLOW_ADDITION_DISPENSE_SPEED

ORGSYN_V95P0080_B_TEXT = '''A 250-mL, two-necked, round-bottomed flask (Note 2) is equipped with a 1-cm, Teflon-coated magnetic stir bar and rubber septa, through one of which a needle connected to a manifold under a positive pressure of dry nitrogen is inserted. One septum is removed and the flask is charged sequentially with N,N-dibenzyl-O-pivaloylhydroxylamine (1, 7.55 g, 25.4 mmol, 1.2 equiv), copper(II) acetate (38 mg, 0.21 mmol, 0.010 equiv), (S)-DTBM-SEGPHOS (274 mg, 0.23 mmol, 0.011 equiv), triphenylphosphine (61 mg, 0.46 mmol, 0.011 equiv), and trans-β-methylstyrene (2.50 g, 2.75 mL, 21.1 mmol, 1 equiv) under nitrogen flow (Figure 4) (Note 8).

The septum is reattached to the flask, and THF (21 mL) (Note 9) is added by syringe. The flask is submerged in a room-temperature (23 °C) water bath such that the solvent level is barely below the water surface. Once the mixture has become homogeneous, using a 6-mL plastic syringe, dimethoxy(methyl)silane (5.22 mL, 4.49 g, 42.3 mmol, 2 equiv) (Note 10) is added dropwise over 10 min, during which time the color of the solution gradually changes from blue to green to bright yellow to orange (Figure 5).

At this time, the reaction flask is removed from the water bath and allowed to stir for an additional 12 h (Note 11). The septum is removed and saturated aqueous sodium bicarbonate (50 mL) is slowly added, followed by the addition of ethyl acetate (50 mL). After transferring the mixture to a 250-mL separatory funnel, the organic layer is separated and retained, and the aqueous layer is extracted with additional ethyl acetate (2 × 50 mL). The combined organic layers are concentrated with the aid of a rotary evaporator (35 °C water bath temperature, 50 mmHg) to afford a heterogeneous yellow-green mixture. This material is purified by flash column chromatography (Note 12) to yield 2 as a colorless, viscous oil (5.72 g, 86%) in 98% enantiomeric excess (Figure 6) (Note 13).'''

ORGSYN_V95P0080_B_INFO = {
    'text': ORGSYN_V95P0080_B_TEXT,
    'name': 'orgsyn_v95p0080_b',
    'reagents': {
        'N,N-dibenzyl-O-pivaloylhydroxylamine': {
            'quantities': ['7.55 g', '25.4 mmol', '1.2 equiv'],
        },
        'copper(II)acetate': {
            'quantities': ['38 mg', '0.21 mmol', '0.010 equiv'],
        },
        '(S)-DTBM-SEGPHOS': {
            'quantities': ['274 mg', '0.23 mmol', '0.011 equiv'],
        },
        'triphenylphosphine': {
            'quantities': ['61 mg', '0.46 mmol', '0.011 equiv'],
        },
        'trans-β-methylstyrene': {
            'quantities': ['2.50 g', '2.75 mL', '21.1 mmol', '1 equiv'],
        },
        'THF': {
            'quantities': ['21 mL'],
        },
        'the water': {
            'quantities': [],
        },
        'dimethoxy(methyl)silane': {
            'quantities': ['5.22 mL', '4.49 g', '42.3 mmol', '2 equiv'],
        },
        'the color': {
            'quantities': [],
        },
        'saturated aqueous sodium bicarbonate': {
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
            'mass': 7.55,
            'stir': False,
        },
        # Add
        {
            'reagent': 'copper(II)acetate',
            'mass': 0.038,
            'stir': False,
        },
        # Add
        {
            'reagent': '(S)-DTBM-SEGPHOS',
            'mass': 0.274,
            'stir': False,
        },
        # Add
        {
            'reagent': 'triphenylphosphine',
            'mass': 0.061,
            'stir': False,
        },
        # Add
        {
            'reagent': 'trans-β-methylstyrene',
            'volume': 2.75,
            'stir': False,
        },
        # Add
        {
            'reagent': 'THF',
            'volume': 21.0,
            'dispense_speed': DEFAULT_SLOW_ADDITION_DISPENSE_SPEED,
            'stir': True,
        },
        # HeatChillToTemp
        {
            'temp': 23.0,
        },
        # Add
        {
            'reagent': 'dimethoxy(methyl)silane',
            'volume': 5.22,
            'time': 600.0,
            'stir': True,
        },
        # Stir
        {
            'time': 43200.0,
        },
        # Add
        {
            'reagent': 'saturated aqueous sodium bicarbonate',
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
