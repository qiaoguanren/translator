from chemputerxdl.steps import *
from xdl.steps import *

DMP_STEP1_TEXT = '''2-Iodobenzoic acid (50.0 g, 0.20 mol) was added all at once to a solution
of Oxone (181.0 g, 0.29 mol, 1.3 equiv) in deionized water (650 mL, 0.45 M)
in a 2 L flask with vigorous stirring. The reaction mixture was warmed to 70−73 °C over 20 min and
mechanically stirred at this temperature for 3 h. The aspect of the mixture
varies consistently during the reaction. The initial thick slurry coating
the walls of the flask eventually becomes a finely dispersed, easy to stir
suspension of a small amount of solid that sedimented easily upon stopping
the stirring. The suspension was then cooled to 5 °C and left at this
temperature for 1.5 h with slow stirring. The mixture was filtered through a
medium porosity sintered-glass funnel, and the solid was repeatedly rinsed
with water (6 × 100 mL) and acetone (2 × 100 mL). The white, crystalline
solid was left to dry at rt for 2 hr.'''

DMP_STEP1_INFO = {
    'name': 'dmp_step1',
    'text': DMP_STEP1_TEXT,
    'reagents': {
        '2-Iodobenzoic acid': {
            'quantities': ['50.0 g', '0.20 mol'],
        },
        'oxone': {
            'quantities': ['181.0 g', '0.29 mol', '1.3 equiv'],
        },
        'deionized water': {
            'quantities': ['650 mL', '0.45 M'],
        },
        'water': {
            'quantities': ['6 × 100 mL'],
        },
        'acetone': {
            'quantities': ['2 × 100 mL'],
        },
    },
    'steps': [
        Add,
        Add,
        HeatChillToTemp,
        Stir,
        HeatChillToTemp,
        Stir,
        Filter,
        WashSolid,
        WashSolid,
        Dry,
    ],
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
    ]
}
