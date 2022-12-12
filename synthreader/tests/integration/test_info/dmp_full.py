import copy

from .dmp_step1  import DMP_STEP1_INFO
from .dmp_step2 import DMP_STEP2_INFO
from .dmp_step3 import DMP_STEP3_INFO

DMP_FULL_TEXT = '\n'.join(
    [DMP_STEP1_INFO['text'], DMP_STEP2_INFO['text'], DMP_STEP3_INFO['text']])

DMP_FULL_REAGENTS = copy.deepcopy(DMP_STEP1_INFO['reagents'])
DMP_FULL_REAGENTS.update(DMP_STEP2_INFO['reagents'])
DMP_FULL_REAGENTS.update(DMP_STEP3_INFO['reagents'])

DMP_FULL_STEP_TYPES = (
    DMP_STEP1_INFO['steps'] + DMP_STEP2_INFO['steps'] + DMP_STEP3_INFO['steps'])

DMP_FULL_INFO = {
    'text': DMP_FULL_TEXT,
    'name': 'dmp_full',
    'reagents': DMP_FULL_REAGENTS,
    'steps': DMP_FULL_STEP_TYPES,
    'vessels': [
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'filter_vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},

        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {},
        {},
        {},
        {'filter_vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},

        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'from_vessel': 'filter',
         'separation_vessel': 'separator',
         'to_vessel': 'separator'},
        {'from_vessel': 'separator',
         'separation_vessel': 'separator',
         'to_vessel': 'rotavap'},
        {'rotavap_name': 'rotavap'},
    ],
    'properties': [
        # Add
        {
            'reagent': 'oxone deionized water solution',
            'volume': 650,
            'stir': True,
            'stir_speed': 600
        },
        # Add
        {
            'reagent': '2-Iodobenzoic acid',
            'mass': 50,
            'stir': True,
            'stir_speed': 600
        },
        # HeatChillToTemp
        {
            'temp': 71.5,
        },
        # Stir
        {
            'time': 3 * 60 * 60,
        },
        # HeatChillToTemp
        {
            'temp': 5,
        },
        # Stir
        {
            'time': 1.5 * 60 * 60,
            'stir_speed': 50,
        },
        # Filter
        {},
        # WashSolid
        {
            'solvent': 'water',
            'volume': 100,
            'repeat': 6,
        },
        #  WashSolid
        {
            'solvent': 'acetone',
            'volume': 100,
            'repeat': 2,
        },
        # Dry
        {
            'time': 2 * 60 * 60,
            'temp': 25,
        },
        # Add
        {
            'reagent': 'the moist solid iodinane oxide',
            'mass': 56,
            'stir': False,
        },
        # Add
        {
            'reagent': 'glacial acetic acid',
            'volume': 96,
            'stir': False,
        },
        # Add
        {
            'reagent': 'acetic anhydride',
            'volume': 192,
            'stir': True,
        },
        # HeatChillToTemp
        {
            'temp': 85,
        },
        # Stir
        {
            'time': 20 * 60,
        },
        # StopStir
        {},
        # StopHeatChill
        {},
        # Wait
        {
            'time': 24 * 60 * 60,
        },
        # Filter
        {},
        # WashSolid
        {
            'solvent': 'anhydrous ether',
            'volume': 80,
            'repeat': 3,
        },
        # Dry
        {},
        # Add
        {
            'reagent': 'DMP',
            'mass': 51,
            'stir': False,
        },
        # Add
        {
            'reagent': 'menthol (31.25 g in 500 mL DCM) DCM solution',
            'volume': 500,
            'stir': False,
        },
        # Stir
        {
            'time': 30 * 60,
        },
        # Add
        {
            'reagent': '25 % aqueous sodium thiosulfate',
            'volume': 234,
            'stir': True,
        },
        # Add
        {
            'reagent': 'saturated aqueous sodium bicarbonate solution',
            'volume': 234,
            'stir': True,
        },
        # Stir
        {
            'time': 30 * 60,
            'stir_speed': 600,
        },
        # Separate
        {
            'purpose': 'extract',
            'solvent': 'anhydrous ether',
            'solvent_volume': 700,
            'n_separations': 1,
            'product_bottom': False,
        },
        # Separate
        {
            'purpose': 'wash',
            'solvent': 'saturated aqueous sodium bicarbonate solution',
            'through': 'magnesium sulfate',
            'solvent_volume': 468,
            'n_separations': 2,
            'product_bottom': False,
        },
        # Evaporate
        {
            'temp': 50,
            'pressure': 768.5,
            'time': 30 * 60,
            'mode': 'auto',
        }
    ],
}
