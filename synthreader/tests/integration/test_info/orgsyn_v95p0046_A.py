from chemputerxdl.steps import *
from xdl.steps import *

ORGSYN_V95P0046_A_TEXT = '''An oven-dried 500 mL three-necked, round-bottomed flask equipped with an egg-shaped, Teflon-coated magnetic stir bar (3 cm x 1.5 cm) is capped on all necks with rubber septa. Phenylmagnesium bromide (57.4 mL, 57.4 mmol, 1.0 equiv, 1M in THF) (Note 2) is charged into this flask under an atmosphere of nitrogen at 5 °C (ice-water bath). Furfural (4.76 mL, 57.4 mmol, 1.0 equiv) (Note 3) is added over the course of 30 min via syringe into the cooled reaction through a side neck while maintaining internal temperature below 25 °C. Once all furfural is added the reaction stirs for 4 h. The reaction is monitored by thin-layer chromatography (TLC) analysis on silica gel with 70% hexanes in ethyl acetate as eluent and visualized under 254 nm UV light and stained with p-anisaldehyde (Note 4). Upon confirmation of product formation the reaction is quenched with saturated aqueous ammonium chloride (1 x 100 mL) and transferred to a 1 L separatory funnel and extracted with ethyl acetate (3 x 100 mL). The combined organic layers are dried over MgSO4, filtered and concentrated to produce a yellow-orange oil. The product of the crude reaction mixture is purified via column chromatography (Note 5) to afford furan-2-yl(phenyl)methanol (1) as a yellow oil (9.71 g, 94%) (Notes 6, 7, and 8).'''

ORGSYN_V95P0046_A_INFO = {
    'text': ORGSYN_V95P0046_A_TEXT,
    'name': 'orgsyn_v95p0046_a',
    'reagents': {
        'phenylmagnesium bromide (1M in THF)': {
            'quantities': ['57.4 mL', '57.4 mmol', '1.0 equiv', '1M in THF'],
        },
        'furfural': {
            'quantities': ['4.76 mL', '57.4 mmol', '1.0 equiv'],
        },
        'all furfural': {
            'quantities': [],
        },
        'silica gel': {
            'quantities': [],
        },
        '70 % hexanes': {
            'quantities': [],
        },
        'ethyl acetate': {
            'quantities': ['3 x 100 mL'],
        },
        'p-anisaldehyde': {
            'quantities': [],
        },
        'saturated aqueous ammonium chloride': {
            'quantities': ['1 x 100 mL'],
        },
        'MgSO4': {
            'quantities': [],
        },
        'furan-2-yl(phenyl)methanol': {
            'quantities': [],
        },
    },
    'steps': [
        HeatChillToTemp,
        Add,
        HeatChillToTemp,
        Add,
        StopHeatChill,
        Stir,
        Add,
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
        # HeatChillToTemp
        {
            'vessel': 'reactor',
        },
        # Add
        {
            'vessel': 'reactor',
        },
        # StopHeatChill
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
        # HeatChillToTemp
        {
            'temp': 5.0,
        },
        # Add
        {
            'reagent': 'phenylmagnesium bromide (1M in THF)',
            'volume': 57.4,
            'stir': False,
        },
        # HeatChillToTemp
        {
            'temp': 22.0,
        },
        # Add
        {
            'reagent': 'furfural',
            'volume': 4.76,
            'time': 1800.0,
            'stir': True,
        },
        # StopHeatChill
        {},
        # Stir
        {
            'time': 14400.0,
        },
        # Add
        {
            'reagent': 'saturated aqueous ammonium chloride',
            'volume': 100.0,
            'stir': True,
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Separate
        {
            'purpose': 'extract',
            'product_bottom': False,
            'solvent': 'ethyl acetate',
            'solvent_volume': 100.0,
            'n_separations': 3,
        },
        # Evaporate
        {
            'time': 1800,
            'mode': 'auto',
        },
        # RunColumn
        {},
    ],
}
