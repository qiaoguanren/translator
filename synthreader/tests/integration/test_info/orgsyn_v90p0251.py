from chemputerxdl.steps import *
from xdl.steps import *

ORGSYN_V90P0251_TEXT = '''A 500-mL, 3-necked, round-bottomed flask equipped with a septum through which is inserted a thermocouple probe, an overhead stirrer with a paddle size of 5 cm, and a 50-mL pressure-equalizing addition funnel fitted with a nitrogen inlet, is charged with anhydrous DME (80 mL) (Note 1) and SOCl2 (6.2 mL, 0.087 mol, 1.2 equiv) (Note 2) at ambient temperature. A solution of 2-aminophenethyl alcohol (10.0 g, 0.070 mol, 1.0 equiv) (Note 3) in DME (20 mL) is added dropwise to the stirred solution via the additional funnel over 1-1.5 h, maintaining the internal temperature at 20-30 °C with an external cooling bath (Note 3 and Note 4). After addition, the batch is further stirred for 6-7 h at ambient temperature (Note 5). Sodium hydroxide (2.5 N, 128 mL, 0.32 mol, 4.4 equiv), followed by water (16 mL), is added to the reaction mixture via the addition funnel over 30 min, maintaining the internal temperature at <35 °C with an ice/water cooling bath (Note 6). The reaction mixture is then warmed to 60 °C and stirred for 10 h (Note 7). The reaction mixture is cooled to ambient temperature and transferred to a 1-L separatory funnel. tert-Butyl methyl ether (MTBE, 100 mL) and water (56 mL) (Note 8) are added. The organic phase is retained and the separated aqueous phase is back extracted with MTBE (56 mL) (Note 9). The combined organic phase is washed with brine (43 mL) (Note 10), dried over sodium sulfate (Note 11 and Note 12), and concentrated by rotary evaporation to dryness under reduced pressure (35 °C bath, 60 mmHg). The resulting crude product is dissolved with ethyl acetate (ca. 90 mL) to a volume of 100 mL (Note 13).
A 500-mL, 3-necked, round-bottomed flask equipped with a septum through which is inserted a thermocouple probe, an overhead stirrer with a paddle size of 5 cm, and a 100-mL pressure-equalizing addition funnel fitted with a nitrogen inlet, is charged with oxalic acid dihydrate (9.3 g, 0.073 mol, 1.04 equiv) (Note 14) and methanol (14 mL). The resulting stirred solution is warmed to ambient temperature (Note 15). About 30 mL of the above crude product solution is added dropwise via the additional funnel at ambient temperature over 15 min. The batch is seeded with crystalline product (3 mg) (Note 16) and stirred for 30 min to form a seed bed slurry. Then, the rest of the product solution is added dropwise over 2 h. The slurry is stirred at ambient temperature for 15 h, then filtered through a 100-mL sintered glass funnel (Note 17). The wet cake is washed with 10% methanol in ethyl acetate (2 x 15 mL). Air suction drying affords the oxalic acid salt of indoline (12.0-12.1 g, 79%) as a white crystalline solid (Note 18).'''

ORGSYN_V90P0251_INFO = {
    'text': ORGSYN_V90P0251_TEXT,
    'name': 'orgsyn_v90p0251',
    'reagents': {
        'anhydrous DME': {
            'quantities': ['80 mL'],
        },
        'SOCl2': {
            'quantities': ['6.2 mL', '0.087 mol', '1.2 equiv'],
        },
        '2-aminophenethyl alcohol': {
            'quantities': ['10.0 g', '0.070 mol', '1.0 equiv'],
        },
        'DME': {
            'quantities': ['20 mL'],
        },
        'sodium hydroxide': {
            'quantities': ['2.5 N', '128 mL', '0.32 mol', '4.4 equiv'],
        },
        'water': {
            'quantities': ['16 mL', '56 mL'],
        },
        'tert-Butyl methyl ether': {
            'quantities': ['100 mL'],
        },
        'MTBE': {
            'quantities': ['56 mL'],
        },
        'brine': {
            'quantities': ['43 mL'],
        },
        'sodium sulfate': {
            'quantities': [],
        },
        'ethyl acetate': {
            'quantities': ['90 mL', '2 x 15 mL'],
        },
        'oxalic acid dihydrate': {
            'quantities': ['9.3 g', '0.073 mol', '1.04 equiv'],
        },
        'methanol': {
            'quantities': ['14 mL'],
        },
        '10 % methanol': {
            'quantities': [],
        },
        'indoline (79 %)': {
            'quantities': ['12.05  g', '79 %'],
        },
        'the oxalic acid salt': {
            'quantities': [],
        },
    },
    'steps': [
        HeatChillToTemp,
        Add,
        Add,
        Add,
        Stir,
        HeatChillToTemp,
        Add,
        Add,
        HeatChillToTemp,
        Stir,
        HeatChillToTemp,
        Add,
        Add,
        Separate,
        Separate,
        Separate,
        Evaporate,
        Dissolve,
        Add,
        Add,
        HeatChillToTemp,
        Stir,
        Stir,
        Filter,
        WashSolid,
        Dry,
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
            'to_vessel': 'rotavap',
            'through': 'sodium sulfate',
        },
        # Evaporate
        {
            'rotavap_name': 'rotavap',
        },
        # Dissolve
        {
            'vessel': 'rotavap',
        },
        # Add
        {
            'vessel': 'filter',
        },
        # Add
        {
            'vessel': 'filter',
        },
        # HeatChillToTemp
        {
            'vessel': 'filter',
        },
        # Transfer
        {
            'from_vessel': 'rotavap',
            'to_vessel': 'filter',
        },
        # Stir
        {
            'vessel': 'filter',
        },
        # Transfer
        {
            'from_vessel': 'rotavap',
            'to_vessel': 'filter',
        },
        # Stir
        {
            'vessel': 'filter',
        },
        # Filter
        {
            'filter_vessel': 'filter',
        },
        # WashSolid
        {
            'vessel': 'filter',
        },
        # Dry
        {
            'vessel': 'filter',
        },
    ],
    'properties': [
        # HeatChillToTemp
        {
            'temp': 25.0,
        },
        # Add
        {
            'reagent': 'anhydrous DME',
            'volume': 80.0,
            'stir': False,
        },
        # Add
        {
            'reagent': 'SOCl2',
            'volume': 6.2,
            'stir': True,
        },
        # Add
        {
            'reagent': '2-aminophenethyl alcohol DME solution',
            'volume': 20.0,
            'time': 4500.0,
            'stir': True,
        },
        # Stir
        {
            'time': 23400.0,
        },
        # HeatChillToTemp
        {
            'temp': 32.0,
        },
        # Add
        {
            'reagent': 'sodium hydroxide',
            'volume': 128.0,
            'time': 1800.0,
            'stir': True,
        },
        # Add
        {
            'reagent': 'water',
            'volume': 16.0,
            'time': 1800.0,
            'stir': True,
        },
        # HeatChillToTemp
        {
            'temp': 60.0,
        },
        # Stir
        {
            'time': 36000.0,
        },
        # HeatChillToTemp
        {
            'temp': 25,
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Add
        {
            'reagent': 'tert-Butyl methyl ether',
            'volume': 100.0,
            'stir': True,
        },
        # Add
        {
            'reagent': 'water',
            'volume': 56.0,
            'stir': True,
        },
        # Separate
        {
            'purpose': 'extract',
            'product_bottom': False,
            'solvent': '',
            'n_separations': 1,
        },
        # Separate
        {
            'purpose': 'extract',
            'product_bottom': False,
            'solvent': 'MTBE',
            'solvent_volume': 56.0,
            'n_separations': 1,
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Separate
        {
            'purpose': 'wash',
            'product_bottom': False,
            'solvent': 'brine',
            'solvent_volume': 43.0,
            'n_separations': 1,
        },
        # Evaporate
        {
            'temp': 35.0,
            'pressure': 79.9932,
        },
        # Dissolve
        {
            'solvent': 'ethyl acetate',
            'volume': 90.0,
        },
        # Add
        {
            'reagent': 'oxalic acid dihydrate',
            'mass': 9.3,
            'stir': True,
        },
        # Add
        {
            'reagent': 'methanol',
            'volume': 14.0,
            'stir': True,
        },
        # HeatChillToTemp
        {
            'temp': 25,
        },
        # Transfer
        {
            'volume': 30,
            'time': 15 * 60,
        },
        # Stir
        {
            'time': 1800.0,
        },
        # Transfer
        {
            'volume': 'all',
            'time': 2 * 60 * 60,
        },
        # Stir
        {
            'time': 54000.0,
        },
        # Filter
        {},
        # WashSolid
        {
            'solvent': '10 % methanol ethyl acetate solution',
            'volume': 15.0,
            'repeat': 2,
        },
        # Dry
        {},
    ],
}
