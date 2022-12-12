from chemputerxdl.steps import *
from xdl.steps import *

ORGSYN_V95P0142_A_TEXT = '''N-Boc hydroxyl-amine (44.0 g, 330 mmol, 1.0 equiv) (Note 2) is introduced into a 2-L round-bottomed flask equipped with a 4-cm oval Teflon-coated stir-bar and is dissolved with CH2Cl2 (1.10 L). The reaction mixture is cooled to 4 °C in an ice-water bath after which a 250-mL addition funnel is attached. Triethylamine (49.0 mL, 363 mmol, 1.10 equiv) is transferred into the addition funnel via a graduated cylinder, and added dropwise over 15 min. Dichloromethane (20 mL) is used to ensure that no reagents are left on the side. tert-Butyldimethylsilylchloride (49.7 g, 330 mmol, 1.0 equiv) is dissolved in CH2Cl2 (150 mL) and added dropwise over 60 min via the addition funnel at 4 ºC. Dichloromethane (50 mL) is used to ensure that no reagent is left on the side of the addition funnel (final concentration of substrate is 0.25 M). The addition funnel is removed, the flask is equipped with a nitrogen inlet, and the reaction is stirred for 16 h at 23 °C under nitrogen (Note 3). Water (250 mL) is added and the mixture is poured into a 2-L separatory funnel. The reaction flask is rinsed with CH2Cl2 (50 mL) and the combined organic layer is separated and washed with saturated aqueous NaCl (250 mL). The organic layer is dried over MgSO4 (20 g) and filtered by suction using a fritted funnel. Dichloromethane (50 mL) is used to wash the MgSO4 and the filtrate is concentrated by rotary evaporation in a 2-L round-bottomed flask (40 °C bath, 425-30 mmHg). The resulting oil, which contains tert-butyl (tert-butyldimethylsilyl)oxycarbamate, is transferred to a 500-mL round-bottomed flask using CH2Cl2, which is then evaporated (40 °C bath, 425-30 mmHg). The product is dried on the vacuum pump (0.5 mmHg) for 48 h affording the desired compound (81.3 g, 329 mmol, 99.5% yield, 97.5% purity) as a white solid (Notes 4 and 5).'''

ORGSYN_V95P0142_A_INFO = {
    'text': ORGSYN_V95P0142_A_TEXT,
    'name': 'orgsyn_v95p0142_a',
    'reagents': {
        'N-Boc hydroxyl-amine': {
            'quantities': ['44.0 g', '330 mmol', '1.0 equiv'],
        },
        'CH2Cl2': {
            'quantities': ['1.10 L', '150 mL', '50 mL'],
        },
        'triethylamine': {
            'quantities': ['49.0 mL', '363 mmol', '1.10 equiv'],
        },
        'dichloromethane': {
            'quantities': ['20 mL', '50 mL', '50 mL'],
        },
        'the side': {
            'quantities': [],
        },
        'tert-Butyldimethylsilylchloride': {
            'quantities': ['49.7 g', '330 mmol', '1.0 equiv'],
        },
        'water': {
            'quantities': ['250 mL'],
        },
        'saturated aqueous NaCl': {
            'quantities': ['250 mL'],
        },
        'MgSO4': {
            'quantities': ['20 g'],
        },
        'the MgSO4': {
            'quantities': [],
        },
    },
    'steps': [
        Add,
        Dissolve,
        HeatChillToTemp,
        Add,
        Add,
        Confirm,
        Dissolve,
        Add,
        HeatChill,
        Add,
        Add,
        Separate,
        Separate,
        Add,
        Evaporate,
        Add,
        Evaporate,
        Dry,
    ],
    'vessels': [
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
        # Add
        {
            'vessel': 'reactor',
        },
        # Confirm
        {},
        # Dissolve
        {
            'vessel': 'filter',
        },
        # Transfer
        {
            'from_vessel': 'filter',
            'to_vessel': 'reactor',
        },
        # Add
        {
            'vessel': 'filter',
        },
        # Transfer
        {
            'from_vessel': 'filter',
            'to_vessel': 'reactor',
        },
        # HeatChill
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
        # Add
        {
            'vessel': 'separator',
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
            'through': 'MgSO4',
        },
        # Add
        {
            'vessel': 'rotavap',
            'through': 'MgSO4',
        },
        # Evaporate
        {
            'rotavap_name': 'rotavap',
        },
        # Add
        {
            'vessel': 'rotavap',
        },
        # Evaporate
        {
            'rotavap_name': 'rotavap',
        },
        # Dry
        {
            'vessel': 'rotavap',
        },
    ],
    'properties': [
        # Add
        {
            'reagent': 'N-Boc hydroxyl-amine',
            'mass': 44.0,
            'stir': False,
        },
        # Dissolve
        {
            'solvent': 'CH2Cl2',
            'volume': 1100.0,
        },
        # HeatChillToTemp
        {
            'temp': 4.0,
        },
        # Add
        {
            'reagent': 'triethylamine',
            'volume': 49.0,
            'time': 900.0,
            'stir': True,
        },
        # Add
        {
            'reagent': 'dichloromethane',
            'volume': 20.0,
            'stir': True,
        },
        # Confirm
        {
            'msg': 'Is tert-Butyldimethylsilylchloride ( 49.7 g , 330 mmol , 1.0 equiv ) in the correct vessel?',
        },
        # Dissolve
        {
            'solvent': 'CH2Cl2',
            'volume': 150.0,
        },
        # Transfer
        {
            'volume': 'all',
            'time': 3600.0,
        },
        # Add
        {
            'reagent': 'dichloromethane',
            'volume': 50.0,
            'stir': True,
        },
        # Transfer
        {
            'volume': 'all',
        },
        # HeatChill
        {
            'temp': 23.0,
            'time': 57600.0,
        },
        # Add
        {
            'reagent': 'water',
            'volume': 250.0,
            'stir': True,
        },
        # Transfer
        {
            'volume': 'all'
        },
        # Add
        {
            'reagent': 'CH2Cl2',
            'volume': 50.0,
            'stir': True,
        },
        # Separate
        {
            'purpose': 'extract',
            'product_bottom': True,
            'solvent': '',
            'n_separations': 1,
        },
        # Separate
        {
            'purpose': 'wash',
            'product_bottom': True,
            'solvent': 'saturated aqueous NaCl',
            'solvent_volume': 250.0,
            'n_separations': 1,
        },
        # Add
        {
            'reagent': 'dichloromethane',
            'volume': 50.0,
            'stir': False,
            'through': 'MgSO4'
        },
        # Evaporate
        {
            'temp': 40.0,
            'pressure': 303.30755,
            'time': 1800,
            'mode': 'auto',
        },
        # Add
        {
            'reagent': 'CH2Cl2',
            'volume': 0,
            'stir': False,
        },
        # Evaporate
        {
            'temp': 40.0,
            'pressure': 303.30755,
            'time': 1800,
            'mode': 'auto',
        },
        # Dry
        {
            'time': 172800.0,
            'vacuum_pressure': 0.66661,
        },
    ],
}
