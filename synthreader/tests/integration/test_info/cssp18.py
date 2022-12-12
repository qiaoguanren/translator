from chemputerxdl.steps import *
from xdl.steps import *
from synthreader.finishing.constants import (
    DEFAULT_HOT_REAGENT_TEMP,
    DEFAULT_MINIMUM_VOLUME,
    DEFAULT_ALLOWED_TO_COOL_TIME,
)
from synthreader.constants import (
    DEFAULT_FAST_STIR_SPEED,
    DEFAULT_OVERNIGHT_TIME
)

CSSP18_TEXT = '''TsNa is dissolved in water and filtered to obtain a clear solution. Bromine is added dropwise over about 30min with rapid stirring and venting to allow for build-up of bromine gas. A yellow precipitate of crude TsBr is observed. The mixture is stirred for a further 30min following complete addition of the bromine. The crude TsBr was filtered off and washed well with water. It was then dried thoroughly in vacuo overnight. Typical crude yield of dry powdery solid, 63-69%. The product was recrystallised from carbon tetrachloride. It was first dissolved in minimum hot CCl4 and then filtered to remove any insoluble oily solid. The product was allowed to cool and crystals of TsBr were filtered off. The crystals were washed with very cold CCl4 (-20°C) Do not air dry for more than a few seconds or crystals will go off. Final overall yield approx 50%'''

CSSP18_INFO = {
    'text': CSSP18_TEXT,
    'name': 'cssp18',
    'reagents': {
        'TsNa': {
            'quantities': [],
        },
        'water': {
            'quantities': [],
        },
        'bromine': {
            'quantities': [],
        },
        'bromine gas': {
            'quantities': [],
        },
        'TsBr': {
            'quantities': [],
        },
        'the bromine': {
            'quantities': [],
        },
        'carbon tetrachloride': {
            'quantities': [],
        },
        'CCl4': {
            'quantities': ['-20 °C'],
        },
    },
    'steps': [
        Confirm,
        Dissolve,
        Filter,
        Add,
        Stir,
        Filter,
        WashSolid,
        Dry,
        Recrystallize,
        Dissolve,
        Filter,
        HeatChillToTemp,
        Filter,
        WashSolid,
        Dry,
    ],
    'vessels': [
        # Confirm
        {},
        # Dissolve
        {
            'vessel': 'filter',
        },
        # Filter
        {},
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
        # Recrystallize
        {},
        # Dissolve
        {
            'vessel': 'filter',
        },
        # Filter
        {},
        # HeatChillToTemp
        {
            'temp': 25,
            'active':  False,
            'continue_heatchill': False,
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
        # Confirm
        {
            'msg': 'Is TsNa in the correct vessel?',
        },
        # Dissolve
        {
            'solvent': 'water',
            'volume': 0,
        },
        # Filter
        {
            'filter_vessel': 'filter',
        },
        # Add
        {
            'reagent': 'bromine',
            'time': 1800.0,
            'stir': True,
            'stir_speed': DEFAULT_FAST_STIR_SPEED,
        },
        # Stir
        {
            'time': 1800.0,
        },
        # Filter
        {
            'filter_vessel': 'filter',
        },
        # WashSolid
        {
            'solvent': 'water',
            'repeat': 1,
        },
        # Dry
        {
            'time': DEFAULT_OVERNIGHT_TIME,
        },
        # Recrystallize
        {},
        # Dissolve
        {
            'solvent': 'CCl4',
            'volume': DEFAULT_MINIMUM_VOLUME,
            'temp': DEFAULT_HOT_REAGENT_TEMP,
        },
        # Filter
        {
            'filter_vessel': 'filter',
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
            'solvent': 'CCl4',
            'temp': -20.0,
            'repeat': 1,
        },
        # Dry
        {},
    ],
}
