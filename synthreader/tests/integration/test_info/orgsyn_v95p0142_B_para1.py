from chemputerxdl.steps import *
from xdl.steps import *
from synthreader.finishing.constants import DEFAULT_SLOW_ADDITION_DISPENSE_SPEED

ORGSYN_V95P0142_B_PARA1_TEXT = '''(S)-(-)-α, α-Diphenyl-2-pyrrolidinylmethanol (25.0 g, 98.8 mmol, 1.0 equiv) (Note 6) is introduced in a 1-L three-necked round-bottomed flask (equipped with a 4-cm oval Teflon-coated stir-bar, an internal thermometer, and a glass stopper) and is dissolved with THF (220 mL). To the resulting solution, imidazole (20.0 g, 294 mmol, 3.0 equiv) is added in one portion. After complete dissolution of the imidazole, the reaction mixture is cooled to 4 ºC in an ice-water bath. A 250-mL addition funnel is attached and then charged with trimethylchlorosilane (31.3 mL, 247 mmol, 2.50 equiv) via a 50 mL syringe. The TMSCl is added dropwise via the addition funnel over 20 min (Figure 1). Tetrahydrofuran (50 mL) is used to rinse the addition funnel and ensure that no reagent is left on the side of the addition funnel. The addition funnel is removed, the flask is equipped with a nitrogen inlet, and the reaction is stirred for 15 h at 23 °C under nitrogen. Methyl tert-butyl ether (MTBE) (150 mL) is added and the reaction stirred for an additional 15 min. The resultant heterogeneous mixture is filtered through a 10 cm diameter fritted funnel packed with Celite, and MTBE (3 x 50 mL) is used to wash the precipitate.'''

ORGSYN_V95P0142_B_PARA1_INFO = {
    'text': ORGSYN_V95P0142_B_PARA1_TEXT,
    'name': 'orgsyn_v95p0142_b_para1',
    'reagents': {
        '(S)-(-)-α,α-Diphenyl-2-pyrrolidinylmethanol': {
            'quantities': ['25.0 g', '98.8 mmol', '1.0 equiv'],
        },
        'THF': {
            'quantities': ['220 mL'],
        },
        'imidazole': {
            'quantities': ['20.0 g', '294 mmol', '3.0 equiv'],
        },
        'the imidazole': {
            'quantities': [],
        },
        'trimethylchlorosilane': {
            'quantities': ['31.3 mL', '247 mmol', '2.50 equiv'],
        },
        'the TMSCl': {
            'quantities': [],
        },
        'tetrahydrofuran': {
            'quantities': ['50 mL'],
        },
        'the side': {
            'quantities': [],
        },
        'methyl tert-butyl ether(MTBE)': {
            'quantities': ['150 mL'],
        },
        'the resultant': {
            'quantities': [],
        },
        'MTBE': {
            'quantities': ['3 x 50 mL'],
        },
    },
    'steps': [
        Add,
        Dissolve,
        Add,
        HeatChillToTemp,
        Add,
        Add,
        HeatChill,
        Add,
        Stir,
        Filter,
        WashSolid,
        Dry,
    ],
    'vessels': [
        # Add
        {
            'vessel': 'filter',
        },
        # Dissolve
        {
            'vessel': 'filter',
        },
        # Add
        {
            'vessel': 'filter',
        },
        # HeatChillToTemp
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
        # Add
        {
            'vessel': 'filter',
        },
        # Stir
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
            'reagent': '(S)-(-)-α,α-Diphenyl-2-pyrrolidinylmethanol',
            'mass': 25.0,
            'stir': False,
        },
        # Dissolve
        {
            'solvent': 'THF',
            'volume': 220.0,
        },
        # Add
        {
            'reagent': 'imidazole',
            'mass': 20.0,
            'stir': True,
        },
        # HeatChillToTemp
        {
            'temp': 4.0,
        },
        # Add
        {
            'reagent': 'trimethylchlorosilane',
            'volume': 31.3,
            'dispense_speed': DEFAULT_SLOW_ADDITION_DISPENSE_SPEED,
            'stir': True,
        },
        # Add
        {
            'reagent': 'tetrahydrofuran',
            'volume': 50.0,
            'stir': True,
        },
        # HeatChill
        {
            'temp': 23.0,
            'time': 54000.0,
        },
        # Add
        {
            'reagent': 'methyl tert-butyl ether(MTBE)',
            'volume': 150.0,
            'stir': True,
        },
        # Stir
        {
            'time': 900.0,
        },
        # Filter
        {
            'filter_vessel': 'filter',
        },
        # WashSolid
        {
            'solvent': 'MTBE',
            'volume': 50.0,
            'repeat': 3,
        },
        # Dry
        {},
    ],
}
