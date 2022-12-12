from chemputerxdl.steps import *
from xdl.steps import *
from synthreader.finishing.constants import (
    DEFAULT_ALLOWED_TO_COOL_TIME,
)

CSSP23_TEXT = '''Palladium chloride is placed in a 3 necked round bottomed flask which is fitted with a thermometer and a reactor stick attached to a second inverted 3 necked round bottomed flask. DMSO is added, followed by triphenylphosphine. The mixture is heated to 140°C using an oil bath with stirring in order to dissolve all the solid (a small amount of solid does not seem to dissolve). The oil bath is then removed and the mixture stirred for a further 15 minutes. Hydrazine hydrate is rapidly added causing evolution of nitrogen. The resulting dark solution is immediately cooled with a water bath until crystallisation begins to occur (~125°C) at which point it is allowed to cool without external cooling. Once the mixture has reached room temperature, the apparatus is inverted in order to reactor and the solid is washed successively with absolute ethanol (2 x 10 mL) and dry ether (2 x 10 mL) (this is achieved by adding the solvent from a syringe through a side arm). The resulting yellow solid is then dried under vacuum for 3-4 hours.
'''

CSSP23_INFO = {
    'text': CSSP23_TEXT,
    'name': 'cssp23',
    'reagents': {
        'palladium chloride': {
            'quantities': [],
        },
        'DMSO': {
            'quantities': [],
        },
        'triphenylphosphine': {
            'quantities': [],
        },
        'hydrazine hydrate': {
            'quantities': [],
        },
        'absolute ethanol': {
            'quantities': ['2 x 10 mL'],
        },
        'dry ether': {
            'quantities': ['2 x 10 mL'],
        },
    },
    'steps': [
        Add,
        Add,
        Add,
        HeatChillToTemp,
        StopHeatChill,
        Stir,
        Add,
        HeatChillToTemp,
        HeatChillToTemp,
        WashSolid,
        WashSolid,
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
        # HeatChillToTemp
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
        # HeatChillToTemp
        {
            'vessel': 'reactor',
        },
        # HeatChillToTemp
        {
            'vessel': 'reactor',
        },
        # WashSolid
        {
            'vessel': 'reactor',
        },
        # WashSolid
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
            'reagent': 'palladium chloride',
        },
        # Add
        {
            'reagent': 'DMSO',
        },
        # Add
        {
            'reagent': 'triphenylphosphine',
        },
        # HeatChillToTemp
        {
            'temp': 140.0,
        },
        # StopHeatChill
        {},
        # Stir
        {
            'time': 900.0,
        },
        # Add
        {
            'reagent': 'hydrazine hydrate',
        },
        # HeatChillToTemp
        {
            'temp': 125.0,
        },
        # HeatChillToTemp
        {
            'temp': 25.0,
            'active': False,
            'continue_heatchill': False,
        },
        # WashSolid
        {
            'solvent': 'absolute ethanol',
            'volume': 10.0,
            'repeat': 2,
        },
        # WashSolid
        {
            'solvent': 'dry ether',
            'volume': 10.0,
            'repeat': 2,
        },
        # Dry
        {
            'time': 12600.0,
        },
    ],
}
