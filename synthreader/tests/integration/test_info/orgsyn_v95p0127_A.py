from chemputerxdl.steps import *
from xdl.steps import *

ORGSYN_V95P0127_A_TEXT = '''A dry, tared, 500 mL round-bottomed flask equipped with a 5x2-cm Teflon-coated magnetic stirring bar and a septum is charged with toluene (250 mL, 0.2 M) (Note 2). Pivalic acid (12.5 mL, 11.3 g, 110 mmol, 2.2 equiv) (Note 3) is added to form a colorless solution. Zinc oxide (4.07 g, 50 mmol, 1 equiv) is added in 1 g portions at 25 ºC over 15 min to form a colorless suspension (Note 4). The flask is equipped with a Dean-Stark trap (10 mL) wrapped in aluminum foil and topped with a reflux condenser (20 cm) and the suspension is stirred under nitrogen at reflux in an oil bath for 16 h (Figure 1) (Note 5).

A viscous colorless suspension is formed overnight. After cooling to 25 ºC, the mixture is concentrated by rotary evaporation (50 °C/50 mmHg). The remaining pivalic acid and water are removed in vacuo from the reaction mixture using a vacuum line (0.1 mmHg) and a liquid nitrogen cold trap (1000 mL) (see Figure 1). The white solid is warmed to 100 °C in an oil bath and dried for at least 6 h (Note 6). Zinc pivalate (13.1-13.2 g, 48.9-49.7 mmol, 98-99%), is obtained as a puffy amorphous white solid (Note 7).'''

ORGSYN_V95P0127_A_INFO = {
    'text': ORGSYN_V95P0127_A_TEXT,
    'name': 'orgsyn_v95p0127_a',
    'reagents': {
        'toluene': {
            'quantities': ['250 mL', '0.2 M'],
        },
        'pivalic acid': {
            'quantities': ['12.5 mL', '11.3 g', '110 mmol', '2.2 equiv'],
        },
        'zinc oxide': {
            'quantities': ['4.07 g', '50 mmol', '1 equiv'],
        },
        'water': {
            'quantities': [],
        },
        'zinc pivalate (98.5  %)': {
            'quantities': ['13.149999999999999  g', '49.3  mmol', '98.5  %'],
        },
        'amorphous': {
            'quantities': [],
        },
    },
    'steps': [
        Add,
        Add,
        Add,
        HeatChill,
        HeatChillToTemp,
        Evaporate,
        Evaporate,
        HeatChillToTemp,
        Dry,
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
        # Dry
        {
            'vessel': 'reactor',
        },
    ],
    'properties': [
        # Add
        {
            'reagent': 'toluene',
            'volume': 250.0,
            'stir': False,
        },
        # Add
        {
            'reagent': 'pivalic acid',
            'volume': 12.5,
            'stir': True,
        },
        # Add
        {
            'reagent': 'zinc oxide',
            'mass': 4.07,
            'stir': True,
        },
        # HeatChill
        {
            'temp': 110.6,
            'time': 57600.0,
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
            'pressure': 48.0,
            'time': 1800,
            'mode': 'auto',
        },
        # Evaporate
        {
            'pressure': 0.13332200000000002,
            'time': 1800,
            'mode': 'auto',
        },
        # Transfer
        {
            'volume': 'all',
        },
        # HeatChillToTemp
        {
            'temp': 100.0,
        },
        # Dry
        {
            'time': 21600.0,
        },
    ],
}
