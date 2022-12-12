from chemputerxdl.steps import *
from xdl.steps import *
from synthreader.finishing.constants import (
    DEFAULT_AUTO_EVAPORATION_TIME_LIMIT,
    DEFAULT_SEPARATION_VOLUME
)

EPILUPININE_5A_TEXT = '''A mixture of proline methyl ester (1.04 g, 8.0 mmol), Et3N (0.28 mL, 2.0 mmol) and 5-bromo-l-diazo-2-pentanone (0.382 g, 2.0 mmol) in EtOAc (8.0 mL) was stirred overnight at 60 °C. The reaction mixture was then transferred to a separatory funnel along with 100 mL of EtOAc, and washed with saturated NaHCO 3 solution, dried over anhydrous MgSO4, filtered and concentrated to give a yellow liquid. Flash column chromatography (silica gel, 3.5-cm x 24-cm column, 1:I followed by 7:3 EtOAc/hexanes, EtOAc and 1:19 MeOH/EtOAc) provided 0.362 g (76%) of 5a as a yellow oil: [ct]z2n = -61.5 o (c 0.5, CHCI3); Rf 0.11 (EtOAc); IR (neat) 2953, 2103, 1738, 1642, 1373, 1177 cm1; ~H NMR (CDC13, 300 MHz) 8 5.33 (s, 1H), 3.71 (s, 3H), 3.19-3.14 (m, 1H), 3.16 (dd, 1H, J = 8.9, 5.8 Hz), 2.69 (dt, 1H, J= 11.9, 7.7 Hz), 2.42 (m, 3H), 2.32 (dd, 1H, J = 16.7, 8.1 Hz), 2.17-2.03 (m, 1H), 1.98-1.86 (m, 3H), 1.81 (quintet, 2H, J= 7.4 Hz); ~3C NMR (CDCI3, 75 MHz) 6 194.7, 174.5, 65.9, 54.2, 54.0, 53.1, 51.6, 38.4, 29.2, 23.9, 23.1. Anal. Calcd for CuH~TN303: C, 55.03; H, 7.19; N, 17.64. Found: C, 55.11; H, 7.20; N, 17.36. '''

EPILUPININE_5A_INFO = {
    'text': EPILUPININE_5A_TEXT,
    'name': 'epilupinine_5a',
    'reagents': {
        'EtOAc': {
            'quantities': ['100 mL'],
        },
        'saturated NaHCO 3 solution': {
            'quantities': [],
        },
        'anhydrous MgSO4': {
            'quantities': [],
        },
        '5a (76 %)': {
            'quantities': ['0.362 g', '76 %'],
        },
    },
    'steps': [
        Add,
        HeatChillToTemp,
        Stir,
        StopHeatChill,
        Add,
        Separate,
        Evaporate,
        RunColumn,
    ],
    'vessels': [
        # Add
        {
            'vessel': 'reactor',
        },
        # HeatChillToTemp
        {
            'vessel': 'reactor',
        },
        # Stir
        {
            'vessel': 'reactor',
        },
        # StopHeatChill
        {
            'vessel': 'reactor',
        },
        # Transfer
        {
            'from_vessel': 'reactor',
            'to_vessel': 'separator',
        },
        # Add
        {
            'vessel': 'separator',
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
        },
    ],
    'properties': [
        # Add
        {
            'reagent': 'A mixture of proline methyl ester ( 1.04 g , 8.0 mmol ) , Et3N ( 0.28 mL , 2.0 mmol ) and 5-bromo-l-diazo-2-pentanone ( 0.382 g , 2.0 mmol ) in EtOAc ( 8.0 mL )',
            'volume': 8.28,
        },
        # HeatChillToTemp
        {
            'temp': 60.0,
        },
        # Stir
        {
            'time': 57600.0,
        },
        # StopHeatChill
        {},
        # Transfer
        {
            'volume': 'all',
        },
        # Add
        {
            'reagent': 'EtOAc',
            'volume': 100.0,
            'stir': True,
        },
        # Separate
        {
            'purpose': 'wash',
            'solvent': 'saturated NaHCO 3 solution',
            'product_bottom': False,
            'solvent_volume': DEFAULT_SEPARATION_VOLUME,
            'n_separations': 1,
            'through': 'anhydrous MgSO4',
        },
        # Evaporate
        {
            'time': DEFAULT_AUTO_EVAPORATION_TIME_LIMIT,
            'mode': 'auto',
        },
        # RunColumn
        {},
    ],
}
