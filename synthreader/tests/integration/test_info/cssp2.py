from chemputerxdl.steps import *
from xdl.steps import *
from synthreader.finishing.constants import DEFAULT_DROPWISE_DISPENSE_SPEED

CSSP2_TEXT = '''Lithium butyl (98.5 cm3, 2.50 M in hexanes, 3 equivalents) was added dropwise at -50°C to a solution of distilled tris(2-aminoethyl)amine (TREN) (12 g, 0.082 mol) in dry tetrahydrofuran (200 cm3). The mixture was stirred for 30 min. during which time it was allowed to warm to 0°C. The solution was then cooled to -50°C and a solution of sublimed tert-butylchlorodimethylsilane (37.1 g, 0.246 mol, 3 equivalents) in tetrahydrofuran (40 cm3) was added over a period of 5 min. The mixture was stirred for 30 min. with slow warming to 0°C. After evaporation of volatiles under reduced pressure at ambient temperature, a liquid nitrogen cooled probe was inserted into the flask in order to facilitate removal of the last traces of solvent in vacuo. The oily residue was extracted into pentane (3 x 50 cm3) and filtered. If required, this solution may be evaporated to give virtually pure H3(NN'3). Lithium butyl (98 cm3, 2.50 M in hexanes) was added dropwise to the combined extracts at -80°C. The mixture was allowed to warm slowly to -30°C and was stirred for a further 15 minutes. The solution was then cooled to -50°C and tetrahydrofuran (18 cm3, 3 equivalents) was added. The white microcrystalline solid which precipitated was isolated by cannula filtration and dried in vacuo (46 g, 78%).'''

CSSP2_INFO = {
    'text': CSSP2_TEXT,
    'name': 'cssp2',
    'reagents': {
        'lithium butyl (2.50 M in hexanes)': {
            'quantities': ['98.5 cm3', '2.50 M in hexanes', '3 equivalents'],
        },
        'distilled tris(2-aminoethyl)amine(TREN)': {
            'quantities': ['12 g', '0.082 mol'],
        },
        'dry tetrahydrofuran': {
            'quantities': ['200 cm3'],
        },
        'sublimed tert-butylchlorodimethylsilane': {
            'quantities': ['37.1 g', '0.246 mol', '3 equivalents'],
        },
        'tetrahydrofuran': {
            'quantities': ['40 cm3', '18 cm3', '3 equivalents'],
        },
        'pentane': {
            'quantities': ['3 x 50 cm3'],
        },
    },
    'steps': [
        HeatChillToTemp,
        Add,
        Add,
        StopHeatChill,
        Stir,
        HeatChillToTemp,
        HeatChillToTemp,
        Add,
        StartHeatChill,
        Stir,
        Evaporate,
        Separate,
        HeatChillToTemp,
        Add,
        HeatChillToTemp,
        Stir,
        HeatChillToTemp,
        Add,
        Filter,
        Dry,
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
        # HeatChillToTemp
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
        # StartHeatChill
        {
            'vessel': 'reactor',
        },
        # Stir
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
        # Separate
        {
            'from_vessel': 'rotavap',
            'separation_vessel': 'separator',
            'to_vessel': 'filter',
        },
        # HeatChillToTemp
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
        # Add
        {
            'vessel': 'filter',
        },
        # Filter
        {},
        # Dry
        {
            'vessel': 'filter',
        },
    ],
    'properties': [
        # HeatChillToTemp
        {
            'temp': -50.0,
        },
        # Add
        {
            'reagent': 'distilled tris(2-aminoethyl)amine(TREN) dry tetrahydrofuran solution',
            'volume': 200.0,
            'stir': False,
        },
        # Add
        {
            'reagent': 'lithium butyl (2.50 M in hexanes)',
            'volume': 98.5,
            'dispense_speed': DEFAULT_DROPWISE_DISPENSE_SPEED,
            'stir': True,
        },
        # StopHeatChill
        {},
        # Stir
        {
            'time': 1800.0,
        },
        # HeatChillToTemp
        {
            'active': False,
            'temp': 0,
            'continue_heatchill': True,
        },
        # HeatChillToTemp
        {
            'temp': -50.0,
        },
        # Add
        {
            'reagent': 'sublimed tert-butylchlorodimethylsilane tetrahydrofuran solution',
            'volume': 40.0,
            'time': 300.0,
            'stir': True,
        },
        # StartHeatChill
        {
            'temp': 0.0,
        },
        # Stir
        {
            'time': 1800.0,
            'stir_speed': 50,
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Evaporate
        {
            'temp': 50,
            'pressure': 249.0,
            'time': 1800,
            'mode': 'auto',
        },
        # Separate
        {
            'purpose': 'extract',
            'solvent': 'pentane',
            'product_bottom': False,
            'solvent_volume': 50.0,
            'n_separations': 3,
        },
        # HeatChillToTemp
        {
            'temp': -80.0,
        },
        # Add
        {
            'reagent': 'lithium butyl (2.50 M in hexanes)',
            'volume': 98.0,
            'dispense_speed': DEFAULT_DROPWISE_DISPENSE_SPEED,
            'stir': True,
        },
        # HeatChillToTemp
        {
            'temp': -30,
            'active': False,
            'continue_heatchill': True,
        },
        # Stir
        {
            'time': 15 * 60,
        },
        # HeatChillToTemp
        {
            'temp': -50.0,
        },
        # Add
        {
            'reagent': 'tetrahydrofuran',
            'volume': 18.0,
            'stir': True,
        },
        # Filter
        {
            'filter_vessel': 'filter',
        },
        # Dry
        {},
    ],
}
