from chemputerxdl.steps import *
from xdl.steps import *
from synthreader.finishing.constants import DEFAULT_AUTO_EVAPORATION_TIME_LIMIT

ORGSYN_CV9P0001_TEXT = '''An oven-dried, 2-L, three-necked, round-bottomed flask, equipped with a nitrogen inlet, magnetic stirring bar, thermometer, and reflux condenser, under an inert nitrogen atmosphere (Note 1), is charged with 1.22 g (10 mmol) of 4-dimethylaminopyridine (Note 2), 500 mL of tetrahydrofuran (Note 3), 11.0 mL (95.7 mmol) of 1-hexyne (Note 4), 13.2 mL (140 mmol) of acetic anhydride (Note 5), 9.8 mL (70 mmol) of triethylamine (Note 2), 20.0 g (64.0 mmol) of pentacarbonyl[phenyl(methoxy)chromium]carbene (Note 1) and (Note 6), and a final 100-mL rinse of tetrahydrofuran. The solution is heated to reflux with an oil bath and heating is maintained until TLC indicates that the chromium complex is totally consumed (about 45–60 min, (Note 7)). The solution is then cooled to ambient temperature, 30 g of silica gel is added (Note 8), and volatile organic material is removed under reduced pressure (rotary evaporator). The green solids are transferred to a filter funnel and washed with hexane until TLC indicates that all products have been removed (5 × 100 mL) (Note 9). The hexane filtrate is then concentrated under reduced pressure to give crude product contaminated with chromium hexacarbonyl. To the mixture is added 20 mL of isopropyl alcohol and the insoluble chromium hexacarbonyl is removed by filtration (Note 9). The filtrate is concentrated under reduced pressure to give 14.0 g of crude product which is purified by silica gel chromatography (Note 10). Appropriate fractions are combined and the solvent is removed under reduced pressure to give 1-acetoxy-2-butyl-4-methoxynaphthalene (11.8 g, >95% pure based on HPLC, 68% yield based on the carbene complex, (Note 6) and (Note 11)) as a light yellow oil which crystallizes on standing (Note 12). If desired, the product can be crystallized from isopropyl alcohol (2.5 mL/g) to give white crystals, mp 49–50°C (>99% pure based on HPLC).'''

ORGSYN_CV9P0001_INFO = {
    'text': ORGSYN_CV9P0001_TEXT,
    'name': 'orgsyn_cv9p0001',
    'reagents': {
        '4-dimethylaminopyridine': {
            'quantities': ['1.22 g', '10 mmol'],
        },
        'tetrahydrofuran': {
            'quantities': ['500 mL', '100 mL'],
        },
        '1 hexyne': {
            'quantities': ['11.0 mL', '95.7 mmol'],
        },
        'acetic anhydride': {
            'quantities': ['13.2 mL', '140 mmol'],
        },
        'triethylamine': {
            'quantities': ['9.8 mL', '70 mmol'],
        },
        'pentacarbonyl [ phenyl(methoxy)chromium ] carbene': {
            'quantities': ['20.0 g', '64.0 mmol'],
        },
        'the chromium complex': {
            'quantities': [],
        },
        'silica gel': {
            'quantities': ['30 g'],
        },
        'hexane': {
            'quantities': [],
        },
        'the hexane': {
            'quantities': [],
        },
        'chromium hexacarbonyl': {
            'quantities': [],
        },
        'isopropyl alcohol': {
            'quantities': ['20 mL'],
        },
        'the insoluble chromium hexacarbonyl': {
            'quantities': [],
        },
        '1-acetoxy-2-butyl-4 methoxynaphthalene': {
            'quantities': [],
        },
    },
    'steps': [
        Add,
        Add,
        Add,
        Add,
        Add,
        Add,
        Add,
        HeatChillToTemp,
        Wait,
        HeatChillToTemp,
        Add,
        Evaporate,
        WashSolid,
        Evaporate,
        Add,
        Filter,
        Evaporate,
        RunColumn,
        Evaporate,
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
        # Add
        {
            'vessel': 'reactor',
        },
        # HeatChillToTemp
        {
            'vessel': 'reactor',
        },
        # Wait
        {},
        # HeatChillToTemp
        {
            'vessel': 'reactor',
        },
        # Transfer
        {
            'from_vessel': 'reactor',
            'to_vessel': 'rotavap',
        },
        # Add
        {
            'vessel': 'rotavap',
        },
        # Evaporate
        {
            'rotavap_name': 'rotavap',
        },
        # WashSolid
        {
            'vessel': 'rotavap',
        },
        # Evaporate
        {
            'rotavap_name': 'rotavap',
        },
        # Transfer
        {
            'from_vessel': 'rotavap',
            'to_vessel': 'filter',
        },
        # Add
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
    ],
    'properties': [
        # Add
        {
            'reagent': '4-dimethylaminopyridine',
            'mass': 1.22,
            'stir': False,
        },
        # Add
        {
            'reagent': 'tetrahydrofuran',
            'volume': 500.0,
            'stir': False,
        },
        # Add
        {
            'reagent': '1 hexyne',
            'volume': 11.0,
            'stir': True,
        },
        # Add
        {
            'reagent': 'acetic anhydride',
            'volume': 13.2,
            'stir': True,
        },
        # Add
        {
            'reagent': 'triethylamine',
            'volume': 9.8,
            'stir': True,
        },
        # Add
        {
            'reagent': 'pentacarbonyl [ phenyl(methoxy)chromium ] carbene',
            'mass': 20.0,
            'stir': True,
        },
        # Add
        {
            'reagent': 'tetrahydrofuran',
            'volume': 100.0,
            'stir': True,
        },
        # HeatChillToTemp
        {
            'temp': 65,
        },
        # Wait
        {
            'time': 3150.0,
        },
        # HeatChillToTemp
        {
            'temp': 25.0,
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Add
        {
            'reagent': 'silica gel',
            'mass': 30.0,
            'stir': True,
        },
        # Evaporate
        {
            'temp': 50,
            'pressure': 249.0,
            'time': 1800,
            'mode': 'auto',
        },
        # WashSolid
        {
            'solvent': 'hexane',
            'volume': 100.0,
            'repeat': 5,
        },
        # Evaporate
        {
            'time': DEFAULT_AUTO_EVAPORATION_TIME_LIMIT,
            'mode': 'auto',
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Add
        {
            'reagent': 'isopropyl alcohol',
            'volume': 20.0,
            'stir': False,
        },
        # Filter
        {
            'filter_vessel': 'filter',
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Evaporate
        {
            'time': DEFAULT_AUTO_EVAPORATION_TIME_LIMIT,
            'mode': 'auto',
        },
        # RunColumn
        {},
        # Evaporate
        {
            'time': DEFAULT_AUTO_EVAPORATION_TIME_LIMIT,
            'mode': 'auto',
        },
    ],
}
