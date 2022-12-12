from chemputerxdl.steps import *
from xdl.steps import *
from synthreader.finishing.constants import DEFAULT_AUTO_EVAPORATION_TIME_LIMIT

ORGSYN_V83P0193_TEXT = '''A nitrogen- purged, 300-mL, three-necked, round-bottomed flask is equipped with a magnetic stirring bar, a rubber septum, a glass stopper, a temperature probe, and a nitrogen inlet adapter. The flask is charged with 2-methylcyclohexanone (10.0 mL, 82.6 mmol) (Note 1), triethylamine (13.9 mL, 100 mmol) (Note 2), and t-butyldimethylsilyl chloride (TBDMSCl) (15.1 g, 100 mmol) (Note 1). To the flask is added a solution of sodium iodide (15.0 g, 100 mmol) (Note 1) in acetonitrile (100 mL) (Note 3) via syringe over 30 min at ambient temperature. The reaction solution is stirred at ambient temperature for 18 h. The resulting mixture is quenched by addition of saturated sodium bicarbonate solution (100 mL). The mixture is extracted with hexane twice (2 × 200 mL). The combined organic phases are washed with brine (40 mL) and dried over MgSO4, filtered and concentrated at reduced pressure (15–25 mmHg, 25–35 °C) to afford crude product 1 (20.2 g) as a pale yellow oil. This crude product is purified by filtration through a silica gel pad (200 g of silica in a 10-cm diameter fritted glass funnel, height of silica was 20 cm), rinsing with 1 L of hexanes (Note 4) to provide 17.75–17.80 g (95%) of 1 as a colorless oil (Notes 5, 6).'''

ORGSYN_V83P0193_INFO = {
    'text': ORGSYN_V83P0193_TEXT,
    'name': 'orgsyn_v83p0193',
    'reagents': {
        '2 methylcyclohexanone': {
            'quantities': ['10.0 mL', '82.6 mmol'],
        },
        'triethylamine': {
            'quantities': ['13.9 mL', '100 mmol'],
        },
        't-butyldimethylsilyl chloride(TBDMSCl)': {
            'quantities': ['15.1 g', '100 mmol'],
        },
        'sodium iodide': {
            'quantities': ['15.0 g', '100 mmol'],
        },
        'acetonitrile': {
            'quantities': ['100 mL'],
        },
        'saturated sodium bicarbonate solution': {
            'quantities': ['100 mL'],
        },
        'hexane': {
            'quantities': [],
        },
        'brine': {
            'quantities': ['40 mL'],
        },
        'MgSO4': {
            'quantities': [],
        },
        'hexanes': {
            'quantities': ['1 L'],
        },
    },
    'steps': [
        Evacuate,
        Add,
        Add,
        Add,
        HeatChillToTemp,
        Add,
        Stir,
        Add,
        Separate,
        Separate,
        Evaporate,
        FilterThrough,
    ],
    'vessels': [
        # Evacuate
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
        # Add
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
            'through': 'MgSO4',
        },
        # Evaporate
        {
            'rotavap_name': 'rotavap',
        },
        # FilterThrough
        {
            'from_vessel': 'rotavap',
            'to_vessel': 'reactor',
            'through': 'silica-gel',
        },
    ],
    'properties': [
        # Evacuate
        {
            'vessel': 'reactor',
        },
        # Add
        {
            'reagent': '2 methylcyclohexanone',
            'volume': 10.0,
            'stir': False,
        },
        # Add
        {
            'reagent': 'triethylamine',
            'volume': 13.9,
            'stir': True,
        },
        # Add
        {
            'reagent': 't-butyldimethylsilyl chloride(TBDMSCl)',
            'mass': 15.1,
            'stir': True,
        },
        # HeatChillToTemp
        {
            'temp': 25.0,
        },
        # Add
        {
            'reagent': 'sodium iodide acetonitrile solution',
            'volume': 100.0,
            'time': 1800.0,
            'stir': True,
        },
        # Stir
        {
            'time': 64800.0,
        },
        # Add
        {
            'reagent': 'saturated sodium bicarbonate solution',
            'volume': 100.0,
            'stir': True,
        },
        # Separate
        {
            'purpose': 'extract',
            'product_bottom': False,
            'solvent': 'hexane',
            'solvent_volume': 200.0,
            'n_separations': 2,
        },
        # Separate
        {
            'purpose': 'wash',
            'product_bottom': False,
            'solvent': 'brine',
            'solvent_volume': 40.0,
            'n_separations': 1,
        },
        # Evaporate
        {
            'time': DEFAULT_AUTO_EVAPORATION_TIME_LIMIT,
            'mode': 'auto',
        },
        # FilterThrough
        {
            'through': 'silica-gel',
            'eluting_solvent': 'hexanes',
            'eluting_volume': 1000,
        },
    ],
}
