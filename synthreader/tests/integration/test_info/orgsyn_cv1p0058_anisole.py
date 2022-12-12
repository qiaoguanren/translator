from chemputerxdl.steps import *
from xdl.steps import *
from synthreader.finishing.constants import DEFAULT_SEPARATION_VOLUME

ORGSYN_CV1P0058_ANISOLE_TEXT = '''In a 5-l., three-necked, round-bottomed flask fitted with an efficient stirrer, separatory funnel, and reflux condenser is placed a mixture of 235 g. (2.5 moles) of phenol and 100 g. (2.5 moles) of sodium hydroxide (Note 1) in 1 l. of water. The mixture is cooled, with stirring, in an ice-salt bath to below 10°. There is then added through the separatory funnel, with stirring, 315 g. (235 cc., 2.5 moles) of dimethyl sulfate (Note 2). This addition requires about one hour, and the cooling bath is not removed until the addition is complete. The mixture is then heated on a water bath for one-half hour. At the end of this time there is added through the separatory funnel a mixture of 235 g. (2.5 moles) of phenol and 100 g. (2.5 moles) of sodium hydroxide in 1 l. of water. This addition requires about fifteen minutes. The mixture is then refluxed vigorously over a free flame for fifteen hours (Note 3).
The mixture is cooled and the anisole layer is separated. The aqueous portion is extracted with about 200 cc. of benzene (Note 4). The combined anisole-benzene portion is washed once with water, dried over calcium chloride and distilled from a modified Claisen flask (p. 130). The portion boiling at 100–153° is refractionated. The main fraction distils at 153–154°/748 mm. The yield is 388–405 g. (72–75 per cent of the theoretical amount) (Note 5) and (Note 6).'''

ORGSYN_CV1P0058_ANISOLE_INFO = {
    'text': ORGSYN_CV1P0058_ANISOLE_TEXT,
    'name': 'orgsyn_cv1p0058_anisole',
    'reagents': {
        'dimethyl sulfate': {
            'quantities': ['315 g', '235 cc', '2.5 moles'],
        },
        'the anisole': {
            'quantities': [],
        },
        'benzene': {
            'quantities': ['200 cc'],
        },
        'water': {
            'quantities': [],
        },
        'calcium chloride': {
            'quantities': [],
        },
    },
    'steps': [
        Add,
        HeatChillToTemp,
        Add,
        HeatChill,
        Add,
        HeatChill,
        HeatChillToTemp,
        Separate,
        Separate,
        Separate,
        Distill,
    ],
    'vessels': [
        # Add
        {
            'vessel': 'reactor',
        },
        # HeatChillToTemp
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
        # HeatChill
        {
            'vessel': 'reactor',
        },
        # HeatChillToTemp
        {
            'vessel': 'reactor',
        },
        # Separate
        {
            'from_vessel': 'reactor',
            'separation_vessel': 'separator',
            'to_vessel': 'buffer_flask1',
            'waste_phase_to_vessel': 'separator',
        },
        # Separate
        {
            'from_vessel': 'separator',
            'separation_vessel': 'separator',
            'to_vessel': 'separator',
        },
        # Transfer
        {
            'from_vessel': 'buffer_flask1',
            'to_vessel': 'separator',
        },
        # Separate
        {
            'from_vessel': 'separator',
            'separation_vessel': 'separator',
            'to_vessel': 'reactor',
            'through': 'calcium chloride',
        },
        # Distill
        {},
    ],
    'properties': [
        # Add
        {
            'reagent': 'a mixture of 235 g ( 2.5 moles ) of phenol and 100 g ( 2.5 moles ) of sodium hydroxide in 1 l of water',
            'volume': 1000.0,
            'stir': False,
        },
        # HeatChillToTemp
        {
            'temp': 7.0,
        },
        # Add
        {
            'reagent': 'dimethyl sulfate',
            'volume': 235.0,
            'time': 3600.0,
            'stir': True,
        },
        # HeatChill
        {
            'temp': 100.0,
            'time': 1800.0,
        },
        # Add
        {
            'reagent': 'a mixture of 235 g ( 2.5 moles ) of phenol and 100 g ( 2.5 moles ) of sodium hydroxide in 1 l of water',
            'volume': 1000.0,
            'time': 900.0,
            'stir': True,
        },
        # HeatChill
        {
            'temp': 150.0,
            'time': 54000.0,
        },
        # HeatChillToTemp
        {
            'temp': 25.0,
        },
        # Separate
        {
            'purpose': 'extract',
            'solvent': '',
            'product_bottom': False,
            'n_separations': 1,
        },
        # Separate
        {
            'purpose': 'extract',
            'product_bottom': False,
            'solvent': 'benzene',
            'solvent_volume': 200.0,
            'n_separations': 1,
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Separate
        {
            'purpose': 'wash',
            'product_bottom': False,
            'solvent': 'water',
            'solvent_volume': DEFAULT_SEPARATION_VOLUME,
            'n_separations': 1,
        },
        # Distill
        {},
    ],
}
