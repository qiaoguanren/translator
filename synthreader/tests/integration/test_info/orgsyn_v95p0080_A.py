from chemputerxdl.steps import *
from xdl.steps import *

ORGSYN_V95P0080_A_TEXT = '''A 500-mL, single-necked, round-bottomed flask (Note 2) is equipped with a 4-cm, Teflon-coated magnetic stir bar and a rubber septum, through which a needle connected to a manifold under a positive pressure of dry nitrogen is inserted. The septum is removed and the flask is charged sequentially with N,N-dibenzylhydroxylamine (21.3 g, 100 mmol, 1 equiv), 4-dimethyl-aminopyridine (12.8 g, 105 mmol, 1.05 equiv), and dichloromethane (250 mL) (Figure 1) (Note 3). The flask is resealed with the septum and is flushed with nitrogen. The suspension is stirred for 5 min and then cooled to 0 °C in an ice-water bath for 20 min.

Pivaloyl chloride (12.9 mL, 105 mmol, 1.05 equiv) is added dropwise over 5 min using a plastic 30-mL syringe (Figure 2) (Note 4). The reaction mixture is allowed to warm to room temperature (23 °C) and then stirred for an additional 6 h (Note 5). The septum is removed and saturated aqueous ammonium chloride (50 mL) is added. The mixture is transferred to a 1-L separatory funnel using dichloromethane (50 mL) and the organic phase is collected. The aqueous phase is extracted with dichloromethane (2 × 50 mL), and the combined organic layers are washed with deionized water (200 mL) and then concentrated with the aid of a rotary evaporator (30 °C, 80 mmHg) to afford a crude, colorless, heterogeneous mixture. This material is dissolved in dichloromethane (50 mL) and eluted through a pad of alumina (Note 6) to yield 1 as a white solid (27.5-28.0 g, 93-94%) (Figure 3) (Note 7).'''

ORGSYN_V95P0080_A_INFO = {
    'text': ORGSYN_V95P0080_A_TEXT,
    'name': 'orgsyn_v95p0080_a',
    'reagents': {
        'N,N-dibenzylhydroxylamine': {
            'quantities': ['21.3 g', '100 mmol', '1 equiv'],
        },
        '4-dimethyl-aminopyridine': {
            'quantities': ['12.8 g', '105 mmol', '1.05 equiv'],
        },
        'dichloromethane': {
            'quantities': ['250 mL', '50 mL', '2 × 50 mL', '50 mL'],
        },
        'pivaloyl chloride': {
            'quantities': ['12.9 mL', '105 mmol', '1.05 equiv'],
        },
        'saturated aqueous ammonium chloride': {
            'quantities': ['50 mL'],
        },
        'deionized water': {
            'quantities': ['200 mL'],
        },
    },
    'steps': [
        Add,
        Add,
        Add,
        Stir,
        HeatChill,
        Add,
        HeatChillToTemp,
        HeatChill,
        Add,
        Add,
        Separate,
        Separate,
        Evaporate,
        Dissolve,
        FilterThrough,
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
        # HeatChill
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
        # Stir
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
        # Add
        {
            'vessel': 'separator',
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
        },
        # Evaporate
        {
            'rotavap_name': 'rotavap',
        },
        # Dissolve
        {
            'vessel': 'rotavap',
        },
        # Filter
        {
            'from_vessel': 'rotavap',
            'to_vessel': 'reactor'
        },
    ],
    'properties': [
        # Add
        {
            'reagent': 'N,N-dibenzylhydroxylamine',
            'mass': 21.3,
            'stir': False,
        },
        # Add
        {
            'reagent': '4-dimethyl-aminopyridine',
            'mass': 12.8,
            'stir': False,
        },
        # Add
        {
            'reagent': 'dichloromethane',
            'volume': 250.0,
            'stir': False,
        },
        # Stir
        {
            'time': 300.0,
        },
        # HeatChill
        {
            'temp': 0.0,
            'time': 1200.0,
        },
        # Add
        {
            'reagent': 'pivaloyl chloride',
            'volume': 12.9,
            'time': 300.0,
            'stir': True,
        },
        # HeatChillToTemp
        {
            'temp': 18,
            'active': False,
            'continue_heatchill': False,
        },
        # Stir
        {
            'time': 21600.0,
        },
        # Add
        {
            'reagent': 'saturated aqueous ammonium chloride',
            'volume': 50.0,
            'stir': True,
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Add
        {
            'reagent': 'dichloromethane',
            'volume': 50.0,
            'stir': True,
        },
        # Separate
        {
            'purpose': 'extract',
            'product_bottom': True,
            'solvent': 'dichloromethane',
            'solvent_volume': 50.0,
            'n_separations': 2,
        },
        # Separate
        {
            'purpose': 'wash',
            'product_bottom': True,
            'solvent': 'deionized water',
            'solvent_volume': 200.0,
            'n_separations': 1,
        },
        # Evaporate
        {
            'temp': 30.0,
            'pressure': 106.6576,
            'time': 1800,
            'mode': 'auto',
        },
        # Dissolve
        {
            'solvent': 'dichloromethane',
            'volume': 50.0,
        },
        # Filter
        {
            'through': 'alumina',
        },
    ],
}
