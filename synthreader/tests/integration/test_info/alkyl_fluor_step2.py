from chemputerxdl.steps import *
from xdl.steps import *

ALKYL_FLUOR_STEP2_TEXT = '''In air, to N,N'-1,4-bis(2,6-diisopropylphenyl)-1,4-diaza-butadiene (S1) (226 g, 0.600 mol, 1.00 equiv) and paraformaldehyde (18.1 g, 0.603 mol, 1.03 equiv) in 5.4 L of EtOAc in a flask at 70°C was added a solution of TMSCl (76.5 mL, 0.603 mol, 1.03 equiv) in 80 mL of EtOAc dropwise over 45 min with vigorous stirring.  The reaction mixture was stirred at 70°C for 2 h. After cooling to 10°C with stirring, the reaction mixture was filtered.  The filter cake was washed with EtOAc (3 x 500 mL) and dried in vacuo to afford 220 g of compound S2 as a colorless solid (86% yield).'''

ALKYL_FLUOR_STEP2_INFO = {
    'name': 'alkyl_fluor_step2',
    'text': ALKYL_FLUOR_STEP2_TEXT,
    'reagents': {
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
    },
    'steps': [
        Add,
        HeatChillToTemp,
        Add,
        Stir,
        HeatChillToTemp,
        Filter,
        WashSolid,
        Dry,
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
    ],
}
