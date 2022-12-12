from chemputerxdl.steps import *
from xdl.steps import *

ORGSYN_V95P0157_A_PARAS34_TEXT = '''The resulting pale yellow oil is then evaporated (40 °C bath, 440-30 mmHg) on a rotary evaporator.

The oil 2 (14.7 g, 38.9 mmol, 1.0 equiv) is diluted with CH2Cl2 (175 mL) and transferred, using a long-stemmed plastic funnel, into a 500-mL, three-necked, round-bottomed flask equipped with a 4-cm Teflon-coated magnetic stir-bar, a 125-mL addition funnel, a thermometer fitted with a glass adaptor, and a rubber septum through which an active nitrogen atmosphere is ensured (Figure 2). The flask from which 2 is transferred is washed with CH2Cl2 (10 mL) to ensure that no product is left.

The receiving flask is cooled to 4 ºC using an ice-water bath. The addition funnel is charged with Et3N (16.6 mL, 119 mmol, 3.0 equiv, via 20-mL disposable syringe), which is then added dropwise over 15 min maintaining the internal temperature to 3-4 ºC. The addition funnel is washed with CH2Cl2 (5 mL) to ensure that no reagents are left. The same addition funnel is next charged with methanesulfonyl chloride (7.40 mL, 95.6 mmol, 2.40 equiv, via 10-mL disposable syringe) which is then added dropwise over approximately 20 min. The internal temperature is maintained at 4 ºC through the entire course of the addition. The addition funnel is washed using CH2Cl2 (5 mL) to ensure that no reagents are left (final concentration of substrate is 0.2 M). The addition funnel is removed and the flask is equipped with a glass stopper. The reaction mixture is stirred for 15 min at 4 ºC after which the ice-water bath is removed and the reaction is stirred at 24 ºC for 1 h. The reaction is monitored by TLC in 40% EtOAc in hexanes using ninhydrin stain (Note 8). After stirring for 1 h at 24 ºC, TLC analysis shows disappearance of starting material. To the completed reaction, saturated aqueous NH4Cl (150 mL) is added and the mixture is poured into a 2-L separatory funnel. The flask is washed with CH2Cl2 (10 mL) to ensure that no reagents are left. The aqueous layer is separated and extracted with CH2Cl2 (4 x 150 mL). The combined organic layers are washed sequentially with saturated aqueous NH4Cl (200 mL), saturated aqueous NaHCO3 (200 mL) and saturated aqueous NaCl (200 mL). The organic layer is dried over Na2SO4 (20 g) and filtered by suction using a fritted funnel (9 cm diameter, medium porosity). Dichloromethane (25 mL) is used to wash the Na2SO4 and the filtrate is concentrated by rotary evaporation into a 2-L round-bottomed flask (40 °C bath, 440-30 mmHg). The resulting dark-orange oil, containing ethyl N-(tert-butoxycarbonyl)-N-((tert-butyldimethylsilyl)oxy)-O-(methylsulfonyl)-L-homoserinate (i.e., 3) is transferred to a 1-L round-bottomed flask using CH2Cl2, which is then evaporated (40 °C bath, 440-30 mmHg) on a rotary evaporator. The residue is transferred to a pre-weighed 250-mL single-necked round-bottomed flask equipped with pre-weighed 4-cm oval Teflon-coated magnetic stir-bar, and dried while stirring on the vacuum pump (0.15 mmHg, 24 °C) for 6 h to afford a dark-orange oil 3 that is used in the next step with no further purification (17.7 g) (Note 9).'''

ORGSYN_V95P0157_A_PARAS34_INFO = {
    'text': ORGSYN_V95P0157_A_PARAS34_TEXT,
    'name': 'orgsyn_v95p0157_a_paras34',
    'reagents': {
        'compound 2': {
            'quantities': ['14.7 g', '14.7 g', '38.9 mmol', '1.0 equiv'],
        },
        'CH2Cl2': {
            'quantities': ['175 mL', '10 mL', '5 mL', '5 mL', '10 mL', '4 x 150 mL'],
        },
        'Et3N': {
            'quantities': [],
        },
        'methanesulfonyl chloride': {
            'quantities': [],
        },
        '40 % EtOAc': {
            'quantities': [],
        },
        'hexanes': {
            'quantities': [],
        },
        'saturated aqueous NH4Cl': {
            'quantities': ['150 mL', '200 mL'],
        },
        'saturated aqueous NaHCO3': {
            'quantities': ['200 mL'],
        },
        'saturated aqueous NaCl': {
            'quantities': ['200 mL'],
        },
        'Na2SO4': {
            'quantities': ['20 g'],
        },
        'dichloromethane': {
            'quantities': ['25 mL'],
        },
        'the Na2SO4': {
            'quantities': [],
        },
        'ethyl N-(tert-butoxycarbonyl)-N-((tert-butyldimethylsilyl)oxy)-O-(methylsulfonyl)-L-homoserinate': {
            'quantities': [],
        },
    },
    'steps': [
        Evaporate, # paras12, just there for  context
        Add,
        Add,
        Add,
        HeatChillToTemp,
        Add,
        Add,
        Add,
        Add,
        Stir,
        HeatChill,
        Add,
        Add,
        Separate,
        Separate,
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
        # Evaporate (paras12), just there for context
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
        # Transfer
        {
            'from_vessel': 'rotavap',
            'to_vessel': 'reactor',
        },
        # Add
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
        # Stir
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
            'to_vessel': 'buffer_flask1',
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
        }
    ],
    'properties': [
        # Evaporate (paras12), just there for context
        {
            'temp': 40.0,
            'pressure': 313.30670000000003,
        },
        # Add
        {
            'reagent': 'compound 2',
            'mass': 14.7,
            'stir': False,
        },
        # Add
        {
            'reagent': 'CH2Cl2',
            'volume': 175.0,
            'stir': False,
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Add
        {
            'reagent': 'CH2Cl2',
            'volume': 10.0,
            'stir': False,
        },
        # Transfer
        {
            'volume': 10,
        },
        # HeatChillToTemp
        {
            'temp': 4.0,
        },
        # Add
        {
            'reagent': 'Et3N',
            'volume': 16.6,
            'time': 900.0,
            'stir': True,
        },
        # Add
        {
            'reagent': 'CH2Cl2',
            'volume': 5.0,
            'stir': True,
        },
        # Add
        {
            'reagent': 'methanesulfonyl chloride',
            'volume': 7.4,
            'time': 1200.0,
            'stir': True,
        },
        # Add
        {
            'reagent': 'CH2Cl2',
            'volume': 5.0,
            'stir': True,
        },
        # Stir
        {
            'time': 900.0,
        },
        # HeatChill
        {
            'temp': 24.0,
            'time': 3600.0,
        },
        # Add
        {
            'reagent': 'saturated aqueous NH4Cl',
            'volume': 150.0,
            'stir': True,
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Add
        {
            'reagent': 'CH2Cl2',
            'volume': 10.0,
            'stir': True,
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Separate
        {
            'purpose': 'extract',
            'product_bottom': True,
            'solvent': '',
            'n_separations': 1,
            'waste_phase_to_vessel': 'separator',
        },
        # Separate
        {
            'purpose': 'extract',
            'product_bottom': True,
            'solvent': 'CH2Cl2',
            'solvent_volume': 150.0,
            'n_separations': 4,
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Separate
        {
            'purpose': 'wash',
            'product_bottom': True,
            'solvent': 'saturated aqueous NH4Cl',
            'solvent_volume': 200.0,
            'n_separations': 1,
        },
        # Separate
        {
            'purpose': 'wash',
            'product_bottom': True,
            'solvent': 'saturated aqueous NaHCO3',
            'solvent_volume': 200.0,
            'n_separations': 1,
        },
        # Separate
        {
            'purpose': 'wash',
            'product_bottom': True,
            'solvent': 'saturated aqueous NaCl',
            'solvent_volume': 200.0,
            'n_separations': 1,
        },
        # Add
        {
            'reagent': 'dichloromethane',
            'volume': 25.0,
            'stir': False,
        },
        # Evaporate
        {
            'temp': 40.0,
            'pressure': 313.30670000000003,
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
            'temp': 24,
            'time': 6 * 60 * 60,
            'vacuum_pressure': 0.2,
        }
    ],
}
