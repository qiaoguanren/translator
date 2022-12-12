from chemputerxdl.steps import *
from xdl.steps import *
from synthreader.finishing.constants import DEFAULT_SLOW_ADDITION_DISPENSE_SPEED
from synthreader.constants import DEFAULT_BELOW_TEMP_REDUCTION

ORGSYN_CV1P0001_ACETAL_TEXT = '''
In a 1-gallon (4-l.) bottle are placed 1050 g. (1305 cc., 21.7 moles) of 95 per cent ethyl alcohol and 200 g. (1.8 moles) of granulated anhydrous calcium chloride (Note 1). The mixture is cooled to 8° or below by immersion in ice water, and 500 g. (620 cc., 11.4 moles) of freshly distilled acetaldehyde (b. p. 20–22°) is slowly added down the sides of the bottle so that it forms a layer on the alcoholic calcium chloride. The bottle is then tightly closed with a cork stopper and shaken vigorously for a few minutes (Note 2). It is then allowed to stand at room temperature with intermittent shaking for one to two days. The mixture divides into two layers after one to two hours; after the first twenty-four hours no appreciable change in volume of the two layers takes place.
The upper layer, which weighs 1280–1285 g., is separated and washed three times with 330 cc. portions of water. The weight has now fallen to 990–995 g. The oil is dried by standing over 25 g. of anhydrous potassium carbonate and is then fractionally distilled with the use of an efficient column at least 90 cm. long (Note 3), and the fraction which boils at 101–103.5° collected as pure acetal. In this way 700–720 g. can be obtained by one or two fractionations. The yield can be further increased by washing the low-boiling fractions and residue with small quantities of water, drying, and again fractionally distilling, so that a total of 790–815 g. is obtained (61–64 per cent of the theoretical amount). (Note 4)'''

ORGSYN_CV1P0001_ACETAL_INFO = {
    'text': ORGSYN_CV1P0001_ACETAL_TEXT,
    'name': 'orgsyn_cv1p0001_acetal',
    'reagents': {
        '95 % ethyl alcohol': {
            'quantities': ['1050 g', '1305 cc', '21.7 moles'],
        },
        'granulated anhydrous calcium chloride': {
            'quantities': ['200 g', '1.8 moles'],
        },
        'freshly distilled acetaldehyde': {
            'quantities': ['500 g', '620 cc', '11.4 moles'],
        },
        'the alcoholic calcium chloride': {
            'quantities': [],
        },
        'water': {
            'quantities': ['330 cc'],
        },
        'pure acetal': {
            'quantities': [],
        },
    },
    'steps': [
        Add,
        Add,
        HeatChillToTemp,
        Add,
        Stir,
        Separate,
        Separate,
        Distill,
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
        # HeatChillToTemp
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
            'to_vessel': 'reactor',
            'through': 'anhydrous potassium carbonate',
        },
        # Distill
        {},
    ],
    'properties': [
        # Add
        {
            'reagent': '95 % ethyl alcohol',
            'volume': 1305.0,
            'stir': False,
        },
        # Add
        {
            'reagent': 'granulated anhydrous calcium chloride',
            'mass': 200.0,
            'stir': True,
        },
        # HeatChillToTemp
        {
            'temp': 8 - DEFAULT_BELOW_TEMP_REDUCTION,
        },
        # Add
        {
            'reagent': 'freshly distilled acetaldehyde',
            'volume': 620.0,
            'dispense_speed': DEFAULT_SLOW_ADDITION_DISPENSE_SPEED,
            'stir': True,
        },
        # Stir
        {
            'time': 129600.0,
            'stir_speed': 600,
        },
        # Separate
        {
            'purpose': 'extract',
            'product_bottom': False,
            'solvent': '',
            'n_separations': 1,
        },
        # Separate
        {
            'purpose': 'wash',
            'product_bottom': False,
            'solvent': 'water',
            'solvent_volume': 330.0,
            'n_separations': 3,
        },
        # Distill
        {},
    ],
}
