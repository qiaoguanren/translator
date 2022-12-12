from chemputerxdl.steps import *
from xdl.steps import *

ORGSYN_V95P0029_TEXT = '''Iridium (III) chloride anhydrous (0.65 g , 2.18 mmol, 1 equiv) (Note 2), 2-phenylpyridine (3.74 mL, 26.1 mmol, 12.0 equiv) (Note 3), and 0.65 L of DI water (0.003 M with respect to IrCl3) is added to a 1 L Parr reactor (Figure 1) (Notes 4, 5, and 6). The reaction mixture is pressurized with argon (10.0 psi), stirred and then depressurized three times, and finally charged again with argon before sealing (Note 7). The reaction mixture is heated to 205 °C for 48 h. Then the reactor is cooled to 20 ⁰C with internal cooling coils. At the end of the experiment the reactor was left in the stand and the contents cooled to 20 °C using cold water. After cooling, the reactor is opened revealing an insoluble yellow solid on the surfaces (Figure 2) and dispersed in the aqueous phase (Note 8). All contents are transferred slowly to a 6 L separatory funnel aided by a large 5 cm glass funnel. Then the interior of the reactor is mechanically scraped (to extract the yellow material), with metal tongs, cotton balls (25 in total), and 500 mL of dichloromethane (DCM) from a spray bottle, and again all contents are added to the separatory funnel (Notes 9 and 10).

While still in the funnel, the cotton is rinsed with 25 mL of DCM from a spray bottle and evenly pressed with tongs to release the yellow material from the cotton (Note 9). After removing the cotton, the solution is then diluted with 2.5 L of DCM. The separatory funnel is shaken vigorously, allowed to settle and again shaken, and the organic layer is then slowly separated from the aqueous layer (Notes 11, 12 and 13) and the aqueous layer is further extracted with more DCM (3 x 10 mL), and the organic layers are combined (Note 14). The aqueous layers are kept for future ligand recovery. The combined organic layer is washed with a 1 M HCl solution, with vigorous mixing prior to separation (3 x 900 mL). Each HCl wash is then back extracted with DCM (3 x 10 mL) to insure complete recovery of the product. After the final wash, the organic layer is filtered slowly (20 min) through a Celite (35 g) pad on top of a 150 mL medium porosity sintered glass funnel, into a 3 L round-bottomed flask, and then dried with 30 g of MgSO4. After filtering the drying reagent using a 4 L Erlenmyer flask fitted with a 5 cm funnel/cotton plug, a homogenous aliquot is removed for NMR analysis (Note 15). Finally, the solvent is removed in batches by transferring to a 2.5 L round-bottomed flask by rotary evaporation (35 °C, 30 mm Hg, 150 rpm) to afford 1.35 g (94%) of Ir(ppy)3 as a bright yellow solid (Note 16).
Further purification of Ir(ppy)3 can be performed by adding the yellow solid to a 1 L round-bottomed flask and adding 600 mL of distilled hexanes. The solid material is then sonicated until a uniform slurry is achieved, and 5 mL of dichloromethane is added (Note 17). The liquid is swirled giving a slight yellow tint to the solution indicating successful dissolution of a colored compound, and selective extraction of the impurities. Then the slurry is slowly poured through a 50 mL fine porosity sintered glass funnel to collect the yellow solid, and the filtrate is collected into a 1 L Erlenmeyer flask. The yellow solid is air dried on the filter to afford 1.29 g (91%) (Notes 18 and 19) of the product in >97% purity (Notes 20 and 21). '''

ORGSYN_V95P0029_INFO = {
    'text': ORGSYN_V95P0029_TEXT,
    'name': 'orgsyn_v95p0029',
    'reagents': {
        'iridium(III)chloride anhydrous': {
            'quantities': ['0.65 g', '2.18 mmol', '1 equiv'],
        },
        '2-phenylpyridine': {
            'quantities': ['3.74 mL', '26.1 mmol', '12.0 equiv'],
        },
        'DI water': {
            'quantities': ['0.65 L'],
        },
        'water': {
            'quantities': [],
        },
        'dichloromethane(DCM)': {
            'quantities': ['500 mL'],
        },
        'DCM': {
            'quantities': ['25 mL', '2.5 L', '3 x 10 mL', '3 x 10 mL'],
        },
        '1 M HCl solution': {
            'quantities': [],
        },
        'HCl': {
            'quantities': [],
        },
        'MgSO4': {
            'quantities': ['30 g'],
        },
        'Ir(ppy)3 (94 %)': {
            'quantities': ['1.35 g', '94 %'],
        },
        'Ir(ppy)3': {
            'quantities': [],
        },
        'distilled hexanes': {
            'quantities': ['600 mL'],
        },
        'dichloromethane': {
            'quantities': ['5 mL'],
        },
    },
    'steps': [
        Add,
        Add,
        Add,
        HeatChill,
        HeatChillToTemp,
        Add,
        Add,
        Separate,
        Separate,
        Separate,
        Separate,
        FilterThrough,
        Filter,
        Evaporate,
        Add,
        Sonicate,
        Add,
        Stir,
        Filter,
        Dry,
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
            'to_vessel': 'separator',
        },
        # Add
        {
            'vessel': 'separator',
        },
        # Add
        {
            'vessel': 'separator',
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
            'to_vessel': 'separator',
            'separation_vessel': 'separator',
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
            'waste_phase_to_vessel': 'separator',
        },
        # Separate
        {
            'from_vessel': 'separator',
            'separation_vessel': 'separator',
            'to_vessel': 'filter',
        },
        # FilterThrough
        {
            'from_vessel': 'filter',
            'to_vessel': 'filter',
            'through': 'MgSO4',
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
        # Add
        {
            'vessel': 'rotavap',
        },
        # Sonicate
        {},
        # Add
        {
            'vessel': 'rotavap',
        },
        # Stir
        {
            'vessel': 'rotavap',
        },
        # Transfer
        {
            'from_vessel': 'rotavap',
            'to_vessel': 'filter',
        },
        # Filter
        {},
        # Dry
        {
            'vessel': 'filter',
        },
    ],
    'properties': [
        # Add
        {
            'reagent': 'iridium(III)chloride anhydrous',
            'mass': 0.65,
            'stir': False,
        },
        # Add
        {
            'reagent': '2-phenylpyridine',
            'volume': 3.74,
            'stir': False,
        },
        # Add
        {
            'reagent': 'DI water',
            'volume': 650.0,
            'stir': True,
        },
        # HeatChill
        {
            'temp': 205.0,
            'time': 172800.0,
        },
        # HeatChillToTemp
        {
            'temp': 20.0,
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Add
        {
            'reagent': 'DCM',
            'volume': 25.0,
            'stir': True,
        },
        # Add
        {
            'reagent': 'DCM',
            'volume': 2500.0,
            'stir': True,
        },
        # Separate
        {
            'purpose': 'extract',
            'product_bottom': True,
            'n_separations': 1,
        },
        # Separate
        {
            'purpose': 'extract',
            'product_bottom': True,
            'solvent': 'DCM',
            'solvent_volume': 10.0,
            'n_separations': 3,
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Separate
        {
            'purpose': 'wash',
            'product_bottom': True,
            'solvent': '1 M HCl solution',
            'solvent_volume': 900.0,
            'n_separations': 3,
            'through': 'celite',
        },
        # Separate
        {
            'purpose': 'extract',
            'product_bottom': True,
            'solvent': 'DCM',
            'solvent_volume': 10.0,
            'n_separations': 3,
            'through': 'celite',
        },
        # FilterThrough
        {},
        # Filter
        {
            'filter_vessel': 'filter',
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Evaporate
        {
            'temp': 35.0,
            'pressure': 39.9966,
        },
        # Add
        {
            'reagent': 'distilled hexanes',
            'volume': 600.0,
            'stir': False,
        },
        # Sonicate
        {},
        # Add
        {
            'reagent': 'dichloromethane',
            'volume': 5.0,
            'stir': True,
        },
        # Stir
        {
            'time': 300.0,
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Filter
        {
            'filter_vessel': 'filter',
        },
        # Dry
        {},
    ],
}
