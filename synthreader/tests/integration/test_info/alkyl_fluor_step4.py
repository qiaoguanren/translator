from chemputerxdl.steps import *
from xdl.steps import *

ALKYL_FLUOR_STEP4_TEXT = '''Under nitrogen atmosphere, potassium fluoride (380 mg, 6.45 mmol, 3.00 equiv.), potassium tetrafluoroborate (1.35 g, 10.75 mmol, 5.00 equiv.) and 1,3-bis(2,6-diisopropylphenyl)-2- chloroimidazolium chloride (1) (1.00 g, 2.15 mmol, 1.00 equiv.) were added to a 25 mL pressure flask and dried for 2 hours. The solids were then suspended in 18 mL acetonitrile. The mixture was heated at 80 °C for 16 hours with vigorous stirring. The reaction mixture was cooled to room temperature, then filtered through a pad of Celite, eluting with dichloromethane (3 × 15 mL). The filtrate was concentrated in vacuo, after which the residue was dissolved in dichloromethane (30 mL) and filtered again through Celite, eluting with dichloromethane (3 × 15 mL). It was then concentrated in vacuo and the residual solid was washed with diethyl ether (3 × 15 mL) to afford the title compound as a colorless solid.'''

ALKYL_FLUOR_STEP4_INFO = {
    'name': 'alkyl_fluor_step4',
    'text': ALKYL_FLUOR_STEP4_TEXT,
    'reagents': {
        'potassium fluoride': {
            'quantities': ['380 mg', '6.45 mmol', '3.00 equiv']
        },
        'potassium tetrafluoroborate': {
            'quantities': ['1.35 g', '10.75 mmol', '5.00 equiv'],
        },
        '1,3-bis(2,6-diisopropylphenyl)-2- chloroimidazolium chloride': {
            'quantities': ['1.00 g', '2.15 mmol', '1.00 equiv']
        },
        'acetonitrile': {
            'quantities': ['18 mL']
        },
        'dichloromethane': {
            'quantities': ['3 × 15 mL', '30 mL'],
        },
        'diethyl ether': {
            'quantities': ['3 × 15 mL']
        }
    },
    'steps': [
        Add,
        Add,
        Add,
        Dry,
        Add,
        HeatChill,
        HeatChillToTemp,
        FilterThrough,
        Evaporate,
        Dissolve,
        FilterThrough,
        Evaporate,
        WashSolid,
    ],
    'vessels': [
        {'vessel': 'reactor'},
        {'vessel': 'reactor'},
        {'vessel': 'reactor'},
        {'vessel': 'reactor'},
        {'vessel': 'reactor'},
        {'vessel': 'reactor'},
        {'vessel': 'reactor'},
        {'from_vessel': 'reactor', 'to_vessel': 'rotavap'},
        {'rotavap_name': 'rotavap'},
        {'vessel': 'rotavap'},
        {'from_vessel': 'rotavap', 'to_vessel': 'rotavap'},
        {'rotavap_name': 'rotavap'},
        {'vessel': 'rotavap'},
    ],
}
