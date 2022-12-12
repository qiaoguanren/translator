from chemputerxdl.steps import *
from xdl.steps import *

ALKYL_FLUOR_STEP1_TEXT = '''In air, to a solution of 2,6-diisopropylaniline (197 g, 1.00 mol, 2.00 equiv) and HOAc (1.0 mL, 0.018 mol, 0.035 equiv) in 250 mL of MeOH at 50°C in a flask was added a solution of glyoxal (73 g, 0.50 mol, 1.0 equiv) in 250 mL of MeOH. The reaction mixture was stirred at 50°C for 15 min and then stirred at 23°C for 10 h. The reaction mixture was filtered. The filter cake was washed with MeOH (3 x 100 mL) and dried in vacuo to afford 169 g of compound S1 as a yellow solid (90% yield) -->'''

ALKYL_FLUOR_STEP1_INFO = {
    'name': 'alkyl_fluor_step1',
    'text': ALKYL_FLUOR_STEP1_TEXT,
    'reagents': {
        '2,6-diisopropylaniline': {
            'quantities': ['197 g'],
        },
        'HOAc': {
            'quantities': ['1.0 mL'],
        },
        'MeOH': {
            'quantities': ['250 mL', '250 mL', '3 x 100 mL'],
        },
        'glyoxal': {
            'quantities': ['73 g'],
        },
    },
    'steps': [
        Add,
        HeatChillToTemp,
        Add,
        Stir,
        HeatChill,
        Filter,
        WashSolid,
        Dry
    ],
    'vessels': [
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'filter_vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
    ]
}
