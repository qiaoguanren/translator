from chemputerxdl.steps import *
from xdl.steps import *
from synthreader.finishing.constants import (
    DEFAULT_SEPARATION_VOLUME, DEFAULT_DROPWISE_DISPENSE_SPEED)

CSSP16_TEXT = '''BuLi (11.2 mmol) was added dropwise to a stirred solution of indole in THF (40 ml) at -78 °C. After about 30 minutes CO2 (gas - dried through CaCl2 tube) was passed through the solution which was then allowed to stand for 10 minutes and the solvent was evaporated at 0 °C (1 mm Hg- using a pump attached directly to the reaction vessel). This takes about an hour. The resulting material was then dissolved in THF (40 ml) and cooled to -78 °C.

t-BuLi (18.7 mmol) was then added dropwise and the solution stirred for about 20 minutes. TsF (1.91 mL, 11 mmol) in THF (8 ml) was then added at -78 °C and the mixture stirred at this temperature for one hour and then allowed to warm to r.t. The reaction was then stirred at room temperature for a couple of hours and the solution then poured onto ice-brine solution and then extracted with ether. Purification was by chromatography using silica-gel, and petrol:ether as eluent (20:1, - 3:1, gradient) to give the product (1.04 g, 35%).'''

CSSP16_INFO = {
    'text': CSSP16_TEXT,
    'name': 'cssp16',
    'reagents': {
        'BuLi': {
            'quantities': ['11.2 mmol'],
        },
        'indole': {
            'quantities': [],
        },
        'THF': {
            'quantities': ['40 ml', '40 ml', '8 ml'],
        },
        'CO2': {
            'quantities': [],
        },
        't-BuLi': {
            'quantities': ['18.7 mmol'],
        },
        'TsF': {
            'quantities': ['1.91 mL', '11 mmol'],
        },
        'ice-brine solution': {
            'quantities': [],
        },
        'ether': {
            'quantities': [],
        },
        'silica-gel': {
            'quantities': [],
        },
        'unknown_reagent (35 %)': {
            'quantities': ['1.04 g', '35 %'],
        },
    },
    'steps': [
        HeatChillToTemp,
        Add,
        Add,
        StopHeatChill,
        Wait,
        Evaporate,
        Dissolve,
        HeatChillToTemp,
        Add,
        Stir,
        Add,
        Stir,
        HeatChillToTemp,
        HeatChill,
        Add,
        Separate,
        RunColumn,
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
        # Wait
        {},
        # Transfer
        {
            'from_vessel': 'reactor',
            'to_vessel': 'rotavap',
        },
        # Evaporate
        {
            'rotavap_name': 'rotavap',
        },
        # Dissolve
        {
            'vessel': 'rotavap',
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
        # Stir
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
        # HeatChillToTemp
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
            'to_vessel': 'reactor',
        },
        # RunColumn
        {
            'from_vessel': 'reactor',
            'to_vessel': 'reactor',
            'column': 'column',
        },
    ],
    'properties': [
        # HeatChillToTemp
        {
            'temp': -78.0,
        },
        # Add
        {
            'reagent': 'indole THF solution',
            'volume': 40.0,
            'stir': False,
        },
        # Add
        {
            'reagent': 'BuLi',
            'dispense_speed': DEFAULT_DROPWISE_DISPENSE_SPEED,
            'stir': True,
        },
        # StopHeatChill
        {},
        # Wait
        {
            'time': 60 * 10,
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
        # Dissolve
        {
            'solvent': 'THF',
            'volume': 40.0,
        },
        # Transfer
        {
            'volume': 'all',
        },
        # HeatChillToTemp
        {
            'temp': -78.0,
        },
        # Add
        {
            'reagent': 't-BuLi',
            'dispense_speed': DEFAULT_DROPWISE_DISPENSE_SPEED,
            'stir': True,
        },
        # Stir
        {
            'time': 1200.0,
        },
        # Add
        {
            'reagent': 'TsF THF solution',
            'volume': 9.91,
            'stir': True,
        },
        # Stir
        {
            'time': 3600.0,
        },
        # HeatChillToTemp
        {
            'temp': 18,
            'active': False,
            'continue_heatchill': False,
        },
        # Stir
        {
            'time': 2 * 3600,
        },
        # Add
        {
            'reagent': 'ice-brine solution',
            'stir': True,
        },
        # Separate
        {
            'purpose': 'extract',
            'solvent': 'ether',
            'product_bottom': False,
            'solvent_volume': DEFAULT_SEPARATION_VOLUME,
            'n_separations': 1,
        },
        # RunColumn
        {},
    ],
}
