from chemputerxdl.steps import *
from xdl.steps import *
from synthreader.finishing.constants import DEFAULT_SLOW_ADDITION_DISPENSE_SPEED

ORGSYN_V87P0192_TEXT = '''A single-necked, 250-mL round-bottomed flask equipped with a Teflon-coated magnetic stir bar (33 × 15 mm, egg-shaped) is charged with trans-4-methoxy-3-buten-2-one (15.3 mL, 15.0 g, 0.135 mol, 1.0 equiv), ethanol (120 mL) (Note 1), and deionized water (30 mL) (Note 1) under an atmosphere of air. Glacial acetic acid (17.5 M, 0.9 mL, 0.944 g, 0.015 mol, 0.11 equiv) (Note 1) is added via syringe to the reaction mixture. A reflux condenser is fitted to the round-bottomed flask and the resulting homogeneous pale yellow reaction mixture is heated gently to reflux, with stirring, for 48 h ensuring that the temperature of the oil bath is kept at 77 °C. Over this time, the reaction remains homogeneous, and turns orange in color (Note 2). The oil bath is removed, and the reaction flask is allowed to cool to room temperature, and then placed in a -20 °C freezer for 18 h to crystallize the product. The resulting mixture is then vacuum filtered while cold through a sintered-glass funnel (Note 3) to collect the yellow needles (Note 4), which are rinsed with pre-cooled (0 °C) anhydrous diethyl ether (4 × 50 mL) (Notes 1, 5 and 6). The crude product (6.4-6.6 g; 70-72%; mp = 161-165 °C) is recrystallized by dissolving the yellow needles in hot ethanol (200 mL, 78 °C), allowing the solution to cool to room temperature, then storing it in a -20 °C freezer for 18 h. The resulting mixture is then vacuum filtered while cold, through a sintered-glass funnel (Note 3), and the pale yellow needles are rinsed with pre-cooled (0 °C) anhydrous ether (4 × 50 mL) (Note 7). The 1,3,5-triacetylbenzene obtained is air dried overnight to provide 5.6-5.9 g of product (61-64%) as pale yellow needles (mp 163-165 °C) (Notes 8 and 9).'''

ORGSYN_V87P0192_INFO = {
    'text': ORGSYN_V87P0192_TEXT,
    'name': 'orgsyn_v87p0192',
    'reagents': {
        'trans-4 methoxy-3-buten-2-one': {
            'quantities': ['15.3 mL', '15.0 g', '0.135 mol', '1.0 equiv'],
        },
        'ethanol': {
            'quantities': ['120 mL', '200 mL', '78 °C'],
        },
        'deionized water': {
            'quantities': ['30 mL'],
        },
        'glacial acetic acid': {
            'quantities': ['17.5 M', '0.9 mL', '0.944 g', '0.015 mol', '0.11 equiv'],
        },
        'anhydrous diethyl ether': {
            'quantities': ['0 °C', '4 × 50 mL'],
        },
        'the 1,3,5-triacetylbenzene obtained': {
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
        HeatChill,
        Filter,
        WashSolid,
        Dry,
        Dissolve,
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
        # Add
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
        # Dissolve
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
            'reagent': 'trans-4 methoxy-3-buten-2-one',
            'volume': 15.3,
            'stir': False,
        },
        # Add
        {
            'reagent': 'ethanol',
            'volume': 120.0,
            'stir': True,
        },
        # Add
        {
            'reagent': 'deionized water',
            'volume': 30.0,
            'stir': True,
        },
        # Add
        {
            'reagent': 'glacial acetic acid',
            'volume': 0.9,
            'dispense_speed': DEFAULT_SLOW_ADDITION_DISPENSE_SPEED,
            'stir': True,
        },
        # HeatChill
        {
            'temp': 77.0,
            'time': 172800.0,
        },
        # HeatChillToTemp
        {
            'temp': 25,
            'active': False,
            'continue_heatchill': False,
        },
        # HeatChill
        {
            'temp': -20.0,
            'time': 64800.0,
        },
        # Filter
        {
            'filter_vessel': 'filter',
        },
        # WashSolid
        {
            'solvent': 'anhydrous diethyl ether',
            'volume': 50.0,
            'temp': 0.0,
            'repeat': 4,
        },
        # Dry
        {},
        # Dissolve
        {
            'solvent': 'ethanol',
            'volume': 200.0,
            'temp': 78.0,
        },
        # HeatChillToTemp
        {
            'temp': 25,
            'active': False,
            'continue_heatchill': False,
        },
        # HeatChill
        {
            'temp': -20.0,
            'time': 64800.0,
        },
        # Filter
        {
            'filter_vessel': 'filter',
        },
        # WashSolid
        {
            'solvent': 'anhydrous diethyl ether',
            'volume': 50.0,
            'temp': 0.0,
            'repeat': 4,
        },
        # Dry
        {
            'time': 57600.0,
        },
    ],
}
