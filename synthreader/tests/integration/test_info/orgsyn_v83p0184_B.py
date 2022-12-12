from chemputerxdl.steps import *
from xdl.steps import *

ORGSYN_V83P0184_B_TEXT = '''A 250-mL, single-necked, round-bottomed flask equipped with a 3.8 cm Teflon-coated magnetic stir bar and a condenser connected to a Drierite® drying tube is charged with absolute ethanol (50 mL) (Note 15), pyridine (7.33 mL, 7.20 g, 0.09 mol) (Note 16) and 1,1-dichloro-2-ethoxycyclopropane (10.86 g, 0.070 mol) (Note 17). The resulting mixture is stirred at a moderate speed at reflux for 48 h in an oil bath at 95 °C (bath temperature), and is then allowed to cool to room temperature before being concentrated under reduced pressure on a rotary evaporator (40 °C at 70 mmHg vacuum) until the volume is approximately 20 mL (Note 18). The residue is transferred to a 250-mL separatory funnel, and the flask is rinsed with water (2 × 50 mL) and dichloromethane (60 mL), which are also added to the separatory funnel. The mixture is shaken, and the organic layer is separated from the aqueous layer. The aqueous phase is extracted with dichloromethane (2 × 50 mL), and the combined organic phases are washed with a 0.7 M aqueous solution (2 × 100 mL) of copper sulfate (CuSO4) (Note 19), and dried with approximately 2 g of anhydrous magnesium sulfate (Note 10). The organic phase is then vacuum filtered into a 500-mL round-bottomed flask through a plug of aluminum oxide (Note 20). Dichloromethane (15 mL) is added to the flask containing the MgSO4 and after mixing the contents for approximately 1 min, the dichloromethane solution is filtered through the plug as well. The combined filtrates are then concentrated under reduced pressure on a rotary evaporator (25 °C at 70 mmHg) and transferred with approximately 2 mL of dichloromethane to a 50-mL round-bottomed flask for vacuum distillation (Notes 11, 21). The dichloromethane is removed at 21 °C and 30 mmHg. Following the removal of the dichloromethane, the apparatus is placed again under vacuum (30 mmHg) and the 25-mL receiving flask is submerged in an acetone/dry ice bath. The product is distilled with an oil bath temperature of 80–85 °C. Upon completion of the distillation, nitrogen gas is bled into the apparatus from the vacuum adaptor as the vacuum is released.'''

ORGSYN_V83P0184_B_INFO = {
    'text': ORGSYN_V83P0184_B_TEXT,
    'name': 'orgsyn_v83p0184_b',
    'reagents': {
        'absolute ethanol': {
            'quantities': ['50 mL'],
        },
        'pyridine': {
            'quantities': ['7.33 mL', '7.20 g', '0.09 mol'],
        },
        '1,1-dichloro-2-ethoxycyclopropane': {
            'quantities': ['10.86 g', '0.070 mol'],
        },
        'water': {
            'quantities': ['2 × 50 mL'],
        },
        'dichloromethane': {
            'quantities': ['60 mL', '2 × 50 mL', '15 mL', '2 mL'],
        },
        'copper sulfate(CuSO4)': {
            'quantities': ['2 × 100 mL'],
        },
        'anhydrous magnesium sulfate': {
            'quantities': ['2 g'],
        },
        'the MgSO4': {
            'quantities': [],
        },
        'the dichloromethane solution': {
            'quantities': [],
        },
        'the dichloromethane': {
            'quantities': [],
        },
    },
    'steps': [
        Add,
        Add,
        Add,
        HeatChill,
        HeatChillToTemp,
        Evaporate,
        Repeat,
        Add,
        Separate,
        Separate,
        Separate,
        Add,
        Stir,
        Filter,
        Evaporate,
        Add,
        HeatChillToTemp,
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
        # HeatChill
        {
            'vessel': 'reactor',
        },
        # HeatChillToTemp
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
            'to_vessel': 'separator',
        },
        # Repeat
        {
            'children':  [
                # Add
                {
                    'vessel': 'rotavap',
                },
                # Transfer
                {
                    'from_vessel': 'rotavap',
                    'to_vessel': 'separator',
                }
            ]
        },
        # Add
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
            'to_vessel': 'buffer_flask1',
            'waste_phase_to_vessel': 'separator',
        },
        # Separate
        {
            'from_vessel': 'separator',
            'separation_vessel': 'separator',
            'to_vessel': 'separator',
        },
        # Transfer
        {
            'from_vessel': 'buffer_flask1',
            'to_vessel': 'separator',
        },
        # Separate
        {
            'from_vessel': 'separator',
            'separation_vessel': 'separator',
            'to_vessel': 'filter',
        },
        # Add
        {
            'vessel': 'filter',
        },
        # Stir
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
        # Transfer
        {
            'from_vessel': 'rotavap',
            'to_vessel': 'reactor',
        },
        # Add
        {
            'vessel': 'reactor',
        },
        # HeatChillToTemp
        {
            'vessel': 'reactor',
        },
        # Distill
        {},
    ],
    'properties': [
        # Add
        {
            'reagent': 'absolute ethanol',
            'volume': 50.0,
            'stir': False,
        },
        # Add
        {
            'reagent': 'pyridine',
            'volume': 7.33,
            'stir': True,
        },
        # Add
        {
            'reagent': '1,1-dichloro-2-ethoxycyclopropane',
            'mass': 10.86,
            'stir': True,
        },
        # HeatChill
        {
            'temp': 95.0,
            'time': 172800.0,
        },
        # HeatChillToTemp
        {
            'temp': 25,
            'active': False,
            'continue_heatchill': False,
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Evaporate
        {
            'temp': 40,
            'pressure': 93.3254,
        },
        # Transfer
        {
            'volume': 'all'
        },
        # Repeat
        {
            'repeats': 2,
            'children': [
                # Add
                {
                    'reagent': 'water',
                    'volume': 50.0,
                    'stir': True,
                },
                # Transfer
                {
                    'volume': 'all'
                }
            ]
        },
        # Add
        {
            'reagent': 'dichloromethane',
            'volume': 60.0,
            'stir': True,
        },
        # Transfer
        {
            'volume': 'all'
        },
        # Separate
        {
            'purpose': 'extract',
            'product_bottom': True,
            'n_separations': 1,
            'solvent': '',
        },
        # Separate
        {
            'purpose': 'extract',
            'product_bottom': True,
            'solvent': 'dichloromethane',
            'solvent_volume': 50.0,
            'n_separations': 2,
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Separate
        {
            'purpose': 'wash',
            'product_bottom': True,
            'solvent': 'copper sulfate(CuSO4) water solution',
            'through': 'anhydrous magnesium sulfate',
            'solvent_volume': 100.0,
            'n_separations': 2,
        },
        # Add
        {
            'reagent': 'dichloromethane',
            'volume': 15.0,
            'stir': False,
        },
        # Stir
        {
            'time': 60,
        },
        # Filter
        {
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Evaporate
        {
            'temp': 25,
            'pressure': 93.3254,
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Add
        {
            'reagent': 'dichloromethane',
            'volume': 2,
        },
        # HeatChillToTemp
        {
            'temp': -78,
        },
        # Distill
        {},
    ],
}
