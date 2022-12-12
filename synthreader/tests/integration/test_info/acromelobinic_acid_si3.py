from chemputerxdl.steps import *
from xdl.steps import *
from synthreader.finishing.constants import DEFAULT_AUTO_EVAPORATION_TIME_LIMIT

# DOI: 10.1055/s-0032-1317668
# SI Section 3
# https://www.thieme-connect.de/media/synlett/201220/supmat/sup_st-2012-w0785-l_10-1055_s-0032-1317668.pdf

ACROMELOBINIC_ACID_SI3_TEXT = '''An oven-dried vial was charged with LiCl (0.53 g, 12.5 mmol) and MeONa (0.41 g, 7.5 mmol) in anhydrous THF (15  mL). The mixture  was stirred at reflux for 3 h and then cooled to 0 °C, to which were added  alkylphenones 1 (5.0  mmol) and diethyl oxalate (0.95g, 6.5  mmol). The  resulting mixture was allowed to stir at room temperature for 3 h and then concentrated to remove THF giving a residual. Anhydrous EtOH (15  mL),  trifluoroacetic acid (1.14 g, 10.0 mmol) and arylhydrazine hydrochlorides 3 (5.0 mmol) was in turn added to the residual at room temperature, followed  by  reflux  for 12 h. Then, a solution of NaOH (0.8 g, 20.0 mmol) in H2O (2  mL) was added  to the reaction solution, and stirred at reflux for another 4 h. Next, the  solution was concentrated in vacuo to remove EtOH affording a new residual, to which were added water (15 mL), methylene dichloride (15 mL) and 10% hydrochloric acid (ca. 10 mL) until pH 3–4 to make the  solution  partitioned  into  organic  and aqueous layers. The aqueous layer was extracted with methylene dichloride  (10 mL × 2). Finally, the combined organic phase was washed with water (20 mL × 2), dried over anhydrous sodium sulfate, and concentrated to give a crude product. The crude product was purified by recrystallization from a petroleum ether/ethyl acetate mixture (6 mL, 5/1, v/v) to give the corresponding 4.'''

ACROMELOBINIC_ACID_SI3_INFO = {
    'text': ACROMELOBINIC_ACID_SI3_TEXT,
    'name': 'acromelobinic_acid_si3',
    'reagents': {
        'LiCl': {
            'quantities': ['0.53 g', '12.5 mmol'],
        },
        'MeONa': {
            'quantities': ['0.41 g', '7.5 mmol'],
        },
        'anhydrous THF': {
            'quantities': ['15 mL'],
        },
        'alkylphenones 1': {
            'quantities': ['5.0 mmol'],
        },
        'diethyl oxalate': {
            'quantities': ['0.95 g', '6.5 mmol'],
        },
        'THF': {
            'quantities': [],
        },
        'anhydrous EtOH': {
            'quantities': ['15 mL'],
        },
        'trifluoroacetic acid': {
            'quantities': ['1.14 g', '10.0 mmol'],
        },
        'arylhydrazine hydrochlorides 3': {
            'quantities': ['5.0 mmol'],
        },
        'NaOH': {
            'quantities': ['0.8 g', '20.0 mmol'],
        },
        'H2O': {
            'quantities': ['2 mL'],
        },
        'EtOH': {
            'quantities': [],
        },
        'water': {
            'quantities': ['15 mL', '20 mL × 2'],
        },
        'methylene dichloride': {
            'quantities': ['15 mL', '10 mL × 2'],
        },
        '10 % hydrochloric acid': {
            'quantities': ['10 mL'],
        },
        'anhydrous sodium sulfate': {
            'quantities': [],
        },
    },
    'steps': [
        Add,
        HeatChill,
        HeatChillToTemp,
        Add,
        Add,
        HeatChill,
        Evaporate,
        HeatChillToTemp,
        Add,
        Add,
        Add,
        HeatChill,
        Add,
        HeatChill,
        Evaporate,
        Add,
        Add,
        Add,
        Separate,
        Separate,
        Evaporate,
        Recrystallize,
    ],
    'vessels': [
        # Add
        {
            'vessel': 'reactor',
        },
        # HeatChill
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
        # Add
        {
            'vessel': 'reactor',
        },
        # HeatChill
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
        # Transfer
        {
            'from_vessel': 'rotavap',
            'to_vessel': 'reactor',
        },
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
        # HeatChill
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
        # Add
        {
            'vessel': 'rotavap',
        },
        # Add
        {
            'vessel': 'rotavap',
        },
        # Add
        {
            'vessel': 'rotavap',
        },
        # Separate
        {
            'from_vessel': 'rotavap',
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
        # Transfer
        {
            'from_vessel': 'rotavap',
            'to_vessel': 'filter',
        },
        # Recrystallize
        {'vessel': 'filter'},
    ],
    'properties': [
        # Add
        {
            'reagent': 'LiCl and MeONa anhydrous THF solution',
            'volume': 15.0,
            'stir': False,
        },
        # HeatChill
        {
            'temp': 65,
            'time': 10800.0,
        },
        # HeatChillToTemp
        {
            'temp': 0.0,
        },
        # Add
        {
            'reagent': 'alkylphenones 1',
            'stir': True,
        },
        # Add
        {
            'reagent': 'diethyl oxalate',
            'mass': 0.95,
            'stir': True,
        },
        # HeatChill
        {
            'temp': 25.0,
            'time': 10800.0,
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Evaporate
        {
            'temp': 50,
            'pressure': 249.0,
            'time': DEFAULT_AUTO_EVAPORATION_TIME_LIMIT,
            'mode': 'auto',
        },
        # Transfer
        {
            'volume': 'all',
        },
        # HeatChillToTemp
        {
            'temp': 25.0,
        },
        # Add
        {
            'reagent': 'anhydrous EtOH',
            'volume': 15.0,
            'stir': True,
        },
        # Add
        {
            'reagent': 'trifluoroacetic acid',
            'mass': 1.14,
            'stir': True,
        },
        # Add
        {
            'reagent': 'arylhydrazine hydrochlorides 3',
            'stir': True,
        },
        # HeatChill
        {
            'temp': 78.5,
            'time': 43200.0,
        },
        # Add
        {
            'reagent': 'NaOH H2O solution',
            'volume': 2.0,
            'stir': True,
        },
        # HeatChill
        {
            'temp': 78.5,
            'time': 14400.0,
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Evaporate
        {
            'temp': 50,
            'pressure': 129.33333333333334,
            'time': DEFAULT_AUTO_EVAPORATION_TIME_LIMIT,
            'mode': 'auto',
        },
        # Add
        {
            'reagent': 'water',
            'volume': 15.0,
            'stir': False,
        },
        # Add
        {
            'reagent': 'methylene dichloride',
            'volume': 15.0,
            'stir': True,
        },
        # Add
        {
            'reagent': '10 % hydrochloric acid',
            'volume': 10.0,
            'stir': True,
        },
        # Separate
        {
            'purpose': 'extract',
            'solvent': 'methylene dichloride',
            'product_bottom': True,
            'solvent_volume': 10.0,
            'n_separations': 2,
        },
        # Separate
        {
            'purpose': 'wash',
            'solvent': 'water',
            'product_bottom': True,
            'solvent_volume': 20.0,
            'n_separations': 2,
            'through': 'anhydrous sodium sulfate',
        },
        # Evaporate
        {
            'temp': 50,
            'pressure': 145.5,
            'time': DEFAULT_AUTO_EVAPORATION_TIME_LIMIT,
            'mode': 'auto',
        },
        # Transfer
        {
            'volume': 'all'
        },
        # Recrystallize
        {},
    ],
}
