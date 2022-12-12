from chemputerxdl.steps import *
from xdl.steps import *
from synthreader.finishing.constants import DEFAULT_STIRRING_TIME

CSSP22_TEXT = '''This procedure is used for the chemoselective reduction of enones to produce allylic alcohols, in this case (and many others) with a good degree of stereospecificity. The enone and cerium trichloride are stirred in methanol at 0C and the sodium borohydride is added portionwise over about 15 minutes; some effervescence should be seen. Stirring is continued at this temperature until completion (TLC), usually about 1.5-2 hours, then quenched with ammonium chloride solution, extracted 4 times with ethyl acetate, washed with brine, dried over magnesium sulphate, filtered, concentrated and purified by column chromatography eluting with 20% EtOAc/PE'''


CSSP22_INFO = {
    'text': CSSP22_TEXT,
    'name': 'cssp22',
    'reagents': {
        'the enone': {
            'quantities': [],
        },
        'cerium trichloride': {
            'quantities': [],
        },
        'methanol': {
            'quantities': [],
        },
        'the sodium borohydride': {
            'quantities': [],
        },
        'ammonium chloride solution': {
            'quantities': [],
        },
        'ethyl acetate': {
            'quantities': [],
        },
        'brine': {
            'quantities': [],
        },
        'magnesium sulphate': {
            'quantities': [],
        },
        '20 % EtOAc/PE': {
            'quantities': [],
        },
    },
    'steps': [
        HeatChillToTemp,
        Add,
        Add,
        Add,
        Stir,
        Add,
        Stir,
        Add,
        Separate,
        Separate,
        Evaporate,
        RunColumn,
    ],
    'vessels': [
        # HeatChillToTemp
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
        # Stir
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
        # Add
        {
            'vessel': 'reactor',
        },
        # Separate
        {
            'from_vessel': 'reactor',
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
        # RunColumn
        {
            'from_vessel': 'rotavap',
            'to_vessel': 'reactor',
            'column': 'column',
        },
    ],
    'properties': [
        # HeatChillToTemp
        {
            'temp': 0.0,
        },
        # Add
        {
            'reagent': 'the enone',
            'stir': True,
        },
        # Add
        {
            'reagent': 'cerium trichloride',
            'stir': True,
        },
        # Add
        {
            'reagent': 'methanol',
            'stir': True,
        },
        # Stir
        {
            'time': DEFAULT_STIRRING_TIME,
        },
        # Add
        {
            'reagent': 'the sodium borohydride',
            'time': 900.0,
        },
        # Stir
        {
            'time': 1.75 * 60 * 60,
        },
        # Add
        {
            'reagent': 'ammonium chloride solution',
        },
        # Separate
        {
            'purpose': 'extract',
            'solvent': 'ethyl acetate',
            'n_separations': 4,
        },
        # Separate
        {
            'purpose': 'wash',
            'solvent': 'brine',
            'n_separations': 1,
            'through': 'magnesium sulphate',
        },
        # Evaporate
        {},
        # RunColumn
        {},
    ],
}
