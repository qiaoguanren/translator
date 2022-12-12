from chemputerxdl.steps import *
from xdl.steps import *

ALKYL_FLUOR_STEP3_TEXT = '''To N,N'-1,3-bis(2,6-diisopropylphenyl)imidazolium chloride(S2) (150 g, 353 mmol, 1.00 equiv) in 700 mL of THF in a flask at 23°C was added KOtBu (47.4 g, 423 mmol, 1.20 equiv). The reaction mixture was stirred at 23°C for 4 h. The reaction mixture was cooled to -40°C and 1M 1,1,1,2,2,2-hexachloroethane solution (423 mL, 1.20 equiv) was added. The reaction mixture was warmed to 23°C and stirred at this temperature for 24 h. The reaction mixture was cooled to -40°C  and filtered. The filter cake was washed with THF (3 x 100 mL) and toluene (6 x 100 mL) at -40°C. It was then dissolved in CH2Cl2 (500 mL) at room temperature and filtered through a pad of Celite (10 g) eluting with CH2Cl2 (3 x 50 mL). The filtrate was concentrated under reduced pressure to afford 131 g of compound S3 as a colorless solid (81% yield).'''

ALKYL_FLUOR_STEP3_INFO = {
    'name': 'alkyl_fluor_step3',
    'text': ALKYL_FLUOR_STEP3_TEXT,
    'reagents': {
        "N,N'-1,3-bis(2,6-diisopropylphenyl)imidazolium chloride(S2)": {
            'quantities': ['150 g', '353 mmol', '1.00 equiv']
        },
        'THF': {
            'quantities': ['700 mL', '3 x 100 mL'],
        },
        'KOtBu': {
            'quantities': ['47.4 g', '423 mmol', '1.20 equiv']
        },
        '1M 1,1,1,2,2,2 hexachloroethane solution': {
            'quantities': ['423 mL', '1.20 equiv']
        },
        'toluene': {
            'quantities': ['6 x 100 mL'],
        },
        'CH2Cl2': {
            'quantities': ['500 mL', '3 x 50 mL'],
        },
    },
    'steps': [
        HeatChillToTemp,
        Add,
        Add,
        Stir,
        HeatChillToTemp,
        Add,
        HeatChillToTemp,
        Stir,
        HeatChillToTemp,
        Filter,
        WashSolid,
        WashSolid,
        Dry,
        Dissolve,
        FilterThrough,
        Evaporate,
    ],
    'vessels': [
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
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
        {'from_vessel': 'filter', 'to_vessel': 'rotavap'},
        {'rotavap_name': 'rotavap'},
    ]
}
