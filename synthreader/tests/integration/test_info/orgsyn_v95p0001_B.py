from chemputerxdl.steps import *
from xdl.steps import *
from synthreader.finishing.constants import (
    DEFAULT_AUTO_EVAPORATION_TIME_LIMIT,  DEFAULT_SLOW_ADDITION_DISPENSE_SPEED)

ORGSYN_V95P0001_B_TEXT = '''An oven-dried, 500-mL, three-necked round-bottomed flask is equipped with a Teflon-coated magnetic stir bar (oval, 30 x 16 mm) and the side neck is fitted with a glass gas inlet adapter connected to a vacuum/nitrogen manifold. The other side neck is capped with a glass stopper, and the center with a rubber septum (Figure 3). The flask is charged with 1 (6.19 g, 34.9 mmol) and copper(I) iodide (1.33 g, 6.98 mmol, 0.2 equiv) (Note 17). The flask is evacuated and backfilled with N2 three times. To the flask are added cinnamaldehyde (6.6 mL, 52 mmol, 1.5 equiv) (Note 18), diisopropylamine (9.8 mL, 70 mmol, 2 equiv) (Note 19), and DMSO (175 mL) (Note 20) via syringe. The center neck is capped with a glass stopper, and the resulting mixture is stirred at 60 °C for 16 h under a gentle stream of nitrogen (Notes 21 and 22) (Figure 1). Upon cooling to room temperature, the reaction mixture is diluted with ethyl acetate (175 mL) and water (100 mL). The mixture is filtered through Celite (10 g) on a glass filter (Note 22) while washing with ethyl acetate (175 mL). The filtrate is transferred to a 1-L separatory funnel. The mixture is partitioned, and the organic layer is washed successively with water (150 mL) and brine (50 mL), and dried over anhydrous MgSO4 (15 g) for 30 min.

The organic layer is filtered through Celite (10 g) on a glass filter (Note 23) and concentrated on a rotary evaporator (35 °C, 30 mmHg). The residue is transferred to a 25-mL flask and subjected to Kugelrohr distillation (Note 24) to remove excess cinnamaldehyde. The residue is subjected to column chromatography on silica gel (Note 25). The fractions containing the product are combined and concentrated on a rotary evaporator (35 °C, 30 mmHg), and the product is dried under reduced pressure at room temperature (1.5 mmHg, 2 h) to yield 2,4-diphenylpyridine (2) as a brown solid (5.17 g, 22.4 mmol, 64%) (Figure 4) (Notes 26, 27 and 28).'''

ORGSYN_V95P0001_B_INFO = {
    'text': ORGSYN_V95P0001_B_TEXT,
    'name': 'orgsyn_v95p0001_b',
    'reagents': {
        'compound 1': {
            'quantities': ['6.19 g', '34.9 mmol'],
        },
        'copper(I)iodide': {
            'quantities': ['1.33 g', '6.98 mmol', '0.2 equiv'],
        },
        'N2': {
            'quantities': [],
        },
        'cinnamaldehyde': {
            'quantities': ['6.6 mL', '52 mmol', '1.5 equiv'],
        },
        'diisopropylamine': {
            'quantities': ['9.8 mL', '70 mmol', '2 equiv'],
        },
        'DMSO': {
            'quantities': ['175 mL'],
        },
        'ethyl acetate': {
            'quantities': ['175 mL', '175 mL'],
        },
        'water': {
            'quantities': ['100 mL', '150 mL'],
        },
        'brine': {
            'quantities': ['50 mL'],
        },
        'anhydrous MgSO4': {
            'quantities': ['15 g'],
        },
        'excess cinnamaldehyde': {
            'quantities': [],
        },
        'silica gel': {
            'quantities': [],
        },
        '2,4-diphenylpyridine': {
            'quantities': [],
        },
    },
    'steps': [
        Add,
        Add,
        Evacuate,
        Add,
        Add,
        Add,
        HeatChill,
        Add,
        Add,
        FilterThrough,
        Separate,
        Separate,
        Separate,
        FilterThrough,
        Evaporate,
        Distill,
        RunColumn,
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
        # Evacuate
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
        # Add
        {
            'vessel': 'reactor',
        },
        # Add
        {
            'vessel': 'reactor',
        },
        # FilterThrough
        {
            'from_vessel': 'reactor',
            'to_vessel': 'separator',
            'through': 'celite',
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
        # FilterThrough
        {
            'from_vessel': 'rotavap',
            'to_vessel': 'rotavap',
            'through': 'celite',
        },
        # Evaporate
        {
            'rotavap_name': 'rotavap',
        },
        # Distill
        {},
        # RunColumn
        {
            'from_vessel': 'rotavap',
            'to_vessel': 'rotavap',
            'column': 'column',
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
            'reagent': 'compound 1',
            'mass': 6.19,
            'stir': False,
        },
        # Add
        {
            'reagent': 'copper(I)iodide',
            'mass': 1.33,
            'stir': False,
        },
        # Evacuate
        {},
        # Add
        {
            'reagent': 'cinnamaldehyde',
            'volume': 6.6,
            'dispense_speed': DEFAULT_SLOW_ADDITION_DISPENSE_SPEED,
            'stir': False,
        },
        # Add
        {
            'reagent': 'diisopropylamine',
            'volume': 9.8,
            'dispense_speed': DEFAULT_SLOW_ADDITION_DISPENSE_SPEED,
            'stir': True,
        },
        # Add
        {
            'reagent': 'DMSO',
            'volume': 175.0,
            'dispense_speed': DEFAULT_SLOW_ADDITION_DISPENSE_SPEED,
            'stir': True,
        },
        # HeatChill
        {
            'temp': 60.0,
            'time': 57600.0,
        },
        # Add
        {
            'reagent': 'ethyl acetate',
            'volume': 175.0,
            'stir': True,
        },
        # Add
        {
            'reagent': 'water',
            'volume': 100.0,
            'stir': True,
        },
        # FilterThrough
        {
            'eluting_solvent': 'ethyl acetate',
            'eluting_volume': 175.0,
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
            'solvent': 'water',
            'solvent_volume': 150.0,
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
        # FilterThrough
        {},
        # Evaporate
        {
            'temp': 35,
            'pressure': 39.9966,
            'time': DEFAULT_AUTO_EVAPORATION_TIME_LIMIT,
            'mode': 'auto',
        },
        # Distill
        {},
        # RunColumn
        {},
        # Evaporate
        {
            'temp': 35,
            'pressure': 39.9966,
        },
        # Dry
        {},
    ],
}
