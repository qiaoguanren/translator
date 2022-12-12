from chemputerxdl.steps import *
from xdl.steps import *

ALKYL_FLUOR_STEPS_1_3_TEXT = '''In air, to a solution of 2,6-diisopropylaniline (197 g, 1.00 mol, 2.00 equiv) and HOAc (1.0 mL, 0.018 mol, 0.035 equiv) in 250 mL of MeOH at 50°C in a flask was added a solution of glyoxal (73 g, 0.50 mol, 1.0 equiv) in 250 mL of MeOH. The reaction mixture was stirred at 50°C for 15 min and then stirred at 23°C for 10 h. The reaction mixture was filtered. The filter cake was washed with MeOH (3 x 100 mL) and dried in vacuo to afford 169 g of compound S1 as a yellow solid (90% yield).

In air, to N,N'-1,4-bis(2,6-diisopropylphenyl)-1,4-diaza-butadiene (S1) (226 g, 0.600 mol, 1.00 equiv) and paraformaldehyde (18.1 g, 0.603 mol, 1.03 equiv) was added 5.4 L of EtOAc at 70°C. A solution of TMSCl (76.5 mL, 0.603 mol, 1.03 equiv) in 80 mL of EtOAc was then added at 70°C, dropwise, over 45 min, with vigorous stirring.  The reaction mixture was stirred at 70°C for 2 h. After cooling to 10°C with stirring, the reaction mixture was filtered.  The filter cake was washed with EtOAc (3 x 500 mL) and dried in vacuo to afford 220 g of compound S2 as a colorless solid (86% yield).

To N,N'-1,3-bis(2,6-diisopropylphenyl)imidazolium chloride(S2) (150 g, 353 mmol, 1.00 equiv) was added 700 mL of THF and a solution of KOtBu (47.4 g, 423 mmol, 1.20 equiv) in 423 mL of THF at 23°C. The reaction mixture was stirred at 23°C for 4 h. The reaction mixture was cooled to -40°C and 1M 1,1,1,2,2,2-hexachloroethane solution (423 mL, 1.20 equiv) was added. The reaction mixture was warmed to 23°C and stirred at this temperature for 24 h. The reaction mixture was cooled to -40°C  and filtered. The filter cake was washed with THF (3 x 100 mL) and toluene (6 x 100 mL) at -40°C. It was then dissolved in CH2Cl2 (500 mL) at room temperature and filtered through a pad of Celite (10 g) eluting with CH2Cl2 (3 x 50 mL). The filtrate was concentrated under reduced pressure to afford 131 g of compound S3 as a colorless solid (81% yield).
'''

ALKYL_FLUOR_STEPS_1_3_INFO = {
    'name': 'alkyl_fluor_steps_1_3',
    'text': ALKYL_FLUOR_STEPS_1_3_TEXT,
    'reagents': {
        # Step 1
        '2,6-diisopropylaniline': {
            'quantities': ['197 g'],
        },
        'HOAc': {
            'quantities': ['1.0 mL'],
        },
        'MeOH': {
            'quantities': ['250 mL', '250 mL', '3 x 100 mL']
        },
        'glyoxal': {
            'quantities': ['73 g'],
        },

        # Step 2
        "N,N'-1,4-bis(2,6-diisopropylphenyl)-1,4-diaza-butadiene(S1)": {
            'quantities': ['226 g', '0.600 mol', '1.00 equiv']
        },
        'paraformaldehyde': {
            'quantities': ['18.1 g', '0.603 mol', '1.03 equiv'],
        },
        'EtOAc': {
            'quantities': ['5.4 L', '80 mL', '3 x 500 mL']
        },
        'TMSCl': {
            'quantities': ['76.5 mL', '0.603 mol', '1.03 equiv']
        },

        # Step 3
        "N,N'-1,3-bis(2,6-diisopropylphenyl)imidazolium chloride(S2)": {
            'quantities': ['150 g', '353 mmol', '1.00 equiv']
        },
        'THF': {
            'quantities': ['700 mL', '3 x 100 mL'],
        },
        'KOtBu': {
            'quantities': ['47.4 g', '423 mmol', '1.20 equiv']
        },
        '1M 1,1,1,2,2,2 hexachloroethane solution': {
            'quantities': ['423 mL', '1.20 equiv']
        },
        'toluene': {
            'quantities': ['6 x 100 mL'],
        },
        'CH2Cl2': {
            'quantities': ['500 mL', '3 x 50 mL'],
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
}
