from chemputerxdl.steps import *
from xdl.steps import *
from synthreader.finishing.constants import (
    DEFAULT_ALLOWED_TO_COOL_TIME, DEFAULT_AUTO_EVAPORATION_TIME_LIMIT)

THISOQ_4E_TEXT = '''Titanocene dichloride (1.0 g, 4.0 mmol) and phenol (0.75 g, 8.0 mmol, 2  eq) were  dissolved in benzene (40  mL). Sodium  hydride (290 mg, 12  mmol, 3 equiv), suspended in benzene (20 mL) was added and gas evolution was observed. The reaction mixture was heated to reflux for 3 hours, which resulted in a color change from red to orange. The mixture was allowed to cool to 23 ºC and filtered and the filter cake was rinsed with additional benzene (50  mL). The  combined organic mother liquors were concentrated and an orange solid (1.2 g) was received. The crude product was suspended in  n-hexane  (4  mL)  and  sonicated  for 1 min in an ultrasonic bath. The solution was decanted off and the suspension/sonication/decanting procedure was repeated.  The remaining solid was dried under high vacuum and the title compound was received in 69% yield (1.0 g) as a yellow solid. The nmr data matched the previously reported values (Figure S1).'''

THISOQ_4E_INFO = {
    'text': THISOQ_4E_TEXT,
    'name': 'thisoq_4e',
    'reagents': {
        'titanocene dichloride': {
            'quantities': ['1.0 g', '4.0 mmol'],
        },
        'phenol': {
            'quantities': ['0.75 g', '8.0 mmol', '2 eq'],
        },
        'benzene': {
            'quantities': ['40 mL', '20 mL', '50 mL'],
        },
        'sodium hydride': {
            'quantities': ['290 mg', '12 mmol', '3 equiv'],
        },
        'n-hexane': {
            'quantities': ['4 mL'],
        }
    },
    'steps': [
        Confirm,
        Confirm,
        Dissolve,
        Add,
        HeatChill,
        HeatChillToTemp,
        Filter,
        WashSolid,
        Dry,
        Evaporate,
        Add,
        Sonicate,
        Dry,
    ],
    'vessels': [
        # Confirm
        {},
        # Confirm
        {},
        # Dissolve
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
        # HeatChillToTemp
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
        # Transfer
        {
            'from_vessel': 'filter',
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
        # Add
        {
            'vessel': 'reactor',
        },
        # Sonicate
        {},
        # Dry
        {
            'vessel': 'reactor',
        },
    ],
    'properties': [
        # Confirm
        {
            'msg': 'Is Titanocene dichloride ( 1.0 g , 4.0 mmol ) in the correct vessel?',
        },
        # Confirm
        {
            'msg': 'Is phenol ( 0.75 g , 8.0 mmol , 2 eq ) in the correct vessel?',
        },
        # Dissolve
        {
            'solvent': 'benzene',
            'volume': 40.0,
        },
        # Add
        {
            'reagent': 'sodium hydride benzene solution',
            'volume': 20.0,
            'stir': True,
        },
        # HeatChill
        {
            'temp': 80.1,
            'time': 10800.0,
        },
        # HeatChillToTemp
        {
            'temp': 25,
            'active': False,
            'continue_heatchill': False,
        },
        # Filter
        {
            'filter_vessel': 'filter',
        },
        # WashSolid
        {
            'solvent': 'benzene',
            'volume': 50.0,
            'repeat': 1,
        },
        # Dry
        {},
        # Transfer
        {
            'volume': 'all',
        },
        # Evaporate
        {
            'time': DEFAULT_AUTO_EVAPORATION_TIME_LIMIT,
            'mode': 'auto',
        },
        # Transfer
        {},
        # Add
        {
            'reagent': 'n-hexane',
            'volume': 4.0,
            'stir': False,
        },
        # Sonicate
        {},
        # Dry
        {},
    ],
}
