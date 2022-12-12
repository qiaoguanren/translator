from chemputerxdl.steps import *
from xdl.steps import *
from synthreader.finishing.constants import DEFAULT_AUTO_EVAPORATION_TIME_LIMIT

ORGSYN_V87P0231_A_TEXT = '''An oven dried, 1-L, three-necked, round-bottomed flask equipped with a magnetic stirring bar (5 cm Teflon coated ovoid-shaped), a 250-mL pressure-equalizing addition funnel fitted with an argon inlet, two rubber septa, and a thermocouple probe is sequentially charged with benzylamine (11.5 mL, 11.3 g, 105.3 mmol, 1.05 equiv), triethylamine (15.5 mL, 11.3 g, 111.2 mmol, 1.1 equiv), and 250 mL of dichloromethane (Notes 1 and 2). The solution is cooled to 2-4 °C (internal temperature) in an ice bath and a solution of p-toluenesulfonyl chloride (19.1 g, 100.2 mmol) (Note 3) in 100 mL of dichloromethane is added dropwise via the addition funnel over 45 min. During the addition, the internal temperature of the flask is maintained below 5 °C. The mixture is stirred for 30 min at 2-4 °C. The ice bath is then removed and the resulting solution is allowed to warm to 21 °C, stirred at this temperature for 13 h, and then quenched by addition of 1 M HCl (500 mL). The resulting mixture is transferred to a 1-L separatory funnel and the organic layer is separated and washed with 1 M HCl (500 mL), 1 M NaOH (500 mL), saturated aqueous NaCl solution (500 mL), dried over MgSO4 (15 g), filtered, and concentrated by rotary evaporation (25 °C, 25 mmHg). The resulting solid is dried under vacuum (0.2 mmHg, 6 h) to afford 25.6 g (98%) of 4-methyl-N-(phenylmethyl)benzenesulfonamide as a white solid (Note 4).'''

ORGSYN_V87P0231_A_INFO = {
    'text': ORGSYN_V87P0231_A_TEXT,
    'name': 'orgsyn_v87p0231_a',
    'reagents': {
        'benzylamine': {
            'quantities': ['11.5 mL', '11.3 g', '105.3 mmol', '1.05 equiv'],
        },
        'triethylamine': {
            'quantities': ['15.5 mL', '11.3 g', '111.2 mmol', '1.1 equiv'],
        },
        'dichloromethane': {
            'quantities': ['250 mL', '100 mL'],
        },
        'p-toluenesulfonyl chloride': {
            'quantities': ['19.1 g', '100.2 mmol'],
        },
        '1 M HCl': {
            'quantities': ['500 mL', '500 mL'],
        },
        '1 M NaOH': {
            'quantities': ['500 mL'],
        },
        'saturated aqueous NaCl solution': {
            'quantities': ['500 mL'],
        },
        'MgSO4': {
            'quantities': ['15 g'],
        },
        '4 methyl-N-(phenylmethyl)benzenesulfonamide (98 %)': {
            'quantities': ['25.6 g', '98 %'],
        },
    },
    'steps': [
        Add,
        Add,
        Add,
        HeatChillToTemp,
        Add,
        Stir,
        HeatChillToTemp,
        HeatChill,
        Add,
        Separate,
        Separate,
        Separate,
        Separate,
        Evaporate,
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
        # Transfer
        {
            'from_vessel': 'reactor',
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
            'to_vessel': 'separator',
        },
        # Separate
        {
            'from_vessel': 'separator',
            'separation_vessel': 'separator',
            'to_vessel': 'rotavap',
            'through': 'MgSO4',
        },
        # Evaporate
        {
            'rotavap_name': 'rotavap',
        },
        # Dry
        {
            'vessel': 'rotavap',
        },
    ],
    'properties': [
        # Add
        {
            'reagent': 'benzylamine',
            'volume': 11.5,
            'stir': False,
        },
        # Add
        {
            'reagent': 'triethylamine',
            'volume': 15.5,
            'stir': True,
        },
        # Add
        {
            'reagent': 'dichloromethane',
            'volume': 250.0,
            'stir': True,
        },
        # HeatChillToTemp
        {
            'temp': 3.0,
        },
        # Add
        {
            'reagent': 'p-toluenesulfonyl chloride dichloromethane solution',
            'volume': 100.0,
            'time': 2700.0,
            'stir': True,
        },
        # Stir
        {
            'time': 1800.0,
        },
        # HeatChillToTemp
        {
            'temp': 18,
            'active': False,
            'continue_heatchill': False,
        },
        # Stir
        {
            'time': 46800.0,
        },
        # Add
        {
            'reagent': '1 M HCl',
            'volume': 500.0,
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
        },
        # Separate
        {
            'purpose': 'wash',
            'product_bottom': True,
            'solvent': '1 M HCl',
            'solvent_volume': 500.0,
            'n_separations': 1,
        },
        # Separate
        {
            'purpose': 'wash',
            'product_bottom': True,
            'solvent': '1 M NaOH',
            'solvent_volume': 500.0,
            'n_separations': 1,
        },
        # Separate
        {
            'purpose': 'wash',
            'product_bottom': True,
            'solvent': 'saturated aqueous NaCl solution',
            'solvent_volume': 500.0,
            'n_separations': 1,
        },
        # Evaporate
        {
            'temp': 25,
            'pressure': 33.3305,
        },
        # Dry
        {
            'time': 21600.0,
            'vacuum_pressure': 0.2666,
        },
    ],
}
