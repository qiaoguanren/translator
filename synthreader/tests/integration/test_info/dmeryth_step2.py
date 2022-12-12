from chemputerxdl.steps import *
from xdl.steps import *
from synthreader.finishing.constants import (
    DEFAULT_AUTO_EVAPORATION_TIME_LIMIT,
    DEFAULT_SLOW_ADDITION_DISPENSE_SPEED,
)

# https://pubs.acs.org/doi/suppl/10.1021/acs.orglett.5b00987/suppl_file/ol5b00987_si_001.pdf

DMERYTH_STEP2_TEXT = '''N-(3,4-Dimethoxyphenethyl)pent-4-enamide  (23.730g,  90.0mmol)  was  dissolved  in  MeCN  (550mL).  POCl3(63.5mL, 666.7mmol, 7.4equiv) was added at room temperature (23°C) and the resulting mixture was heated to 95°C for 4h. After cooling down to room temperature the solvent was removed in vacuum. The residue was added carefully to an ice-cold aqueous saturated K2CO3 solution (500mL) and the aqueous solution  was  extracted  with CH2Cl2(5×200mL). The  combined  organic  layers  were  dried  over K2CO3 and concentrated to give the crude 1-(But-3-en-1-yl)-6,7-dimethoxy-3,4-dihydroisoquinoline. The pure title compound was received after extraction as a brown oil (19.451g, 79.3mmol)in 88% yield. The Dihydroisoquinoline 7was directly  employed  in  the  titanium-catalysis  without  purification.'''

DMERYTH_STEP2_INFO = {
    'text': DMERYTH_STEP2_TEXT,
    'name': 'dmeryth_step2',
    'reagents': {
        'N-(3,4-Dimethoxyphenethyl)pent-4-enamide': {
            'quantities': ['23.730 g', '90.0 mmol'],
        },
        'MeCN': {
            'quantities': ['550 mL'],
        },
        'POCl3': {
            'quantities': ['63.5 mL', '666.7 mmol', '7.4 equiv'],
        },
        'aqueous saturated K2CO3 solution': {
            'quantities': ['500 mL'],
        },
        'CH2Cl2': {
            'quantities': ['5 x 200 mL'],
        },
        'K2CO3': {
            'quantities': [],
        },
        'the crude 1-(But-3-en-1-yl)-6,7-dimethoxy-3,4-dihydroisoquinoline': {
            'quantities': [],
        },
    },
    'steps': [
        Confirm,
        Dissolve,
        HeatChillToTemp,
        Add,
        HeatChill,
        HeatChillToTemp,
        Evaporate,
        HeatChillToTemp,
        Add,
        StopHeatChill,
        Separate,
        Evaporate,
    ],
    'vessels': [
        # Confirm
        {},
        # Dissolve
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
        # HeatChillToTemp
        {
            'vessel': 'reactor',
        },
        # Transfer
        {
            'from_vessel': 'reactor',
            'to_vessel': 'rotavap',
        },
        # Evaporate
        {
            'rotavap_name': 'rotavap',
        },
        # Transfer
        {
            'from_vessel': 'rotavap',
            'to_vessel': 'reactor',
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
        # Separate
        {
            'from_vessel': 'reactor',
            'separation_vessel': 'separator',
            'to_vessel': 'rotavap',
        },
        # Evaporate
        {
            'rotavap_name': 'rotavap',
        },
    ],
    'properties': [
        # Confirm
        {
            'msg': 'Is N- ( 3,4-Dimethoxyphenethyl ) pent-4-enamide ( 23.730 g , 90.0 mmol ) in the correct vessel?',
        },
        # Dissolve
        {
            'solvent': 'MeCN',
            'volume': 550.0,
        },
        # HeatChillToTemp
        {
            'temp': 23.0,
        },
        # Add
        {
            'reagent': 'POCl3',
            'volume': 63.5,
            'stir': True,
        },
        # HeatChill
        {
            'temp': 95.0,
            'time': 14400.0,
        },
        # HeatChillToTemp
        {
            'temp': 25.0,
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Evaporate
        {
            'temp': 50,
            'pressure': 153.0,
            'time': DEFAULT_AUTO_EVAPORATION_TIME_LIMIT,
            'mode': 'auto',
        },
        # Transfer
        {
            'volume': 'all',
        },
        # HeatChillToTemp
        {
            'temp': 2,
        },
        # Add
        {
            'reagent': 'aqueous saturated K2CO3 solution',
            'volume': 500.0,
            'stir': True,
        },
        # StopHeatChill
        {},
        # Separate
        {
            'purpose': 'extract',
            'solvent': 'CH2Cl2',
            'product_bottom': True,
            'solvent_volume': 200.0,
            'n_separations': 5,
            'through': 'K2CO3',
        },
        # Evaporate
        {

        },
    ],
}
