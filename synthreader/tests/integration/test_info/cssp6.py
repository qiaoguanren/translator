from chemputerxdl.steps import *
from xdl.steps import *

# Text has been modified as some parts of it were either grammatically wrong or
# considered too hard to translate at this stage.

CSSP6_TEXT = '''The phenol is added to a hot solution of ninhydrin in acetic acid and the mixture heated at reflux for 2h. After cooling to room temperature the resulting precipitate was isolated by vacuum filtration, washed with ice-cold acetic acid and dried in vacuo, 2nd crop can be collected.

4-methylaniline is added to a solution of NaOH in acetic acid and stirred under reflux for 12h. The mixture is allowed to cool to room temperature before the resulting precipitate was isolated by vacuum filtration, washed with ice-cold acetic acid and dried in vacuo, 2nd crop can be collected. NaCl is added to aqueous 2M NaOH and refluxed for 15 min, and the resulting white precipitate was isolated by filtration and washed with water. The yellow filtrate was then cooled and acidified with 6M HCl. The resulting white precipitate is isolated by vacuum filtration, washed with cold water and recrystallized from ethanol/water to give a white solid.
'''

CSSP6_INFO = {
    'text': CSSP6_TEXT,
    'name': 'cssp6',
    'reagents': {
        'the phenol': {
            'quantities': [],
        },
        'ninhydrin': {
            'quantities': [],
        },
        'acetic acid': {
            'quantities': [],
        },
        'acetic acid': {
            'quantities': [],
        },
        '4 methylaniline': {
            'quantities': [],
        },
        'NaOH': {
            'quantities': [],
        },
        'NaCl': {
            'quantities': [],
        },
        'aqueous 2M NaOH': {
            'quantities': [],
        },
        'water': {
            'quantities': [],
        },
        '6M HCl': {
            'quantities': [],
        },
    },
    'steps': [
        Add,
        Add,
        HeatChill,
        HeatChillToTemp,
        Filter,
        WashSolid,
        Dry,
        Add,
        Add,
        HeatChill,
        HeatChillToTemp,
        Filter,
        WashSolid,
        Dry,
        Add,
        Add,
        HeatChill,
        Filter,
        WashSolid,
        Dry,
        HeatChillToTemp,
        Add,
        Filter,
        WashSolid,
        Dry,
        Recrystallize,
    ],
    'vessels': [
        # Add
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
        # Add
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
        # Add
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
        # HeatChillToTemp
        {
            'vessel': 'filter',
        },
        # Add
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
    ],
    'properties': [
        # Add
        {
            'reagent': 'ninhydrin acetic acid solution',
        },
        # Add
        {
            'reagent': 'the phenol',
        },
        # HeatChill
        {
            'temp': 100,
            'time': 7200.0,
        },
        # HeatChillToTemp
        {
            'temp': 25.0,
        },
        # Filter
        {
            'filter_vessel': 'filter',
        },
        # WashSolid
        {
            'solvent': 'acetic acid',
            'temp': 2,
            'repeat': 1,
        },
        # Dry
        {},
        # Add
        {
            'reagent': 'NaOH acetic acid solution',
            'stir': False,
        },
        # Add
        {
            'reagent': '4 methylaniline',
            'stir': False,
        },
        # HeatChill
        {
            'temp': 100,
            'time': 43200.0,
        },
        # HeatChillToTemp
        {
            'active': False,
            'temp': 25,
            'continue_heatchill': False,
        },
        # Filter
        {
            'filter_vessel': 'filter',
        },
        # WashSolid
        {
            'solvent': 'acetic acid',
            'temp': 2,
            'repeat': 1,
        },
        # Dry
        {},
        # Add
        {
            'reagent': 'aqueous 2M NaOH',
        },
        # Add
        {
            'reagent': 'NaCl',
        },
        # HeatChill
        {
            'temp': 100,
            'time': 900.0,
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
        {},
        # HeatChillToTemp
        {
            'temp': 25.0,
        },
        # Add
        {
            'reagent': '6M HCl',
        },
        # Filter
        {
            'filter_vessel': 'filter',
        },
        # WashSolid
        {
            'solvent': 'water',
            'temp': 10,
            'repeat': 1,
        },
        # Dry
        {},
        # Recrystallize
        {},
    ],
}
