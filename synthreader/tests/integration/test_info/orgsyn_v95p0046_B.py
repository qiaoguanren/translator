from chemputerxdl.steps import *
from xdl.steps import *

ORGSYN_V95P0046_B_TEXT = '''An oven-dried 500 mL single-necked, round-bottomed flask equipped with an egg-shaped, Teflon-coated magnetic stir bar (3 cm x 1.5 cm) is capped with a rubber septum. While cooling to ambient temperature under an atmosphere of nitrogen, an oil bath is preheated to 80 °C. Once the flask is cooled, furan-2-yl(phenyl)methanol (1) (3.95 g, 22.7 mmol, 1.1 equiv) (Note 9) and acetonitrile (200 mL) (MeCN) (Notes 10 and 11) are added along with 2,4,6-trimethylaniline (2.78 g, 20.5 mmol, 1.0 equiv) (Note 12), resulting in a pale brown homogeneous mixture (Figure 1).

Dysprosium(III) trifluoromethanesulfonate (Dy(OTf)3, 0.628 g, 1.03 mmol, 0.05 equiv) is added (Notes 13 and 14). Immediately following addition, the flask is fitted with a water reflux condenser, placed under an atmosphere of nitrogen, and submerged in the oil bath that is preheated to 80 °C and stirred for 4 h (Note 15).

The reaction mixture becomes dark brown in color upon heating (Figure 2). The reaction is followed by TLC analysis on silica gel with 85% hexanes in ethyl acetate as eluent and visualized with under 254 nm UV light and stained with p-anisaldehyde (Note 16). Upon confirmation that no 1,3,5-trimethylaniline remains, the stirring is stopped and the reaction mixture is allowed to cool to ambient temperature under an atmosphere of nitrogen. The cooled reaction mixture is quenched with saturated aqueous sodium bicarbonate (1 x 150 mL) and transferred to a 1 L separatory funnel and extracted with ethyl acetate (3 x 150 mL) (Figure 3).

The combined organic layers are dried over MgSO4, filtered and concentrated (25 °C, 10 mmHg) to produce a dark brown oil. The product of the crude reaction mixture is purified via column chromatography (Note 17) to afford the cyclopentenone product (2) as a brown oil (4.97 g, 83%) (Notes 18, 19, 20, 21, and 22) (Figure 4).'''

ORGSYN_V95P0046_B_INFO = {
    'text': ORGSYN_V95P0046_B_TEXT,
    'name': 'orgsyn_v95p0046_b',
    'reagents': {
        'furan-2-yl(phenyl)methanol': {
            'quantities': ['3.95 g', '22.7 mmol', '1.1 equiv'],
        },
        'acetonitrile': {
            'quantities': ['200 mL'],
        },
        '2,4,6-trimethylaniline': {
            'quantities': ['2.78 g', '20.5 mmol', '1.0 equiv'],
        },
        'dysprosium': {
            'quantities': ['0.628 g', '1.03 mmol', '0.05 equiv'],
        },
        'silica gel': {
            'quantities': [],
        },
        '85 % hexanes': {
            'quantities': [],
        },
        'ethyl acetate': {
            'quantities': ['3 x 150 mL'],
        },
        'UV': {
            'quantities': [],
        },
        'p-anisaldehyde': {
            'quantities': [],
        },
        'no 1,3,5-trimethylaniline': {
            'quantities': [],
        },
        'saturated aqueous sodium bicarbonate': {
            'quantities': ['1 x 150 mL'],
        },
        'MgSO4': {
            'quantities': [],
        },
        'the cyclopentenone product': {
            'quantities': [],
        },
    },
    'steps': [
        Add,
        Add,
        Add,
        Add,
        HeatChillToTemp,
        Stir,
        StopStir,
        HeatChillToTemp,
        Add,
        Separate,
        Evaporate,
        RunColumn,
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
        # Add
        {
            'vessel': 'reactor',
        },
        # Add
        {
            'vessel': 'reactor',
        },
        # HeatChillToTemp
        {
            'vessel': 'reactor',
        },
        # Stir
        {
            'vessel': 'reactor',
        },
        # StopStir
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
        # Transfer
        {
            'from_vessel': 'reactor',
            'to_vessel': 'separator',
        },
        # Separate
        {
            'from_vessel': 'separator',
            'separation_vessel': 'separator',
            'to_vessel': 'rotavap',
            'through': 'MgSO4',
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
        # Add
        {
            'reagent': 'furan-2-yl(phenyl)methanol',
            'mass': 3.95,
            'stir': False,
        },
        # Add
        {
            'reagent': 'acetonitrile',
            'volume': 200.0,
            'stir': False,
        },
        # Add
        {
            'reagent': '2,4,6-trimethylaniline',
            'mass': 2.78,
            'stir': True,
        },
        # Add
        {
            'reagent': 'dysprosium',
            'mass': 0.628,
            'stir': True,
        },
        # HeatChillToTemp
        {
            'temp': 80.0,
        },
        # Stir
        {
            'time': 14400.0,
        },
        # StopStir
        {},
        # HeatChillToTemp
        {
            'temp': 25,
            'active': False,
            'continue_heatchill': False,
        },
        # Add
        {
            'reagent': 'saturated aqueous sodium bicarbonate',
            'volume': 150.0,
            'stir': True,
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Separate
        {
            'purpose': 'extract',
            'product_bottom': True,
            'solvent': 'ethyl acetate',
            'solvent_volume': 150.0,
            'n_separations': 3,
        },
        # Evaporate
        {
            'temp': 25.0,
            'pressure': 13.3322,
            'time': 1800,
            'mode': 'auto',
        },
        # RunColumn
        {},
    ],
}
