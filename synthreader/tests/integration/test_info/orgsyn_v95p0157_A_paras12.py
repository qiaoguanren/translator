from chemputerxdl.steps import *
from xdl.steps import *

ORGSYN_V95P0157_A_PARAS12_TEXT = '''The aldehyde 1 (15.0 g, 39.9 mmol, 1.0 equiv, 94% ee) (Note 2) is dissolved in MeOH (200 mL, concentration of substrate is 0.20 M) (Note 3) in a 500-mL, three-necked, round-bottomed flask equipped with a 4-cm Teflon-coated magnetic stir-bar, a plastic stopper, a low-temperature thermometer and a rubber septum through which a positive nitrogen atmosphere is ensured (Note 3) (Figure 1) . The reaction mixture is cooled to -20 ºC using an CH3CN-dry ice bath. Sodium borohydride (3.02 g, 79.8 mmol, 2.0 equiv) is added in ten portions (~300 mg every three min) via the neck with the plastic stopper, and the internal temperature is maintained at -20 ºC.

After complete addition, the reaction is stirred for 45 min in the CH3CN-dry ice bath at -20 ºC, after which the reaction is allowed to warm up to 0 ºC. The reaction is monitored by TLC in 25% EtOAc in hexanes using ninhydrin to stain (Note 4). After stirring for 35 min at 0 ºC, TLC analysis shows disappearance of starting material. To the completed reaction, a mixture of ice-water (170 mL) is added to the solution with vigorous stirring and the solution is stirred for 10 min at 0 ºC (Note 5). To this mixture EtOAc (900 mL) and H2O (50 mL) are added and the resultant mixture is poured into a 2-L separatory funnel. Ethyl acetate (50 mL) and H2O (50 mL) are used to rinse the flask. The aqueous layer is extracted with EtOAc (3 x 150 mL). The combined organic layers are washed with saturated aqueous NH4Cl (100 mL) and saturated aqueous NaCl (100 mL). The organic layer is dried over Na2SO4 (20 g) and filtered by suction using a fritted funnel (9 cm diameter, medium porosity). Additional EtOAc (50 mL) is used to wash the Na2SO4 and the filtrate is concentrated by rotary evaporation into a 2-L round-bottomed flask (40 °C bath, 140-30 mmHg). The resulting pale yellow oil, containing ethyl N-(tert-butoxycarbonyl)-N-((tert-butyldimethylsilyl)oxy)-L-homoserinate (i.e., 2) is transferred to a 500-mL, single-necked round-bottomed flask using CH2Cl2, which is then evaporated (40 °C bath, 440-30 mmHg) on a rotary evaporator. The flask is equipped with a 4-cm oval Teflon-coated magnetic stir-bar, and the viscous oil stirred while being dried on the vacuum pump (0.15 mmHg, 24 °C) for 5 h to obtain a pale yellow oil 2 (14.7 g). The material is used without further purification (Notes 6 and 7).'''

ORGSYN_V95P0157_A_PARAS12_INFO = {
    'text': ORGSYN_V95P0157_A_PARAS12_TEXT,
    'name': 'orgsyn_v95p0157_a_paras12',
    'reagents': {
        'the aldehyde 1': {
            'quantities': [],
        },
        'MeOH': {
            'quantities': [],
        },
        'sodium borohydride': {
            'quantities': ['3.02 g', '79.8 mmol', '2.0 equiv'],
        },
        '25 % EtOAc': {
            'quantities': [],
        },
        'hexanes': {
            'quantities': [],
        },
        'EtOAc': {
            'quantities': ['900 mL', '3 x 150 mL', '50 mL'],
        },
        'H2O': {
            'quantities': ['50 mL', '50 mL'],
        },
        'ethyl acetate': {
            'quantities': ['50 mL'],
        },
        'saturated aqueous NH4Cl': {
            'quantities': ['100 mL'],
        },
        'saturated aqueous NaCl': {
            'quantities': ['100 mL'],
        },
        'Na2SO4': {
            'quantities': ['20 g'],
        },
        'the Na2SO4': {
            'quantities': [],
        },
        'ethyl N-(tert-butoxycarbonyl)-N-((tert-butyldimethylsilyl)oxy)-L-homoserinate': {
            'quantities': [],
        },
        'CH2Cl2': {
            'quantities': [],
        },
        'compound 2': {
            'quantities': ['14.7 g'],
        },
    },
    'steps': [
        Confirm,
        Dissolve,
        HeatChillToTemp,
        Repeat,
        Stir,
        HeatChillToTemp,
        Stir,
        Add,
        Stir,
        Add,
        Add,
        Add,
        Add,
        Separate,
        Separate,
        Separate,
        Add,
        Evaporate,
        Add,
        Evaporate,
        Dry,
    ],
    'vessels': [
        # Confirm
        {},
        # Dissolve
        {
            'vessel': 'reactor',
        },
        # HeatChillToTemp
        {
            'vessel': 'reactor',
        },
        # Repeat
        {
            'children': [
                # Add
                {
                    'vessel': 'reactor',
                },
                # Wait
                {}
            ]
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
        # Stir
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
        # Transfer
        {
            'from_vessel': 'reactor',
            'to_vessel': 'separator',
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
            'vessel': 'reactor',
        },
        # Transfer
        {
            'from_vessel': 'reactor',
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
            'to_vessel': 'separator',
        },
        # Separate
        {
            'from_vessel': 'separator',
            'separation_vessel': 'separator',
            'to_vessel': 'rotavap',
            'through': 'Na2SO4',
        },
        # Add
        {
            'vessel': 'rotavap',
            'through': 'Na2SO4',
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
        # Confirm
        {
            'msg': 'Is The aldehyde 1 in the correct vessel?',
        },
        # Dissolve
        {
            'solvent': 'MeOH',
            'volume': 200.0,
        },
        # HeatChillToTemp
        {
            'temp': -20.0,
        },
        # Repeat
        {
            'repeats': 10,
            'children': [
                # Add
                {
                    'reagent': 'sodium borohydride',
                    'mass': 0.3,
                    'stir': True,
                },
                # Wait
                {
                    'time': 3 * 60,
                }
            ]
        },
        # Stir
        {
            'time': 2700.0,
        },
        # HeatChillToTemp
        {
            'temp': 0.0,
            'active': False,
        },
        # Stir
        {
            'time': 2100.0,
        },
        # Add
        {
            'reagent': 'a mixture of ice-water ( 170 mL )',
            'volume': 170.0,
            'stir': True,
            'stir_speed': 600,
        },
        # Stir
        {
            'time': 600.0,
        },
        # Add
        {
            'reagent': 'EtOAc',
            'volume': 900.0,
            'stir': True,
        },
        # Add
        {
            'reagent': 'H2O',
            'volume': 50.0,
            'stir': True,
        },
        # Transfer
        {
            'volume': 'all'
        },
        # Add
        {
            'reagent': 'ethyl acetate',
            'volume': 50.0,
            'stir': True,
        },
        # Transfer
        {
            'volume': 50
        },
        # Add
        {
            'reagent': 'H2O',
            'volume': 50.0,
            'stir': True,
        },
        # Transfer
        {
            'volume': 50
        },
        # Separate
        {
            'purpose': 'extract',
            'product_bottom': False,
            'solvent': 'EtOAc',
            'solvent_volume': 150.0,
            'n_separations': 3,
        },
        # Separate
        {
            'purpose': 'wash',
            'product_bottom': False,
            'solvent': 'saturated aqueous NH4Cl',
            'solvent_volume': 100.0,
            'n_separations': 1,
        },
        # Separate
        {
            'purpose': 'wash',
            'product_bottom': False,
            'solvent': 'saturated aqueous NaCl',
            'solvent_volume': 100.0,
            'n_separations': 1,
        },
        # Add
        {
            'reagent': 'EtOAc',
            'volume': 50.0,
            'stir': False,
        },
        # Evaporate
        {
            'temp': 40.0,
            'pressure': 113.3237,
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
            'pressure': 313.30670000000003,
        },
        # Dry
        {
            'time': 5 * 60 * 60,
            'temp': 24,
            'vacuum_pressure': 0.2,
        }
    ],
}
