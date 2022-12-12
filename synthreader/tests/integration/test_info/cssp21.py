from chemputerxdl.steps import *
from xdl.steps import *

CSSP21_TEXT = '''The palladium tetrakis(triphenylphosphine), diethylamine (100 mL) and vinyl halide are stirred together at room temperature for 15 minutes. The copper iodide is then added, followed by the alkyne. The solution is heated for 3-5 hours at reflux, during which time it will usually go brown. The reaction is quenched with ammonium chloride, extracted with ether, washed with brine, dried over magnesium sulphate, filtered, concentrated and purified by column chromatography.'''

CSSP21_INFO = {
    'text': CSSP21_TEXT,
    'name': 'cssp21',
    'reagents': {
        'the palladium tetrakis(triphenylphosphine)': {
            'quantities': [],
        },
        'diethylamine': {
            'quantities': ['100 mL'],
        },
        'vinyl halide': {
            'quantities': [],
        },
        'the copper iodide': {
            'quantities': [],
        },
        'the alkyne': {
            'quantities': [],
        },
        'ammonium chloride': {
            'quantities': [],
        },
        'ether': {
            'quantities': [],
        },
        'brine': {
            'quantities': [],
        },
        'magnesium sulphate': {
            'quantities': [],
        },
    },
    'steps': [
        HeatChillToTemp,
        Add,
        Add,
        Add,
        Stir,
        StopHeatChill,
        Add,
        Add,
        HeatChill,
        Add,
        Separate,
        Separate,
        Evaporate,
        RunColumn,
    ],
    'vessels': [
        # HeatChillToTemp
        {},
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
        # Stir
        {
            'vessel': 'reactor',
        },
        # StopHeatChill
        {},
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
        # Add
        {
            'vessel': 'reactor',
        },
        # Separate
        {
            'from_vessel': 'reactor',
            'separation_vessel': 'separator',
            'to_vessel': 'separator',
        },
        # Separate
        {
            'from_vessel': 'separator',
            'separation_vessel': 'separator',
            'to_vessel': 'rotavap',
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
            'temp': 25.0,
        },
        # Add
        {
            'reagent': 'the palladium tetrakis(triphenylphosphine)',
            'stir': True,
        },
        # Add
        {
            'reagent': 'diethylamine',
            'volume': 100.0,
            'stir': True,
        },
        # Add
        {
            'reagent': 'vinyl halide',
            'stir': True,
        },
        # Stir
        {
            'time': 900.0,
        },
        # StopHeatChill
        {},
        # Add
        {
            'reagent': 'the copper iodide',
            'stir': True,
        },
        # Add
        {
            'reagent': 'the alkyne',
            'stir': True,
        },
        # HeatChill
        {
            'temp': 55.5,
            'time': 4 * 60 * 60,
        },
        # Add
        {
            'reagent': 'ammonium chloride',
            'stir': True,
        },
        # Separate
        {
            'purpose': 'extract',
            'solvent': 'ether',
            'n_separations': 1,
        },
        # Separate
        {
            'purpose': 'wash',
            'solvent': 'brine',
            'n_separations': 1,
            'through': 'magnesium sulphate',
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
