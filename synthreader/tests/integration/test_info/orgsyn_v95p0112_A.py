from chemputerxdl.steps import *
from xdl.steps import *

ORGSYN_V95P0112_A_TEXT = '''A 500 mL single-necked, round-bottomed flask equipped with a 3 cm stirrer bar and a needle-pierced septum is charged with methyl (tert-butoxycarbonyl)-glycinate 1 (Note 2) (6.80 g, 36.0 mmol, 1.20 equiv) and methanol (Note 3) (225 mL). 1-Amino pyridinium iodide (Note 4) (6.67 g, 30.0 mmol) is added and the reaction is stirred for 5 min at 22 °C. Potassium carbonate (Note 5) (9.95 g, 72.0 mmol, 2.40 equiv) is added and the reaction is stirred at 22 °C for 64 h (Note 6) (the yellow heterogeneous reaction turns colorless two seconds after the addition of potassium carbonate, and forms a dark purple solution, Figure 1). After removal of the stir bar, 200 mL of the methanol is removed under reduced pressure (200 mmHg to 70 mmHg, 40 °C) to give a brown-purple syrup, which is poured onto an alumina pad (Notes 7 and 8).

The flask is rinsed with 10 mL of dichloromethane as well as 50 mL of eluent (dichloromethane-methanol, 9:1), and the product is eluted with 1.1 L of dichloromethane-methanol (9:1) (Note 9). The filtrate is concentrated (375 mmHg to 75 mmHg, 40 °C) and then transferred to a 500 mL single-necked round-bottomed flask and rinsed with dichloromethane (20 mL). The filtrate is concentrated further (375 mmHg to 15 mmHg, 40 °C) and then dried under vacuum (0.08 mmHg, 20 °C, 1 h) to give a brown powder (Note 10). A 3 cm Teflon coated stirrer bar is added, followed by acetone (175 mL) (Note 11). A water-cooled condenser is added to the flask and the mixture is heated to reflux until complete dissolution had occurred (15 min). The mixture is allowed to cool to room temperature over 3 h and then cooled to -22 °C in a freezer for 20 h. The resultant fine brown crystals are filtered off through a sintered S3 funnel, the flask is rinsed with diethyl ether (Note 12) (3 x 25 mL), and the contents were then added to the funnel.'''

ORGSYN_V95P0112_A_INFO = {
    'text': ORGSYN_V95P0112_A_TEXT,
    'name': 'orgsyn_v95p0112_a',
    'reagents': {
        'methyl(tert-butoxycarbonyl)-glycinate 1': {
            'quantities': ['6.80 g', '36.0 mmol', '1.20 equiv'],
        },
        'methanol': {
            'quantities': ['225 mL'],
        },
        '1-Amino pyridinium iodide': {
            'quantities': ['6.67 g', '30.0 mmol'],
        },
        'potassium carbonate': {
            'quantities': ['9.95 g', '72.0 mmol', '2.40 equiv'],
        },
        'the methanol': {
            'quantities': ['200 mL'],
        },
        'dichloromethane': {
            'quantities': ['10 mL', '20 mL'],
        },
        'dichloromethane-methanol': {
            'quantities': ['50 mL', '1.1 L'],
        },
        'acetone': {
            'quantities': ['175 mL'],
        },
        'the resultant': {
            'quantities': [],
        },
        'S3': {
            'quantities': [],
        },
        'diethyl ether': {
            'quantities': ['3 x 25 mL'],
        },
    },
    'steps': [
        Add,
        Add,
        Add,
        HeatChill,
        Add,
        HeatChill,
        Evaporate,
        FilterThrough,
        Add,
        Add,
        FilterThrough,
        Evaporate,
        Add,
        Evaporate,
        Dry,
        Add,
        HeatChill,
        HeatChillToTemp,
        HeatChill,
        Filter,
        WashSolid,
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
        # Add
        {
            'vessel': 'reactor',
        },
        # HeatChill
        {
            'vessel': 'reactor',
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
        # FilterThrough
        {
            'from_vessel': 'rotavap',
            'to_vessel': 'rotavap',
            'through': 'alumina',
        },
        # Add
        {
            'vessel': 'rotavap',
        },
        # Add
        {
            'vessel': 'rotavap',
        },
        # FilterThrough
        {
            'from_vessel': 'rotavap',
            'to_vessel': 'rotavap',
            'through': 'alumina',
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
        # Transfer
        {
            'from_vessel': 'rotavap',
            'to_vessel': 'filter',
        },
        # Add
        {
            'vessel': 'filter',
        },
        # HeatChill
        {
            'vessel': 'filter',
        },
        # HeatChillToTemp
        {
            'vessel': 'filter',
        },
        # HeatChill
        {
            'vessel': 'filter',
        },
        # Filter
        {},
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
        # Add
        {
            'reagent': 'methyl(tert-butoxycarbonyl)-glycinate 1',
            'mass': 6.8,
            'stir': False,
        },
        # Add
        {
            'reagent': 'methanol',
            'volume': 225.0,
            'stir': False,
        },
        # Add
        {
            'reagent': '1-Amino pyridinium iodide',
            'mass': 6.67,
            'stir': True,
        },
        # HeatChill
        {
            'temp': 22.0,
            'time': 300.0,
        },
        # Add
        {
            'reagent': 'potassium carbonate',
            'mass': 9.95,
            'stir': True,
        },
        # HeatChill
        {
            'temp': 22.0,
            'time': 230400.0,
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Evaporate
        {
            'temp': 40.0,
            'pressure': 179.9847,
            'time': 1800,
            'mode': 'auto',
        },
        # FilterThrough
        {},
        # Add
        {
            'reagent': 'dichloromethane',
            'volume': 10.0,
            'stir': True,
        },
        # Add
        {
            'reagent': 'dichloromethane-methanol',
            'volume': 50.0,
            'stir': True,
        },
        # FilterThrough
        {
            'eluting_solvent': 'dichloromethane-methanol',
            'eluting_volume': 1100.0,
        },
        # Evaporate
        {
            'temp': 40.0,
            'pressure': 299.97450000000003,
            'time': 1800,
            'mode': 'auto',
        },
        # Add
        {
            'reagent': 'dichloromethane',
            'volume': 20.0,
            'stir': False,
        },
        # Evaporate
        {
            'temp': 40.0,
            'pressure': 259.97790000000003,
            'time': 1800,
            'mode': 'auto',
        },
        # Dry
        {
            'temp': 20.0,
            'vacuum_pressure': 0.1066576,
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Add
        {
            'reagent': 'acetone',
            'volume': 175.0,
            'stir': True,
        },
        # HeatChill
        {
            'temp': 56.05,
            'time': 900.0,
        },
        # HeatChillToTemp
        {
            'temp': 25,
            'active': False,
            'continue_heatchill': False,
        },
        # HeatChill
        {
            'temp': -22.0,
            'time': 72000.0,
        },
        # Filter
        {
            'filter_vessel': 'filter',
        },
        # WashSolid
        {
            'solvent': 'diethyl ether',
            'volume': 25.0,
            'repeat': 3,
        },
        # Dry
        {},
    ],
}
