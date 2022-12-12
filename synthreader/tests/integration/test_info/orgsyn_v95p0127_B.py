from chemputerxdl.steps import *
from xdl.steps import *
from synthreader.finishing.constants import DEFAULT_SLOW_ADDITION_DISPENSE_SPEED

ORGSYN_V95P0127_B_TEXT = '''A dry and argon flushed 1 L Schlenk-flask equipped with a 5×2-cm Teflon-coated magnetic stirring bar and a septum is filled with argon and then weighed. 3-Bromopyridine (6.32 g, 40.0 mmol, 1 equiv) (Note 8) and dry THF (50 mL, 0.8 M) are added to the flask via syringe (Note 9). The solution is cooled in an ice-water bath under an atmosphere of argon and stirred for at least 5 min at 0 °C before iPrMgCl·LiCl (35.2 mL, 1.25 M, 44.0 mmol, 1.1 equiv) (Note 10) is added via a syringe pump over the period of 30 min (Note 11). The ice bath is removed and the solution is stirred for 3 h at 25 °C during which time it gradually turns from yellow to dark red (Note 12). Upon completion of the reaction, solid Zn(OPiv)2 (12.3 g, 46.0 mmol, 1.15 equiv) is added in one portion under argon counterflow via a powder funnel. A slight exotherm is noticed (Note 13). The mixture is stirred at 25 °C for 30 min leading to a clear dark red solution. The solvent is removed using a vacuum line (0.1 mmHg) and a liquid nitrogen cold trap. The solid residue is dried for at least 2 h longer leading to a voluminous yellow foam (Figure 2) (Note 14). The foam is crushed with a spatula under argon counterflow to form a fine yellow powder. This powder is dried under high vacuum (0.1 mmHg) for further 2 h. The resulting pyridine-3-ylzinc pivalate (28.6-28.8 g, 1.1-1.20 mmol g-1, 31.5-34.5 mmol, 79-86%) is used immediately.
After the drying process is complete, the argon-flushed flask is weighed to determine the weight of the resulting powder. To determine the actual content in zinc species and the reaction yield, a small aliquot of the powder (accurately weighed amount, ca. 1 g, see Figure 3: a) is titrated using a 1 M solution of iodine in THF (Note 15) with a color change from red (b) to bright yellow (c) until the persisting brown color of the iodine (d) indicates the completion of the titration (Note 16).'''

ORGSYN_V95P0127_B_INFO = {
    'text': ORGSYN_V95P0127_B_TEXT,
    'name': 'orgsyn_v95p0127_b',
    'reagents': {
        '3-Bromopyridine': {
            'quantities': ['6.32 g', '40.0 mmol', '1 equiv'],
        },
        'dry THF': {
            'quantities': ['50 mL', '0.8 M'],
        },
        'iPrMgCl·LiCl': {
            'quantities': ['35.2 mL', '1.25 M', '44.0 mmol', '1.1 equiv'],
        },
        'solid Zn(OPiv)2': {
            'quantities': ['12.3 g', '46.0 mmol', '1.15 equiv'],
        },
        'the resulting pyridine-3-ylzinc pivalate': {
            'quantities': [],
        },
        'iodine': {
            'quantities': [],
        },
        'THF': {
            'quantities': [],
        },
        '(b)': {
            'quantities': [],
        },
        '(c)': {
            'quantities': [],
        },
        'the iodine(d)indicates': {
            'quantities': [],
        },
    },
    'steps': [
        Add,
        Add,
        HeatChillToTemp,
        Stir,
        Add,
        HeatChill,
        Add,
        HeatChill,
        Dry,
        Dry,
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
        # HeatChill
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
        # Dry
        {
            'vessel': 'reactor',
        },
        # Dry
        {
            'vessel': 'reactor',
        },
        # Dry
        {
            'vessel': 'reactor',
        },
    ],
    'properties': [
        # Add
        {
            'reagent': '3-Bromopyridine',
            'mass': 6.32,
            'stir': False,
        },
        # Add
        {
            'reagent': 'dry THF',
            'volume': 50.0,
            'dispense_speed': DEFAULT_SLOW_ADDITION_DISPENSE_SPEED,
            'stir': False,
        },
        # HeatChillToTemp
        {
            'temp': 0,
        },
        # Stir
        {
            'time': 300.0,
        },
        # Add
        {
            'reagent': 'iPrMgCl·LiCl',
            'volume': 35.2,
            'time': 1800.0,
            'stir': True,
        },
        # HeatChill
        {
            'temp': 25.0,
            'time': 10800.0,
        },
        # Add
        {
            'reagent': 'solid Zn(OPiv)2',
            'mass': 12.3,
            'stir': True,
        },
        # HeatChill
        {
            'temp': 25.0,
            'time': 1800.0,
        },
        # Dry
        {
            'vacuum_pressure': 0.13332200000000002,
        },
        # Dry
        {
            'time': 7200.0,
        },
        # Dry
        {
            'vacuum_pressure': 0.13332200000000002,
        },
    ],
}
