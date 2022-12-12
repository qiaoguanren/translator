from chemputerxdl.steps import *
from xdl.steps import *
from synthreader.finishing.constants import (
    DEFAULT_DROPWISE_DISPENSE_SPEED,
    DEFAULT_ALLOWED_TO_COOL_TIME,
    DEFAULT_AUTO_EVAPORATION_TIME_LIMIT
)

# https://pubs.acs.org/doi/suppl/10.1021/acs.orglett.5b00987/suppl_file/ol5b00987_si_001.pdf

DMERYTH_STEP1_TEXT = '''2-(3,4-Dimethoxyphenyl)ethylamine (15.2mL, 90.0mmol, 1.0equiv) was dissolved in CH2Cl2 (90mL) and NEt3 (18.9mL, 135.0mmol, 1.5equiv). Pent-4-enoyl chloride 6 (10.680g, 90.0 mmol, 1.0 equiv) was added dropwise at 0ºC and after continued stirring at 0ºC for 30 min the mixture was allowed to warm to room temperature (23ºC). After additional stirring for 20h, the mixture was concentrated and the  residue  was  dissolved  in  EtOAc  (300mL).  The  solution  was  transferred  into  a  separation  funnel  and washed with aq HCl (1M, 300mL) followed by brine (100mL). The organic layer was separated, dried over Na2SO4 and   concentrated   to   receive   pure N-(3,4-Dimethoxyphenethyl)pent-4-enamide   as   a   brown   oil   (23.730g, 90.0mmol)  in  quantitative  yield.'''

DMERYTH_STEP1_INFO = {
    'text': DMERYTH_STEP1_TEXT,
    'name': 'dmeryth_step1',
    'reagents': {
        '2-(3,4-Dimethoxyphenyl)ethylamine': {
            'quantities': ['15.2 mL', '90.0 mmol', '1.0 equiv'],
        },
        'CH2Cl2': {
            'quantities': ['90 mL'],
        },
        'NEt3': {
            'quantities': ['18.9 mL', '135.0 mmol', '1.5 equiv'],
        },
        'pent-4-enoyl chloride 6': {
            'quantities': ['10.680 g', '90.0 mmol', '1.0 equiv'],
        },
        'EtOAc': {
            'quantities': ['300 mL'],
        },
        'aqueous HCl': {
            'quantities': ['1M', '300 mL'],
        },
        'brine': {
            'quantities': ['100 mL'],
        },
        'Na2SO4': {
            'quantities': [],
        },
        'pure N-(3,4-Dimethoxyphenethyl)pent-4-enamide': {
            'quantities': [],
        },
    },
    'steps': [
        Add,
        Add,
        Dissolve,
        HeatChillToTemp,
        Add,
        Stir,
        HeatChillToTemp,
        Stir,
        Evaporate,
        Dissolve,
        Separate,
        Separate,
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
        # Dissolve
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
        # HeatChillToTemp
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
        # Dissolve
        {
            'vessel': 'rotavap',
        },
        # Transfer
        {
            'from_vessel': 'rotavap',
            'to_vessel': 'separator',
        },
        # Separate
        {
            'from_vessel': 'separator',
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
    ],
    'properties': [
        # Add
        {
            'reagent': '2-(3,4-Dimethoxyphenyl)ethylamine',
            'volume': 15.2,
            'stir': False,
        },
        # Add
        {
            'reagent': 'CH2Cl2',
            'volume': 90.0,
            'stir': True,
        },
        # Dissolve
        {
            'solvent': 'NEt3',
            'volume': 18.9,
        },
        # HeatChillToTemp
        {
            'temp': 0.0,
        },
        # Add
        {
            'reagent': 'pent-4-enoyl chloride 6',
            'mass': 10.68,
            'dispense_speed': DEFAULT_DROPWISE_DISPENSE_SPEED,
            'stir': True,
        },
        # Stir
        {
            'time': 1800.0,
        },
        # HeatChillToTemp
        {
            'temp': 18,
            'active': False,
            'continue_heatchill': False,
        },
        # Stir
        {
            'time': 72000.0,
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Evaporate
        {
            'temp': 50,
            'pressure': 699.0,
            'time': DEFAULT_AUTO_EVAPORATION_TIME_LIMIT,
            'mode': 'auto',
        },
        # Dissolve
        {
            'solvent': 'EtOAc',
            'volume': 300.0,
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Separate
        {
            'purpose': 'wash',
            'solvent': 'aqueous HCl',
            'product_bottom': False,
            'solvent_volume': 300.0,
            'n_separations': 1,
        },
        # Separate
        {
            'purpose': 'wash',
            'solvent': 'brine',
            'product_bottom': False,
            'solvent_volume': 100.0,
            'n_separations': 1,
            'through': 'Na2SO4',
        },
        # Evaporate
        {
            'temp': 50,
            'pressure': 153.0,
            'time': DEFAULT_AUTO_EVAPORATION_TIME_LIMIT,
            'mode': 'auto',
        },
    ],
}
