from chemputerxdl.steps import *
from xdl.steps import *

ALKYL_FLUOR_STEPS_1_3_SCALED_TEXT = '''In air, to a solution of 2,6-diisopropylaniline (10 mL, 53.0 mmol, 2.00 equiv) and HOAc (0.2 mL, 3.5 mmol, 0.066 equiv) in 15 mL of MeOH at 50°C in a flask was added a solution of glyoxal (3.0 mL, 26.5 mmol, 1.0 equiv) in 15 mL of MeOH. The reaction mixture was stirred at 50°C for 15 min and then stirred at 23°C for 10 h. The reaction mixture was filtered. The filter cake was washed with MeOH (3 x 15 mL) and dried in vacuo at 75 mbar to afford 8.9 g of compound S1 as a yellow solid (90% yield).

In air, to N,N'-1,4-bis(2,6-diisopropylphenyl)-1,4-diaza-butadiene (S1) (8.9 g, 23.9 mmol, 1.00 equiv) and paraformaldehyde (750 mg, 24.6 mmol, 1.03 equiv) was added 50 mL of EtOAc at 70°C. A solution of TMSCl (3.3 mL, 24.6 mmol, 1.03 equiv) in 15 mL of EtOAc was then added at 70°C, dropwise, over 45 min, with vigorous stirring.  The reaction mixture was stirred at 70°C for 2 h. After cooling to 10°C with stirring, the reaction mixture was filtered.  The filter cake was washed with EtOAc (3 x 25 mL) and dried in vacuo at 75 mbar for 2 hours to afford 8.7 g of compound S2 as a colorless solid (86% yield).

To N,N'-1,3-bis(2,6-diisopropylphenyl)imidazolium chloride(S2) (8.7 g, 21.7 mmol, 1.00 equiv) was added 10 mL of THF and a solution of KOtBu (2.92 g, 26.0 mmol, 1.20 equiv) in 26 mL of THF at 23°C. The reaction mixture was stirred at 23°C for 4 h. The reaction mixture was cooled to -35°C and 2M 1,1,1,2,2,2-hexachloroethane solution (13 mL, 26.0 mmol, 1.20 equiv) was added. The reaction mixture was warmed to 23°C and stirred at this temperature for 24 h. The reaction mixture was cooled to -35°C  and filtered. The filter cake was washed with THF (3 x 10 mL) at -20°C and washed with toluene (6 x 10 mL) at 23°C. It was then dissolved in CH2Cl2 (50 mL) at room temperature and filtered through a pad of Celite (10 g) eluting with CH2Cl2 (3 x 15 mL). The filtrate was concentrated under reduced pressure to afford 5.0 g of compound S3 as a colorless solid (81% yield).
'''

ALKYL_FLUOR_STEPS_1_3_SCALED_INFO = {
    'name': 'alkyl_fluor_steps_1_3_scaled',
    'text': ALKYL_FLUOR_STEPS_1_3_SCALED_TEXT,
    'reagents': {
        # Step 1
        '2,6-diisopropylaniline': {
            'quantities': ['10 mL', '53.0 mmol', '2.00 equiv'],
        },
        'HOAc': {
            'quantities': ['0.2 mL', '3.5 mmol', '0.066 equiv'],
        },
        'MeOH': {
            'quantities': ['15 mL', '15 mL', '3 x 15 mL']
        },
        'glyoxal': {
            'quantities': ['3.0 mL'],
        },

        # Step 2
        "N,N'-1,4-bis(2,6-diisopropylphenyl)-1,4-diaza-butadiene(S1)": {
            'quantities': ['8.9 g', '23.9 mmol', '1.00 equiv'],
        },
        'paraformaldehyde': {
            'quantities': ['750 mg', '24.6 mmol', '1.03 equiv'],
        },
        'EtOAc': {
            'quantities': ['50 mL', '15 mL', '3 x 25 mL']
        },
        'TMSCl': {
            'quantities': ['3.3 mL', '24.6 mmol', '1.03 equiv']
        },

        # Step 3
        "N,N'-1,3-bis(2,6-diisopropylphenyl)imidazolium chloride(S2)": {
            'quantities': ['8.7 g', '21.7 mmol', '1.00 equiv']
        },
        'THF': {
            'quantities': ['10 mL', '26 mL', '3 x 10 mL'],
        },
        'KOtBu': {
            'quantities': ['2.92 g', '26.0 mmol', '1.20 equiv']
        },
        '2M 1,1,1,2,2,2 hexachloroethane solution': {
            'quantities': ['13 mL', '26.0 mmol', '1.20 equiv']
        },
        'toluene': {
            'quantities': ['6 x 10 mL'],
        },
        'CH2Cl2': {
            'quantities': ['50 mL', '3 x 15 mL'],
        },
    },
    'steps': [
        # Step 1
        Add,
        HeatChillToTemp,
        Add,
        Stir,
        HeatChill,
        Filter,
        WashSolid,
        Dry,

        # Step 2
        Add,
        Add,
        Add,
        HeatChillToTemp,
        Add,
        Stir,
        HeatChillToTemp,
        Filter,
        WashSolid,
        Dry,

        # Step 3
        HeatChillToTemp,
        Add,
        Add,
        Add,
        Stir,
        HeatChillToTemp,
        Add,
        HeatChillToTemp,
        Stir,
        HeatChillToTemp,
        Filter,
        WashSolid,
        WashSolid,
        Dry,
        Dissolve,
        FilterThrough,
        Evaporate,
    ],
    'vessels': [
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'filter_vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},

        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'filter_vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},

        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'filter_vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'from_vessel': 'filter', 'to_vessel': 'rotavap'},
        {'rotavap_name': 'rotavap'},
    ],
    'properties': [
        # Step 1
        # Add
        {
            'volume': 25.2,
            'stir': False,
            'reagent': '2,6-diisopropylaniline and HOAc MeOH solution'
        },
        # HeatChillToTemp
        {
            'temp': 50,
        },
        # Add
        {
            'reagent': 'glyoxal MeOH solution',
            'volume': 18,
            'stir': True,
        },
        # Stir
        {
            'time': 15 * 60,
        },
        # HeatChill
        {
            'temp': 23,
            'time': 10 * 60 * 60,
        },
        # Filter
        {},
        # WashSolid
        {
            'solvent': 'MeOH',
            'volume': 15,
            'repeat': 3,
        },
        # Dry
        {
            'vacuum_pressure': 75,
        },

        # Step 2
        # Add
        {
            'reagent': 'paraformaldehyde',
            'mass': 0.75,
            'stir': False,
        },
        # Add
        {
            'reagent': "N,N'-1,4-bis(2,6-diisopropylphenyl)-1,4-diaza-butadiene(S1)",
            'mass': 8.9,
            'stir': False
        },
        # Add
        {
            'reagent': 'EtOAc',
            'volume': 50,
            'stir': False,
        },
        # HeatChillToTemp
        {
            'temp': 70,
        },
        # Add
        {
            'reagent': 'TMSCl EtOAc solution',
            'volume': 18.3,
            'time': 45 * 60,
            'stir': True,
            'stir_speed': 600,
        },
        # Stir
        {
            'time': 2 * 60 * 60,
        },
        # HeatChillToTemp
        {
            'temp': 10,
        },
        # Filter
        {},
        #  WashSolid
        {
            'solvent': 'EtOAc',
            'volume': 25,
            'repeat': 3,
        },
        # Dry
        {
            'time': 2 * 60 * 60,
            'vacuum_pressure': 75
        },

        # Step 3
        # HeatChillToTemp
        {
            'temp': 23,
        },
        # Add
        {
            'reagent': "N,N'-1,3-bis(2,6-diisopropylphenyl)imidazolium chloride(S2)",
            'mass': 8.7,
            'stir': False,
        },
        # Add
        {
            'reagent': 'THF',
            'volume': 10,
            'stir': False,
        },
        # Add
        {
            'reagent': 'KOtBu THF solution',
            'volume': 26,
            'stir': True,
        },
        # Stir
        {
            'time': 4 * 60 * 60,
        },
        # HeatChillToTemp
        {
            'temp': -35,
        },
        # Add
        {
            'reagent': "2M 1,1,1,2,2,2 hexachloroethane solution",
            'volume': 13,
            'stir': True,
        },
        # HeatChillToTemp
        {
            'temp': 23,
        },
        # Stir
        {
            'time': 24 * 60 * 60,
        },
        # HeatChillToTemp
        {
            'temp': -35,
        },
        # Filter
        {
            'filter_vessel': 'filter',
        },
        # WashSolid
        {
            'solvent': 'THF',
            'volume': 10,
            'temp': -20,
            'repeat': 3,
        },
        # WashSolid
        {
            'solvent': 'toluene',
            'volume': 10,
            'temp': 23,
            'repeat': 6,
        },
        # Dry
        {},
        # Dissolve
        {
            'vessel': 'filter',
            'solvent': 'CH2Cl2',
            'volume': 50,
        },
        # FilterThrough
        {
            'through': 'celite',
            'eluting_solvent': 'CH2Cl2',
            'eluting_volume': 15,
            'eluting_repeats': 3,
        },
        # Evaporate
        {
            'temp': 50,
            'pressure': 699,
            'time': 30 * 60,
            'mode': 'auto',
        }
    ],
}
