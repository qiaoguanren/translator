from chemputerxdl.steps import *
from xdl.steps import *

ORGSYN_CV9P0004_A_TEXT = '''(2R,3S)- and (2S,3S)-1,4-Dioxa-2,3-dimethyl-2-(1-methylethenyl)-8-carboethoxy-8-azaspiro[4.5]decane. An oven-dried, 500-mL, three-necked, round-bottomed flask is fitted with a mechanical stirrer, 100-mL addition funnel, and rubber septum, and then is charged with 100 mL of dry tetrahydrofuran (Note 1) and 7.7 mL (10.5 g, 86.7 mmol) of 2-bromopropene (Note 2). The solution is cooled to −70°C with mechanical stirring and a 1.9 M pentane solution of tert-butyllithium (92 mL, 175 mmol) is added by syringe over 20 min. The resulting yellow solution is stirred for an additional 10 min at −70°C and at this time a solution of 17.6 g (54.0 mmol) of 3-(S)-[(tert-butyldiphenylsilyl)oxy]-2-butanone2 and 50 mL of dry tetrahydrofuran is added by dropping funnel over 20 min. The resulting solution is stirred for an additional 30 min at −70°C and at this time a 1.0 M tetrahydrofuran solution of tetrabutylammonium fluoride (163 mL, 163 mmol) is added in one portion and the resulting mixture is warmed to 23°C and stirred for 1 hr. At this time the contents of the flask are poured into 200 mL of saturated aqueous ammonium chloride (NH4Cl) and the resulting mixture is concentrated to remove tetrahydrofuran. The resulting aqueous suspension is diluted with 200 mL of brine and extracted twice with 200 mL of ethyl acetate (Note 3). The combined organic extracts are washed with five 100-mL portions of brine, dried over sodium sulfate, filtered, and then concentrated under reduced pressure using a rotary evaporator. The residue is subjected to short path vacuum distillation (150–160°C, 3 mm) to remove the less volatile tert-butyldiphenylsilyl by-product. The distillate contains ca. 10 g of a colorless oil that is comprised of the 2,3-dimethyl-1-pentene-3,4-diols as a 6:1 mixture of diastereomers and up to 30% of tributylamine (Note 4) and (Note 5).
1-Carbethoxy-4-piperidone (7.52 g, 43.9 mmol) (Note 6) and p-toluenesulfonic acid (5.0 g, 26 mmol) are added to a 250-mL, round-bottomed flask that contains the above distillate and a magnetic stir bar. The mixture is stirred under vacuum (20 mm) at 100°C for 90 min and the evolved water vapor is collected in a vacuum trap. The mixture is cooled to 23°C and subjected to flash chromatography on silica gel (250 g, 20 cm × 10 cm) using ethyl acetate:hexane (1:4) as the eluant (Note 7) to give 9.0 g (59% overall) of (2R,3S)- and (2S,3S)-1,4-dioxa-2,3-dimethyl-2-(1-methylethenyl)-8-carboethoxy-8-azaspiro[4.5]decane, a 6:1 mixture of diastereomers, as a pale yellow oil (Note 8).'''

ORGSYN_CV9P0004_A_INFO = {
    'text': ORGSYN_CV9P0004_A_TEXT,
    'name': 'orgsyn_cv9p0004_a',
    'reagents': {
        '(2S,3S)-1,4-dioxa-2,3-dimethyl-2-(1 methylethenyl)-8-carboethoxy-8-azaspiro': {
            'quantities': [],
        },
        'decane': {
            'quantities': [],
        },
        'dry tetrahydrofuran': {
            'quantities': ['100 mL', '50 mL'],
        },
        '2-bromopropene': {
            'quantities': ['7.7 mL', '10.5 g', '86.7 mmol'],
        },
        'tert-butyllithium': {
            'quantities': ['92 mL', '175 mmol'],
        },
        '1.9 M pentane solution': {
            'quantities': [],
        },
        '3-(S)- [(tert-butyldiphenylsilyl)oxy ] -2-butanone2': {
            'quantities': ['17.6 g', '54.0 mmol'],
        },
        'tetrabutylammonium fluoride': {
            'quantities': ['163 mL', '163 mmol'],
        },
        '1.0 M tetrahydrofuran solution': {
            'quantities': [],
        },
        'saturated aqueous ammonium chloride(NH4Cl)': {
            'quantities': ['200 mL'],
        },
        'tetrahydrofuran': {
            'quantities': [],
        },
        'brine': {
            'quantities': ['200 mL', '100 mL'],
        },
        'ethyl acetate': {
            'quantities': ['200 mL'],
        },
        'sodium sulfate': {
            'quantities': [],
        },
        'the less volatile tert-butyldiphenylsilyl by-product': {
            'quantities': [],
        },
        'the 2,3-dimethyl-1-pentene-3,4-diols': {
            'quantities': [],
        },
        'tributylamine': {
            'quantities': [],
        },
        '1-Carbethoxy-4-piperidone': {
            'quantities': ['7.52 g', '43.9 mmol'],
        },
        'p-toluenesulfonic acid': {
            'quantities': ['5.0 g', '26 mmol'],
        },
        'water': {
            'quantities': [],
        },
        'silica gel': {
            'quantities': [],
        },
        'hexane': {
            'quantities': [],
        },
    },
    'steps': [
        Add,
        Add,
        HeatChillToTemp,
        Add,
        Stir,
        Add,
        Stir,
        Add,
        HeatChillToTemp,
        Stir,
        Add,
        Evaporate,
        Add,
        Separate,
        Separate,
        Evaporate,
        Distill,
        Add,
        Add,
        HeatChill,
        HeatChillToTemp,
        RunColumn,
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
            'vessel': 'rotavap',
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
        # Add
        {
            'vessel': 'rotavap',
        },
        # Separate
        {
            'from_vessel': 'rotavap',
            'separation_vessel': 'separator',
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
        # Distill
        {},
        # Transfer
        {
            'from_vessel': 'rotavap',
            'to_vessel': 'reactor',
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
        # RunColumn
        {
            'from_vessel': 'reactor',
            'to_vessel': 'reactor',
            'column': 'column',
        },
    ],
    'properties': [
        # Add
        {
            'reagent': 'dry tetrahydrofuran',
            'volume': 100.0,
            'stir': False,
        },
        # Add
        {
            'reagent': '2-bromopropene',
            'volume': 7.7,
            'stir': True,
        },
        # HeatChillToTemp
        {
            'temp': -70.0,
        },
        # Add
        {
            'reagent': 'tert-butyllithium 1.9 M pentane solution solution',
            'volume': 92.0,
            'time': 1200.0,
            'stir': True,
        },
        # Stir
        {
            'time': 600.0,
        },
        # Add
        {
            'reagent': '3-(S)- [(tert-butyldiphenylsilyl)oxy ] -2-butanone2 dry tetrahydrofuran solution',
            'volume': 50.0,
            'time': 1200.0,
            'stir': True,
        },
        # Stir
        {
            'time': 1800.0,
        },
        # Add
        {
            'reagent': 'tetrabutylammonium fluoride 1.0 M tetrahydrofuran solution solution',
            'volume': 163.0,
            'stir': True,
        },
        # HeatChillToTemp
        {
            'temp': 23.0,
        },
        # Stir
        {
            'time': 3600.0,
        },
        # Add
        {
            'reagent': 'saturated aqueous ammonium chloride(NH4Cl)',
            'volume': 200.0,
            'stir': False,
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Evaporate
        {
            'temp': 50,
            'pressure': 541.5,
            'time': 1800,
            'mode': 'auto',
        },
        # Add
        {
            'reagent': 'brine',
            'volume': 200.0,
            'stir': False,
        },
        # Separate
        {
            'purpose': 'extract',
            'product_bottom': True,
            'solvent': 'ethyl acetate',
            'solvent_volume': 200.0,
            'n_separations': 2,
        },
        # Separate
        {
            'purpose': 'wash',
            'product_bottom': False,
            'solvent': 'brine',
            'solvent_volume': 100.0,
            'n_separations': 5,
        },
        # Evaporate
        {
            'time': 1800,
            'mode': 'auto',
        },
        # Distill
        {},
        # Transfer
        {
            'volume': 'all',
        },
        # Add
        {
            'reagent': '1-Carbethoxy-4-piperidone',
            'mass': 7.52,
            'stir': False,
        },
        # Add
        {
            'reagent': 'p-toluenesulfonic acid',
            'mass': 5.0,
            'stir': False,
        },
        # HeatChill
        {
            'temp': 100.0,
            'time': 5400.0,
        },
        # HeatChillToTemp
        {
            'temp': 23.0,
        },
        # RunColumn
        {},
    ],
}
