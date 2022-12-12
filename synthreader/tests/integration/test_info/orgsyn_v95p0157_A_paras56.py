from chemputerxdl.steps import *
from xdl.steps import *

ORGSYN_V95P0157_A_PARAS56_TEXT = '''The resulting dark-orange oil, containing ethyl N-(tert-butoxycarbonyl)-N-((tert-butyldimethylsilyl)oxy)-O-(methylsulfonyl)-L-homoserinate (i.e., 3) is transferred to a 1-L round-bottomed flask, which is then evaporated (40 °C bath, 440-30 mmHg) on a rotary evaporator.

The compound 3 (17.7 g, 38.8 mmol, 1.0 equiv) is diluted with THF (750 mL) and transferred, using a long-stemmed plastic funnel, into a 1-L, three-necked, round-bottomed flask equipped with a 4-cm Teflon-coated magnetic stir-bar, a 125-mL addition funnel, a thermometer fitted with a glass adaptor, and a rubber septum through which an active nitrogen atmosphere is ensured. THF (15 mL) is used to rinse the flask and the remaining solution transferred into the reaction flask using a 10-mL pipette. The flask is cooled down to 4 ºC using an ice-water bath (Figure 3). The addition funnel is charged with tetrabutylammonium fluoride (1 M in THF, 58.0 mL, 58.0 mmol, 1.50 equiv, via a 100-mL graduated cylinder), which is then added to the reaction flask dropwise over 90 min, maintaining the internal temperature to 3-4 ºC. Tetrahydrofuran (10 mL) is used to ensure that no reagents are left on the side of the addition funnel (final concentration of substrate 0.05 M). The addition funnel and the thermometer are removed and the flask is equipped with a glass stopper and a rubber septum.

The reaction mixture is stirred for 1 h at 4 ºC. The reaction is monitored by TLC in 40% EtOAc in hexanes using ninhydrin to stain (Notes 10 and 11). Upon completion of the reaction (as noted by disappearance of starting material (Notes 10 and 11), saturated aqueous NaHCO3 (120 mL) is added to the reaction and stirred for 10 min. The resultant biphasic mixture is diluted with Et2O (300 mL) and the mixture poured into a 2-L separatory funnel. The aqueous layer is separated and washed with Et2O (3 x 150 mL). The combined organic layers are washed sequentially with saturated aqueous NaHCO3 (150 mL) and saturated aqueous NaCl (150 mL). The organic layer is dried over Na2SO4 (30 g) and filtered by suction using a fritted funnel (9 cm diameter, medium porosity). Diethyl ether (200 mL) is used to wash the Na2SO4 and the filtrate is concentrated by rotary evaporation (40 °C bath, 500-30 mmHg). The resulting brown oil, containing (S)-2-tert-butyl 3-ethyl isoxazolidine-2,3-dicarboxylate (i.e., 4) is transferred to a pre-weighed 250-mL round-bottomed flask using CH2Cl2, which is then evaporated (40 °C bath, 400-30 mmHg). The flask is equipped with a pre-weighed 4-cm oval Teflon-coated magnetic stirbar and dried while stirring on the vacuum pump (0.15 mmHg, 24 °C) for 10 h to provide a yellow oil (10.3 g). Column chromatography with 20% EtOAc in hexanes (Note 12) furnished 4 (6.35 g, 97.0 % purity, 64.9% based on compound 1) as a clear yellow oil (Notes 13, 14, and 15).'''

ORGSYN_V95P0157_A_PARAS56_INFO = {
    'text': ORGSYN_V95P0157_A_PARAS56_TEXT,
    'name': 'orgsyn_v95p0157_a_paras56',
    'reagents': {
        'ethyl N-(tert-butoxycarbonyl)-N-((tert-butyldimethylsilyl)oxy)-O-(methylsulfonyl)-L-homoserinate': {
            'quantities': [],
        },
        'compound 3': {
            'quantities': ['17.7 g', '38.8 mmol', '1.0 equiv'],
        },
        'THF': {
            'quantities': ['750 mL', '15 mL'],
        },
        'pipette': {
            'quantities': ['10 mL'],
        },
        'tetrabutylammonium fluoride': {
            'quantities': [],
        },
        'tetrahydrofuran': {
            'quantities': ['10 mL'],
        },
        'the side': {
            'quantities': [],
        },
        '40 % EtOAc': {
            'quantities': [],
        },
        'hexanes': {
            'quantities': [],
        },
        'ninhydrin': {
            'quantities': [],
        },
        'saturated aqueous NaHCO3': {
            'quantities': ['120 mL', '150 mL'],
        },
        'the resultant': {
            'quantities': [],
        },
        'Et2O': {
            'quantities': ['300 mL', '3 x 150 mL'],
        },
        'saturated aqueous NaCl': {
            'quantities': ['150 mL'],
        },
        'Na2SO4': {
            'quantities': ['30 g'],
        },
        'diethyl ether': {
            'quantities': ['200 mL'],
        },
        'the Na2SO4': {
            'quantities': [],
        },
        'CH2Cl2': {
            'quantities': [],
        },
        '20 % EtOAc': {
            'quantities': [],
        },
    },
    'steps': [
        Evaporate,
        Add,
        Add,
        Add,
        HeatChillToTemp,
        Add,
        Add,
        Stir,
        Add,
        Stir,
        Add,
        Separate,
        Separate,
        Separate,
        Separate,
        Add,
        Evaporate,
        Add,
        Evaporate,
        Dry,
        RunColumn,
    ],
    'vessels': [
        # Evaporate
        {
            'rotavap_name': 'rotavap',
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
        # Separate
        {
            'from_vessel': 'reactor',
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
        # RunColumn
        {
            'from_vessel': 'rotavap',
            'to_vessel': 'reactor',
        },
    ],
    'properties': [
        # Evaporate
        {
            'temp': 40.0,
            'pressure': 313.30670000000003,
            'time': 1800,
            'mode': 'auto',
        },
        # Add
        {
            'reagent': 'compound 3',
            'mass': 17.7,
            'stir': False,
        },
        # Add
        {
            'reagent': 'THF',
            'volume': 750.0,
            'stir': False,
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Add
        {
            'reagent': 'THF',
            'volume': 15.0,
            'stir': True,
        },
        # Transfer
        {
            'volume': 15,
        },
        # HeatChillToTemp
        {
            'temp': 4.0,
        },
        # Add
        {
            'reagent': 'tetrabutylammonium fluoride',
            'volume': 58.0,
            'time': 5400.0,
            'stir': True,
        },
        # Add
        {
            'reagent': 'tetrahydrofuran',
            'volume': 10.0,
            'stir': True,
        },
        # Stir
        {
            'time': 3600.0,
        },
        # Add
        {
            'reagent': 'saturated aqueous NaHCO3',
            'volume': 120.0,
            'stir': True,
        },
        # Stir
        {
            'time': 600.0,
        },
        # Add
        {
            'reagent': 'Et2O',
            'volume': 300.0,
            'stir': True,
        },
        # Separate
        {
            'purpose': 'extract',
            'product_bottom': False,
            'solvent': '',
            'n_separations': 1,
            'waste_phase_to_vessel': 'separator',
        },
        # Separate
        {
            'purpose': 'extract',
            'product_bottom': False,
            'solvent': 'Et2O',
            'solvent_volume': 150.0,
            'n_separations': 3,
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Separate
        {
            'purpose': 'wash',
            'product_bottom': False,
            'solvent': 'saturated aqueous NaHCO3',
            'solvent_volume': 150.0,
            'n_separations': 1,
        },
        # Separate
        {
            'purpose': 'wash',
            'product_bottom': False,
            'solvent': 'saturated aqueous NaCl',
            'solvent_volume': 150.0,
            'n_separations': 1,
        },
        # Add
        {
            'reagent': 'diethyl ether',
            'volume': 200.0,
            'stir': False,
        },
        # Evaporate
        {
            'temp': 40.0,
            'pressure': 353.30330000000004,
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
            'pressure': 286.64230000000003,
            'time': 1800,
            'mode': 'auto',
        },
        # Dry
        {
            'time': 36000.0,
            'temp': 24.0,
            'vacuum_pressure': 0.199983,
        },
        # RunColumn
        {},
    ],
}
