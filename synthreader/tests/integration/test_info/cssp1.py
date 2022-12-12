from chemputerxdl.steps import *
from xdl.steps import *

CSSP1_TEXT = '''Using Schlenk techniques, C6H5CH2MgCl (100 ml, 1M in diethyl ether, 4 equiv.) was added to ZrCl4 (6.0 g, 0.025 mol) in a diethyl ether (50 ml) slurry over 1 hr at -78°C, ensuring that the suspension was cool before addition of the Grignard reagent. Once the addition was complete, the mixture was allowed to warm slowly with stirring and any gas expansion was vented at the Schlenk line bubbler. The solution was stirred overnight at ambient temperature (in the absence of light) and the bright orange solution was then cooled to 0°C and filtered to remove MgCl2 [this residue should be "destroyed" by cautious hydrolysis before disposal]. The diethyl ether was removed in vacuo and the orange product was redissolved in toluene (30 ml) and filtered. Cooling to -30°C afforded orange crystals which were washed with cold toluene (2 x 10 ml). Yield variable, but about 70%.'''

CSSP1_INFO = {
    'text': CSSP1_TEXT,
    'name': 'cssp1',
    'reagents': {
        'C6H5CH2MgCl (1M in diethyl ether)': {
            'quantities': ['100 ml', '1M in diethyl ether', '4 equiv'],
        },
        'ZrCl4': {
            'quantities': ['6.0 g', '0.025 mol'],
        },
        'diethyl ether': {
            'quantities': ['50 ml'],
        },
        'MgCl2': {
            'quantities': [],
        },
        'toluene': {
            'quantities': ['30 ml', '2 x 10 ml'],
        },
    },
    'steps': [
        HeatChillToTemp,
        Add,
        Add,
        HeatChillToTemp,
        HeatChill,
        HeatChillToTemp,
        Filter,
        Evaporate,
        Dissolve,
        Filter,
        WashSolid,
        Dry,
    ],
    'vessels': [
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
        # HeatChillToTemp
        {
            'vessel': 'filter',
        },
        # Stir
        {
            'vessel': 'filter',
        },
        # HeatChillToTemp
        {
            'vessel': 'filter',
        },
        # Filter
        {},
        # Transfer
        {
            'from_vessel': 'filter',
            'to_vessel': 'rotavap',
        },
        # Evaporate
        {
            'rotavap_name': 'rotavap',
        },
        # Dissolve
        {
            'vessel': 'rotavap',
        },
        # Transfer
        {
            'from_vessel': 'rotavap',
            'to_vessel': 'filter',
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
        # HeatChillToTemp
        {
            'temp': -78.0,
        },
        # Add
        {
            'reagent': 'ZrCl4 diethyl ether solution',
            'volume': 50,
            'stir': False,
        },
        # Add
        {
            'reagent': 'C6H5CH2MgCl (1M in diethyl ether)',
            'volume': 100,
            'time': 3600,
            'stir': True,
        },
        # HeatChillToTemp
        {
            'temp': 18,
            'active': False,
            'continue_heatchill': False,
        },
        # Stir
        {
            'time': 57600,
        },
        # HeatChillToTemp
        {
            'temp': 0,
        },
        # Filter
        {
            'filter_vessel': 'filter',
            'filter_top_volume': 0,
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Evaporate
        {
            'time': 1800,
            'mode': 'auto',
        },
        # Dissolve
        {
            'solvent': 'toluene',
            'volume': 30,
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Filter
        {
            'filter_vessel': 'filter',
            'filter_top_volume': 0,
        },
        # WashSolid
        {
            'solvent': 'toluene',
            'volume': 10,
            'temp': 10,
            'repeat': 2,
        },
        # Dry
        {},
    ],
}
