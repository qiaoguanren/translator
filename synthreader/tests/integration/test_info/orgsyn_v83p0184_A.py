from chemputerxdl.steps import *
from xdl.steps import *
from synthreader.finishing.constants import DEFAULT_AUTO_EVAPORATION_TIME_LIMIT

ORGSYN_V83P0184_A_TEXT = '''A 250-mL, three-necked, round-bottomed flask equipped with a septum, a 3.8 cm Teflon-coated magnetic stir bar and a condenser connected to a drying tube containing Drierite® is charged with ethyl vinyl ether (9.55 mL, 7.20 g, 0.10 mol) (Note 1), chloroform (31.9 mL, 47.8 g, 0.40 mol) (Note 2), and benzyltriethylammonium chloride (TEBA) (0.100 g, 0.44 mmol) (Note 3) and placed in an ice bath (Note 4). After the reaction flask is cooled for 10 min, the mixture is stirred vigorously (Note 5) and 24 g of a viscous 50% aqueous solution of sodium hydroxide (NaOH) (12.0 g, 0.30 mol in 12 mL of H2O) (Note 6) is added dropwise via a syringe in 10 min (Note 7). The reaction mixture is stirred vigorously at bath temperature (approximately 0 °C) for 2 h and at room temperature for 22 h. The reaction mixture is then cooled in an ice bath and quenched by injecting 6 M hydrochloric acid (30 mL) dropwise over a 10 min period (Note 8). The hydrolysate is transferred to a 500-mL separatory funnel, and the flask is rinsed with water (2 × 20 mL) and dichloromethane (30 mL), which is also added to the funnel. After addition of more water (60 mL) to the funnel, the mixture is shaken and the organic layer is separated from the aqueous layer. The aqueous layer is extracted with dichloromethane (3 × 60 mL) (Note 9). The combined organic extracts are dried with approximately 2 g of anhydrous magnesium sulfate (MgSO4) (Note 10), vacuum filtered, and concentrated under reduced pressure on a rotary evaporator (25 °C at 70 mmHg) to afford a pale yellow residue. This residue is transferred to a 50-mL round bottom flask using approximately 2 mL of dichloromethane (Note 11). The dichloromethane is removed at 30–35 °C (oil bath temperature) at 50 mmHg, and the product is distilled at 65–70 °C (oil bath temperature) at 30 mmHg to give 12.94 g (84%) (Note 12) of 1,1-dichloro-2-ethoxycyclopropane (Note 13) as a colorless liquid, bp 55 °C/30 mmHg.'''

ORGSYN_V83P0184_A_INFO = {
    'text': ORGSYN_V83P0184_A_TEXT,
    'name': 'orgsyn_v83p0184_a',
    'reagents': {
        'ethyl vinyl ether': {
            'quantities': ['9.55 mL', '7.20 g', '0.10 mol'],
        },
        'chloroform': {
            'quantities': ['31.9 mL', '47.8 g', '0.40 mol'],
        },
        'benzyltriethylammonium chloride(TEBA)': {
            'quantities': ['0.100 g', '0.44 mmol'],
        },
        'sodium hydroxide(NaOH) (12.0 g , 0.30 mol in 12 mL of H2O)': {
            'quantities': ['12.0 g , 0.30 mol in 12 mL of H2O', '12.0 g'],
        },
        'water': {
            'quantities': ['12 mL', '2 × 20 mL', '60 mL'],
        },
        '6 M hydrochloric acid': {
            'quantities': ['30 mL'],
        },
        'the hydrolysate': {
            'quantities': [],
        },
        'dichloromethane': {
            'quantities': ['30 mL', '3 × 60 mL', '2 mL'],
        },
        'anhydrous magnesium sulfate(MgSO4)': {
            'quantities': ['2 g'],
        },
        'the dichloromethane': {
            'quantities': [],
        },
        '1,1-dichloro-2-ethoxycyclopropane (84 %)': {
            'quantities': ['12.94 g', '84 %'],
        },
    },
    'steps': [
        Add,
        Add,
        Add,
        HeatChillToTemp,
        Stir,
        Add,
        Stir,
        HeatChill,
        HeatChillToTemp,
        Add,
        Repeat,
        Add,
        Add,
        Separate,
        Separate,
        Evaporate,
        Add,
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
        # Add
        {
            'vessel': 'reactor',
        },
        # Stir
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
        # Transfer
        {
            'from_vessel': 'reactor',
            'to_vessel': 'separator',
        },
        # Repeat
        {
            'children': [
                # Add
                {
                    'vessel': 'reactor',
                },
                # Transfer
                {
                    'from_vessel': 'reactor',
                    'to_vessel': 'separator',
                }
            ]
        },
        # Add
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
            'to_vessel': 'rotavap',
            'separation_vessel': 'separator',
            'waste_phase_to_vessel': 'separator',
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
        # Add
        {
            'vessel': 'rotavap',
        },
        # Distill
        {},
    ],
    'properties': [
        # Add
        {
            'reagent': 'ethyl vinyl ether',
            'volume': 9.55,
            'stir': False,
        },
        # Add
        {
            'reagent': 'chloroform',
            'volume': 31.9,
            'stir': True,
        },
        # Add
        {
            'reagent': 'benzyltriethylammonium chloride(TEBA)',
            'mass': 0.1,
            'stir': True,
        },
        # HeatChillToTemp
        {
            'temp': 0.0,
        },
        # Stir
        {
            'time': 600.0,
        },
        # Add
        {
            'reagent': 'sodium hydroxide(NaOH) (12.0 g , 0.30 mol in 12 mL of H2O) water solution',
            'volume': 12.0,
            'time': 600.0,
            'stir': True,
            'stir_speed': 600,
            'viscous': True,
        },
        # Stir
        {
            'time': 7200.0,
            'stir_speed': 600,
        },
        # HeatChill
        {
            'temp': 25.0,
            'time': 79200.0,
            'stir_speed': 600,
        },
        # HeatChillToTemp
        {
            'temp': 0,
        },
        # Add
        {
            'reagent': '6 M hydrochloric acid',
            'volume': 30.0,
            'time': 600.0,
            'stir': True,
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Repeat
        {
            'repeats': 2,
            'children': [
                # Add
                {
                    'reagent': 'water',
                    'volume': 20.0,
                    'stir': True,
                },
                # Transfer
                {
                    'volume': 'all',
                },
            ],
        },
        # Add
        {
            'reagent': 'dichloromethane',
            'volume': 30.0,
            'stir': True,
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Add
        {
            'reagent': 'water',
            'volume': 60.0,
            'stir': True,
        },
        # Separate
        {
            'purpose': 'extract',
            'product_bottom': True,
            'solvent': '',
            'n_separations': 1,
            'through': 'anhydrous magnesium sulfate(MgSO4)'
        },
        # Separate
        {
            'purpose': 'extract',
            'product_bottom': True,
            'solvent': 'dichloromethane',
            'solvent_volume': 60.0,
            'n_separations': 3,
            'through': 'anhydrous magnesium sulfate(MgSO4)'
        },
        # Evaporate
        {
            'time': DEFAULT_AUTO_EVAPORATION_TIME_LIMIT,
            'mode': 'auto',
        },
        # Add
        {
            'reagent': 'dichloromethane',
            'volume': 2.0,
            'stir': False,
        },
        # Distill
        {},
    ],
}
