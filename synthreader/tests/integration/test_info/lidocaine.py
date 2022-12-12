from chemputerxdl.steps import *
from xdl.steps import *

LIDOCAINE_TEXT = '''2,6-Dimethylaniline (3.0 mL, 2.9 g, 24.4 mmol) is added to 15 mL of glacial acetic acid in a 125-mL Erlenmeyer flask followed by chloroacetyl chloride (2.0 mL, 2.85 g, 25.1mmol) and 25 mL of half-saturated aqueous sodium acetate. Precipitation of the amide is virtually instantaneous. The product is stirred thoroughly with 60 mL of cold water and isolated by vacuum filtration. It should be pressed as dry as possible in the Buchner funnel and used immediately in the next step.

The amide is placed in a 50-mL round-bottom flask containing diethylamine (7.5 mL, 5.29 g, 72.5 mmol) and 25 mL of toluene and refluxed for one hour. The reaction mixture is cooled to room temperature and transferred to a separatory funnel, where it is washed 4× with 50-mL portions of water to remove diethylamine hydrochloride and excess diethylamine. The organic layer is extracted with one 20-mL portion of 3 M hydrochloric acid and extracted once with 20mL of water. The combined aqueous extracts are placed in a 125-mL Erlenmeyer flask, cooled to 10 °C in an ice bath, and neutralized by addition of 3 M sodium hydroxide in portions with stirring while maintaining the temperature below 20 °C. The product separates as a granular white solid and is isolated by vacuum filtration. It is washed with cold water, pressed dry, and air-dried as long as possible.'''

LIDOCAINE_INFO = {
    'name': 'lidocaine',
    'text': LIDOCAINE_TEXT,
    'reagents': {
        '2,6-Dimethylaniline': {
            'quantities': ['3.0 mL', '2.9 g', '24.4 mmol'],
        },
        'glacial acetic acid': {
            'quantities': ['15 mL'],
        },
        'chloroacetyl chloride': {
            'quantities': ['2.0 mL', '2.85 g', '25.1 mmol'],
        },
        'half-saturated aqueous sodium acetate': {
            'quantities': ['25 mL'],
        },
        'diethylamine': {
            'quantities': ['7.5 mL', '5.29 g', '72.5 mmol'],
        },
        'toluene': {
            'quantities': ['25 mL'],
        },
        'water': {
            'quantities': ['20 mL'],
        },
        'diethylamine hydrochloride': {
            'quantities': [],
        },
        '3 M hydrochloric acid': {
            'quantities': ['20 mL'],
        },
        '3 M sodium hydroxide': {
            'quantities': [],
        },
    },
    'steps': [
        Add,
        Add,
        Add,
        Add,
        HeatChillToTemp,
        Add,
        Stir,
        StopHeatChill,
        Filter,
        Dry,
        Add,
        Add,
        HeatChill,
        HeatChillToTemp,
        Separate,
        Separate,
        Separate,
        HeatChillToTemp,
        Add,
        Filter,
        WashSolid,
        Dry,
        Dry,
    ],
    'vessels': [
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'filter_vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},

        # Transfer
        {
            'from_vessel': 'filter',
            'to_vessel': 'separator',
        },
        {'from_vessel': 'separator',
        'to_vessel': 'separator',
        'separation_vessel': 'separator'},

        {'from_vessel': 'separator',
        'to_vessel': 'filter',
        'separation_vessel': 'separator',
        'waste_phase_to_vessel': 'separator'},

        {'from_vessel': 'separator',
        'to_vessel': 'filter',
        'separation_vessel': 'separator'},

        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'filter_vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
    ],
    'properties': [
        # Add
        {
            'volume': 15,
            'stir': False,
            'reagent': 'glacial acetic acid',
        },
        # Add
        {
            'volume': 3,
            'stir': True,
            'reagent': '2,6-Dimethylaniline',
        },
        # Add
        {
            'volume': 2,
            'stir': True,
            'reagent': 'chloroacetyl chloride',
        },
        # Add
        {
            'volume': 25,
            'stir': True,
            'reagent': 'half-saturated aqueous sodium acetate',
        },
        # HeatChillToTemp
        {
            'temp': 10,
        },
        # Add
        {
            'reagent': 'water',
            'volume': 60,
            'stir': True,
        },
        # Stir
        {
            'time': 60 * 60,
        },
        # StopHeatChill
        {},
        # Filter
        {},
        # Dry
        {},
        # Add
        {
            'reagent': 'diethylamine',
            'volume': 7.5,
            'stir': False,
        },
        # Add
        {
            'reagent': 'toluene',
            'volume': 25,
            'stir': True,
        },
        # HeatChill
        {
            'temp': 110.6,
            'time': 60 * 60,
        },
        # HeatChillToTemp
        {
            'temp': 25,
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Separate
        {
            'purpose': 'wash',
            'solvent': 'water',
            'product_bottom': False,
            'solvent_volume': 50,
            'n_separations': 4,
        },
        # Separate
        {
            'purpose': 'extract',
            'solvent': '3 M hydrochloric acid',
            'product_bottom': True,
            'solvent_volume': 20,
            'n_separations': 1,
        },
        # Separate
        {
            'purpose': 'extract',
            'solvent': 'water',
            'product_bottom': True,
            'solvent_volume': 20,
            'n_separations': 1,
        },
        # HeatChillToTemp
        {
            'temp': 10,
        },
        # Add
        {
            'reagent': '3 M sodium hydroxide',
            'volume': 20,
            'stir': True,
            'dispense_speed': 10,
        },
        # Filter
        {},
        # WashSolid
        {
            'solvent': 'water',
            'temp': 10
        },
        # Dry
        {},
        # Dry
        {
            'time': 3*60*60
        }
    ],
}
