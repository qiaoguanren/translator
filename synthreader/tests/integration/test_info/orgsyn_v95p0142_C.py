from chemputerxdl.steps import *
from xdl.steps import *

ORGSYN_V95P0142_C_TEXT = '''A solution of (S)-(-)-α,α-diphenyl-2-pyrrolidinemethanol trimethylsilyl ether 2 (19.0 g, 58.6 mmol, 0.50 equiv) in chloroform (120 mL) is transferred to a 1-L, three-necked, round-bottomed flask equipped with a 4-cm Teflon-coated magnetic stir-bar, a 250-mL addition funnel, a thermometer fitted with a glass adaptor, and a rubber septum through which nitrogen atmosphere is ensured (Figure 2). The flask is cooled to 4 ºC using an ice-water bath. Using a 20 mL syringe, ethyl (2E)-4-oxo-2-butenoate (14.1 mL, 117 mmol, 1.0 equiv) (Note 10) is added to the addition funnel.

The enoate is then added to the flask dropwise via the addition funnel over 15 min, maintaining the internal temperature at 4 ºC. Chloroform (10 mL) is used to rinse the additional funnel. tert-Butyl (tert-butyldimethylsilyl)oxycarbamate 1 (34.8 g, 141 mmol, 1.20 equiv) is dissolved in chloroform (60 mL), placed in the addition funnel, and added dropwise over 1 h. The internal temperature is maintained at 4 ºC throughout the course of the addition. Chloroform (10 mL) is used to wash both the flask that contained the tert-butyl (tert-butyldimethylsilyl)oxycarbamate and the addition funnel. The final concentration of the substrate is 0.6 M. The reaction is stirred for 12 h under nitrogen at 23 °C, and the reaction is monitored by TLC (Note 11). The reaction mixture is transferred to a 1-L round-bottomed flask and concentrated by rotary evaporation (40 °C bath, 325-30 mmHg). The residue is dried on the vacuum pump (0.5 mmHg) for 5 h, after which the crude compound is purified by column chromatography (Note 12). The desired fractions are collected and concentrated by rotary evaporation (40 °C bath, 325-30 mmHg) to provide 13.3 g (30.1%) of the desired product. Impure fractions from the initial column are combined and further purified by column chromatography (Note 13). The desired fractions are collected and concentrated by rotary evaporation (40 °C bath, 325-30 mmHg) to provide 3.4 g (7.7%) of the product. The residual oils are further dried for 5 h under vacuum pump (0.5 mmHg) to afford the desired compound as a pale yellow oil (combined yield of 16.7 g, 37.8%, >98.5% purity, 94% ee) (Notes 14, 15, 16, and 17).'''

ORGSYN_V95P0142_C_INFO = {
    'text': ORGSYN_V95P0142_C_TEXT,
    'name': 'orgsyn_v95p0142_c',
    'reagents': {
        '(S)-(-)-α,α-diphenyl-2-pyrrolidinemethanol trimethylsilyl ether 2': {
            'quantities': ['19.0 g', '58.6 mmol', '0.50 equiv'],
        },
        'chloroform': {
            'quantities': ['120 mL', '10 mL', '60 mL', '10 mL'],
        },
        'ethyl(2E)-4-oxo-2-butenoate': {
            'quantities': ['14.1 mL', '117 mmol', '1.0 equiv'],
        },
        'the enoate': {
            'quantities': [],
        },
        'tert-Butyl(tert-butyldimethylsilyl)oxycarbamate 1': {
            'quantities': ['34.8 g', '141 mmol', '1.20 equiv'],
        },
        'the tert-butyl(tert-butyldimethylsilyl)oxycarbamate': {
            'quantities': [],
        },
    },
    'steps': [
        Add,
        HeatChillToTemp,
        Add,
        Add,
        Confirm,
        Dissolve,
        Add,
        HeatChill,
        Evaporate,
        Dry,
        RunColumn,
        Evaporate,
        RunColumn,
        Evaporate,
        Dry,
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
        # Add
        {
            'vessel': 'reactor',
        },
        # Confirm
        {},
        # Dissolve
        {
            'vessel': 'filter',
        },
        # Transfer
        {
            'from_vessel': 'filter',
            'to_vessel': 'reactor',
        },
        # Add
        {
            'vessel': 'filter',
        },
        # Transfer
        {
            'from_vessel': 'filter',
            'to_vessel': 'reactor',
        },
        # HeatChill
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
        # Dry
        {
            'vessel': 'rotavap',
        },
        # RunColumn
        {
            'from_vessel': 'rotavap',
            'to_vessel': 'rotavap',
            'column': 'column',
        },
        # Evaporate
        {
            'rotavap_name': 'rotavap',
        },
        # RunColumn
        {
            'from_vessel': 'rotavap',
            'to_vessel': 'rotavap',
            'column': 'column',
        },
        # Evaporate
        {
            'rotavap_name': 'rotavap',
        },
        # Dry
        {
            'vessel': 'rotavap',
        },
    ],
    'properties': [
        # Add
        {
            'reagent': '(S)-(-)-α,α-diphenyl-2-pyrrolidinemethanol trimethylsilyl ether 2 chloroform solution',
            'volume': 120.0,
            'stir': False,
        },
        # HeatChillToTemp
        {
            'temp': 4.0,
        },
        # Add
        {
            'reagent': 'ethyl(2E)-4-oxo-2-butenoate',
            'volume': 14.1,
            'time': 900.0,
            'stir': True,
        },
        # Add
        {
            'reagent': 'chloroform',
            'volume': 10.0,
            'stir': True,
        },
        # Confirm
        {
            'msg': 'Is tert-Butyl ( tert-butyldimethylsilyl ) oxycarbamate 1 ( 34.8 g , 141 mmol , 1.20 equiv ) in the correct vessel?',
        },
        # Dissolve
        {
            'solvent': 'chloroform',
            'volume': 60.0,
        },
        # Transfer
        {
            'volume': 'all',
            'time': 3600.0,
        },
        # Add
        {
            'reagent': 'chloroform',
            'volume': 10.0,
            'stir': True,
        },
        # Transfer
        {
            'volume': 'all',
        },
        # HeatChill
        {
            'temp': 23.0,
            'time': 43200.0,
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Evaporate
        {
            'temp': 40.0,
            'pressure': 236.64655000000002,
            'time': 1800,
            'mode': 'auto',
        },
        # Dry
        {
            'time': 18000.0,
            'vacuum_pressure': 0.66661,
        },
        # RunColumn
        {},
        # Evaporate
        {
            'temp': 40.0,
            'pressure': 236.64655000000002,
            'time': 1800,
            'mode': 'auto',
        },
        # RunColumn
        {},
        # Evaporate
        {
            'temp': 40.0,
            'pressure': 236.64655000000002,
            'time': 1800,
            'mode': 'auto',
        },
        # Dry
        {
            'time': 18000.0,
        },
    ],
}
