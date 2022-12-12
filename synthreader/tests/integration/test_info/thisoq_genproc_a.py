from chemputerxdl.steps import *
from xdl.steps import *
from synthreader.finishing.constants import DEFAULT_DROPWISE_DISPENSE_SPEED

# General procedure A from this paper (DOI in URL):
#   https://pubs.acs.org/doi/suppl/10.1021/acs.orglett.5b00987/suppl_file/ol5b00987_si_001.pdf

THISOQ_GENPROC_A_TEXT = '''In a round-bottom flask equipped with a magnetic stir bar, the desired phenyl ethyl amine S1 (10.0 mmol) was dissolved in CH2Cl2 (20 mL). NEt3 (2.10 mL, 15.0 mmol, 1.5 equiv) was added with stirring. The corresponding acid chloride S2 (10.0 mmol, 1.0 equiv) was added dropwise at 0 ºC and after continued  stirring  at  0 ºC  for  30  min  the  mixture  was  allowed  to  warm  to  room  temperature  (23 ºC).  After additional stirring for 20–24 h, the mixture was concentrated and the residue was redissolved in EtOAc (40 mL). The solution was transferred into a separation funnel and washed with aq HCl (1 M, 40 mL) followed by brine (40 mL). The organic layer was separated, dried over Na2SO4 and concentrated to yield the pure amide S3, which was transferred to the cyclization.'''

THISOQ_GENPROC_A_INFO = {
    'text': THISOQ_GENPROC_A_TEXT,
    'name': 'thisoq_genproc_a',
    'reagents': {
        'phenyl ethyl amine S1': {
            'quantities': ['10.0 mmol'],
        },
        'CH2Cl2': {
            'quantities': ['20 mL'],
        },
        'NEt3': {
            'quantities': ['2.10 mL', '15.0 mmol', '1.5 equiv'],
        },
        'acid chloride S2': {
            'quantities': ['10.0 mmol', '1.0 equiv'],
        },
        'EtOAc': {
            'quantities': ['40 mL'],
        },
        'aqueous HCl': {
            'quantities': ['1 M', '40 mL'],
        },
        'brine': {
            'quantities': ['40 mL'],
        },
        'Na2SO4': {
            'quantities': [],
        },
    },
    'steps': [
        Confirm,
        Dissolve,
        Add,
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
        # Confirm
        {},
        # Dissolve
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
        # Confirm
        {
            'msg': 'Is phenyl ethyl amine S1 ( 10.0 mmol ) in the correct vessel?',
        },
        # Dissolve
        {
            'solvent': 'CH2Cl2',
            'volume': 20.0,
        },
        # Add
        {
            'reagent': 'NEt3',
            'volume': 2.1,
            'stir': True,
        },
        # HeatChillToTemp
        {
            'temp': 0.0,
        },
        # Add
        {
            'reagent': 'acid chloride S2',
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
            'time': 79200.0,
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Evaporate
        {
            'temp': 50,
            'pressure': 699.0,
            'time': 1800,
            'mode': 'auto',
        },
        # Dissolve
        {
            'solvent': 'EtOAc',
            'volume': 40.0,
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
            'solvent_volume': 40.0,
            'n_separations': 1,
        },
        # Separate
        {
            'purpose': 'wash',
            'solvent': 'brine',
            'product_bottom': False,
            'solvent_volume': 40.0,
            'n_separations': 1,
            'through': 'Na2SO4',
        },
        # Evaporate
        {
            'temp': 50,
            'pressure': 153.0,
            'time': 1800,
            'mode': 'auto',
        },
    ],
}
