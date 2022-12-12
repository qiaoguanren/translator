from chemputerxdl.steps import *
from xdl.steps import *
from synthreader.finishing.constants import DEFAULT_AUTO_EVAPORATION_TIME_LIMIT

# DOI: 10.1055/s-0032-1317668
# SI Section 2
# https://www.thieme-connect.de/media/synlett/201220/supmat/sup_st-2012-w0785-l_10-1055_s-0032-1317668.pdf

ACROMELOBINIC_ACID_SI2_TEXT = '''An  oven-dried  vial  was  charged  with  LiCl  (0.32  g,  7.5  mmol)  and  EtONa  (0.51  g,  7.5  mmol)  in  anhydrous THF (15 mL). The mixture was stirred at reflux for 3 h and then cooled to 0 °C. To the resulted solution were added propiophenone 1a (0.67 g, 5.0 mmol) and diethyl oxalate (0.95g, 6.5 mmol)  at  0 °C,  and  the  resulting  mixture  was  allowed  to  stir  at  room  temperature  for  3  h.  The  mixture was concentrated to remove THF giving a residual, to which were added water (15 mL), methylene  chloride  (15  mL)  and  10%  hydrochloric  acid  (ca.  3  mL)  until  pH  3–4  to  make  the  solution  partitioned  into  organic  and  aqueous  layers.  The  aqueous  layer  was  extracted  with  methylene chloride (10 mL × 2). The combined organic phase was washed with water (20 mL × 2), dried over anhydrous sodium sulfate, and concentrated to give a crude oil, which was purified by column chromatography (200–300 mesh silica gel, petroleum ether/ethyl acetate 20:1) to offer the 2a (0.86  g,  74%), ethyl benzoate  (0.11  g,  15%)  and  ethyl  2-hydroxy-3-methyl-4,5-dioxohept-2-  enoate (0.07 g, 13%).'''

ACROMELOBINIC_ACID_SI2_INFO = {
    'text': ACROMELOBINIC_ACID_SI2_TEXT,
    'name': 'acromelobinic_acid_si2',
    'reagents': {
        'LiCl': {
            'quantities': ['0.32 g', '7.5 mmol'],
        },
        'EtONa': {
            'quantities': ['0.51 g', '7.5 mmol'],
        },
        'anhydrous THF': {
            'quantities': ['15 mL'],
        },
        'propiophenone 1a': {
            'quantities': ['0.67 g', '5.0 mmol'],
        },
        'diethyl oxalate': {
            'quantities': ['0.95 g', '6.5 mmol'],
        },
        'THF': {
            'quantities': [],
        },
        'water': {
            'quantities': ['15 mL', '20 mL × 2'],
        },
        'methylene chloride': {
            'quantities': ['15 mL', '10 mL × 2'],
        },
        '10 % hydrochloric acid': {
            'quantities': ['3 mL'],
        },
        'anhydrous sodium sulfate': {
            'quantities': [],
        },
        'the 2a (74 %)': {
            'quantities': ['0.86 g', '74 %'],
        },
        'ethyl benzoate (15 %)': {
            'quantities': ['0.11 g', '15 %'],
        },
        'ethyl 2 hydroxy-3 methyl-4,5-dioxohept-2- enoate (13 %)': {
            'quantities': ['0.07 g', '13 %'],
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
        Add,
        Add,
        Add,
        Separate,
        Separate,
        Evaporate,
        RunColumn,
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
        # RunColumn
        {
            'from_vessel': 'rotavap',
            'to_vessel': 'reactor',
            'column': 'column',
        },
    ],
    'properties': [
        # Add
        {
            'reagent': 'LiCl and EtONa anhydrous THF solution',
            'volume': 15.0,
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
            'reagent': 'propiophenone 1a',
            'mass': 0.67,
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
        # Add
        {
            'reagent': 'water',
            'volume': 15.0,
            'stir': False,
        },
        # Add
        {
            'reagent': 'methylene chloride',
            'volume': 15.0,
            'stir': True,
        },
        # Add
        {
            'reagent': '10 % hydrochloric acid',
            'volume': 3.0,
            'stir': True,
        },
        # Separate
        {
            'purpose': 'extract',
            'solvent': 'methylene chloride',
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
            'time': 1800,
            'mode': 'auto',
        },
        # RunColumn
        {},
    ],
}
