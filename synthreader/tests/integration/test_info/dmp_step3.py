from chemputerxdl.steps import *
from xdl.steps import *

DMP_STEP3_TEXT = '''A solution of menthol (31.25 g in 500 mL DCM) was added to
DMP (51 g) and stirred for 30 min. The reaction was quenched by adding 234
mL of 25% aqueous sodium thiosulfate and 234 mL of saturated aqueous sodium bicarbonate
solution and stirring vigorously for 30 min. The organic layer was extracted
with ether (700 mL), washed twice with 468 mL of saturated aqueous sodium bicarbonate solution and dried over magnesium sulfate, then evaporated to give the crude product.'''

DMP_STEP3_INFO = {
    'name': 'dmp_step3',
    'text': DMP_STEP3_TEXT,
    'reagents': {
        'menthol (31.25 g in 500 mL DCM)': {
            'quantities': ['31.25 g'],
        },
        'DCM': {
            'quantities': ['500 mL'],
        },
        'DMP': {
            'quantities': ['51 g'],
        },
        '25 % aqueous sodium thiosulfate': {
            'quantities': ['234 mL'],
        },
        'saturated aqueous sodium bicarbonate solution': {
            'quantities': ['234 mL', '468 mL'],
        },
        'ether': {
            'quantities': ['700 mL'],
        },
        'magnesium sulfate': {
            'quantities': [],
        },
    },
    'steps': [
        Add,
        Add,
        Stir,
        Add,
        Add,
        Stir,
        Separate,
        Separate,
        Evaporate,
    ],
    'vessels': [
        {'vessel': 'separator'},
        {'vessel': 'separator'},
        {'vessel': 'separator'},
        {'vessel': 'separator'},
        {'vessel': 'separator'},
        {'vessel': 'separator'},
        {'from_vessel': 'separator',
         'to_vessel': 'separator',
         'separation_vessel': 'separator'},
        {'from_vessel': 'separator',
         'to_vessel': 'rotavap',
         'separation_vessel': 'separator'},
        {'rotavap_name': 'rotavap'},
    ],
}
