from chemputerxdl.steps import *
from xdl.steps import *
from synthreader.finishing.constants import DEFAULT_SLOW_ADDITION_DISPENSE_SPEED

ORGSYN_V95P0060_TEXT = '''A 1-L, three-necked, round-bottomed flask is equipped with an oval Teflon-coated magnetic stir bar, a rubber septum, a nitrogen line fitted to a glass bubbler filled with mineral oil, and a 250-mL pressure-equalizing addition funnel capped with a rubber septum pierced with a needle (Notes 2, 3, 4, and 5) (Figure 1).
While under a continuous flow of nitrogen, the flask is dried with a heat gun and then allowed to cool to room temperature. The needle on the addition funnel is removed. Then the septum on the flask is removed and the flask is charged with 200 mL of dichloromethane (Note 6), Oxone (80.0 g, 130 mmol, 2.6 equiv) (Note 7), and pyridinium bromide (365 mg, 2.25 mmol, 0.045 equiv) (Note 8) (Figure 2). The heterogeneous mixture is stirred for 15 min until a faint yellow color develops (Figure 3).
Dry pyridine (20 mL, 19.6 g, 250 mmol, 5 equiv) (Note 9) is then added via syringe through the rubber septum (Figure 3), upon which the yellow color of the reaction mixture intensifies (Figure 4). The reaction mixture is stirred for 1-2 min, the septum is then removed and the 4-acetamidoTEMPO catalyst (533 mg, 2.50 mmol, 0.050 equiv) (Note 10) is added in one portion.

The septum is placed back on the flask and the reaction mixture, which darkens upon addition of the catalyst (Figure 5), is stirred for 15-30 min.

A clean, dry 125-mL Erlenmeyer flask is charged with dodecylamine (9.24 g, 49.9 mmol, 1 equiv) (Note 11) and 100 mL of dichloromethane. The Erlenmeyer flask is swirled to dissolve the amine. The septum on the addition funnel is removed and the homogenous solution of the amine is transferred to the addition funnel through the use of a funnel. The Erlenmeyer flask is then rinsed with additional dichloromethane (10 mL) to ensure complete transfer and to rinse any residual amine from the funnel. The funnel is then removed and the septum is placed back onto the addition funnel. An additional nitrogen line is added through the septum of the addition funnel and the addition rate is adjusted to ensure a constant delivery of the amine solution at approximately 40-50 mL/h (Figure 6). Addition of the amine takes approximately 2-2.5 h to complete, at which point additional dichloromethane (20 mL) is added via syringe to the funnel (Note 12) (Figure 8) allowing for any residual white solid (Figure 7) to be rinsed into the reaction flask. The light yellow reaction mixture (Figure 8) is stirred at 23 °C (Note 13) for an additional 9-15 h (Note 14).

During this time the reaction mixture turns from a yellow suspension (Figure 9) to a clear yellow solution with sticky yellow solids along the wall of the round-bottomed flask (Figure 10).

A 600-mL medium porosity, sintered glass Büchner funnel is filled with 150 g of silica gel (Note 15), and a small filter paper (90 mm diameter, coarse porosity) is placed on top of the silica gel. The funnel is then fitted to a 1-L round-bottomed flask, set up for vacuum filtration, and the reaction mixture is poured through the filtration setup (Figure 11). The reaction flask is rinsed with an additional 300 mL of dichloromethane and poured through the filtration setup (Note 16) (Figure 12). The yellow solids remain in the original flask (Figure 13).

The filtrate is concentrated by rotary evaporation (30--40 °C, 500 mmHg then to approx. 15 mmHg for 15-30 min) (Note 17) to afford dodecanenitrile (8.80 g, 94%) (Notes 18 and 19) as a pale yellow oil (Notes 20, 21, and 22). However, the title compound is reported in the literature as a clear, colorless oil.3 Colorless product is obtained by transferring the pale yellow crude oil (Note 23) to a 25-mL round-bottomed flask from the 1-L round-bottomed flask. The remaining oil in the 1-L round-bottomed flask is rinsed with dichloromethane (2 x 5 mL) and transferred to the 25-mL round-bottomed flask to ensure all the oil is transferred. Then the dichloromethane was removed by rotary evaporation (30-40 °C, 500 mmHg then to approx. 15 mmHg for 15-30 min). The 25-mL round-bottomed flask is then set up for bulb-to-bulb distillation (Kugelrohr, bath temp: 200 °C, 10-20 mmHg) (Figure 14) to afford analytically pure dodecanenitrile (8.37 g, 93% yield) (Notes 24, 25, 26, and 27), as a clear colorless oil.'''

ORGSYN_V95P0060_INFO = {
    'text': ORGSYN_V95P0060_TEXT,
    'name': 'orgsyn_v95p0060',
    'reagents': {
        'dichloromethane': {
            'quantities': ['200 mL', '100 mL', '10 mL', '20 mL', '300 mL', '2 x 5 mL'],
        },
        'oxone': {
            'quantities': ['80.0 g', '130 mmol', '2.6 equiv'],
        },
        'pyridinium bromide': {
            'quantities': ['365 mg', '2.25 mmol', '0.045 equiv'],
        },
        'dry pyridine': {
            'quantities': ['20 mL', '19.6 g', '250 mmol', '5 equiv'],
        },
        'the 4-acetamidoTEMPO catalyst': {
            'quantities': ['533 mg', '2.50 mmol', '0.050 equiv'],
        },
        'dodecylamine': {
            'quantities': ['9.24 g', '49.9 mmol', '1 equiv'],
        },
        'the amine': {
            'quantities': [],
        },
        'amine': {
            'quantities': [],
        },
        'solids': {
            'quantities': [],
        },
        'silica gel': {
            'quantities': ['150 g'],
        },
        'dodecanenitrile (94 %)': {
            'quantities': ['8.80 g', '94 %'],
        },
        'the dichloromethane': {
            'quantities': [],
        },
        'analytically pure dodecanenitrile': {
            'quantities': [],
        },
    },
    'steps': [
        Dry,
        HeatChillToTemp,
        Add,
        Add,
        Add,
        Stir,
        Add,
        Stir,
        Add,
        Stir,
        Add,
        Add,
        Stir,
        Add,
        Add,
        HeatChill,
        Filter,
        Add,
        Filter,
        Evaporate,
        Evaporate,
        Repeat,
        Evaporate,
        Evaporate,
        Distill,
    ],
    'vessels': [
        # Dry
        {
            'vessel': 'filter',
        },
        # HeatChillToTemp
        {
            'vessel': 'filter',
        },
        # Add
        {
            'vessel': 'filter',
        },
        # Add
        {
            'vessel': 'filter',
        },
        # Add
        {
            'vessel': 'filter',
        },
        # Stir
        {
            'vessel': 'filter',
        },
        # Add
        {
            'vessel': 'filter',
        },
        # Stir
        {
            'vessel': 'filter',
        },
        # Add
        {
            'vessel': 'filter',
        },
        # Stir
        {
            'vessel': 'filter',
        },
        # Add
        {
            'vessel': 'filter',
        },
        # Add
        {
            'vessel': 'filter',
        },
        # Stir
        {
            'vessel': 'filter',
        },
        # Add
        {
            'vessel': 'filter',
        },
        # Add
        {
            'vessel': 'filter',
        },
        # HeatChill
        {
            'vessel': 'filter',
        },
        # Filter
        {},
        # Add
        {
            'vessel': 'filter',
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
        # Evaporate
        {
            'rotavap_name': 'rotavap',
        },
        # Repeat
        {
            'children': [
                # Add
                {
                    'vessel': 'rotavap',
                },
            ]
        },
        # Evaporate
        {
            'rotavap_name': 'rotavap',
        },
        # Evaporate
        {
            'rotavap_name': 'rotavap',
        },
        # Distill
        {},
    ],
    'properties': [
        # Dry
        {},
        # HeatChillToTemp
        {
            'temp': 25,
            'active': False,
            'continue_heatchill': False,
        },
        # Add
        {
            'reagent': 'dichloromethane',
            'volume': 200.0,
            'stir': False,
        },
        # Add
        {
            'reagent': 'oxone',
            'mass': 80.0,
            'stir': True,
        },
        # Add
        {
            'reagent': 'pyridinium bromide',
            'mass': 0.365,
            'stir': True,
        },
        # Stir
        {
            'time': 900.0,
        },
        # Add
        {
            'reagent': 'dry pyridine',
            'volume': 20.0,
            'dispense_speed': DEFAULT_SLOW_ADDITION_DISPENSE_SPEED,
            'stir': True,
        },
        # Stir
        {
            'time': 90.0,
        },
        # Add
        {
            'reagent': 'the 4-acetamidoTEMPO catalyst',
            'mass': 0.533,
            'stir': True,
        },
        # Stir
        {
            'time': 1350.0,
        },
        # Add
        {
            'reagent': 'dodecylamine',
            'mass': 9.24,
            'stir': True,
        },
        # Add
        {
            'reagent': 'dichloromethane',
            'volume': 100.0,
            'stir': True,
        },
        # Stir
        {
            'time': 300.0,
        },
        # Add
        {
            'reagent': 'dichloromethane',
            'volume': 10.0,
            'stir': True,
        },
        # Add
        {
            'reagent': 'dichloromethane',
            'volume': 20.0,
            'dispense_speed': DEFAULT_SLOW_ADDITION_DISPENSE_SPEED,
            'stir': True,
        },
        # HeatChill
        {
            'temp': 23.0,
            'time': 43200.0,
        },
        # Filter
        {
            'filter_vessel': 'filter',
        },
        # Add
        {
            'reagent': 'dichloromethane',
            'volume': 300.0,
            'stir': False,
        },
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
            'pressure': 666.61,
            'time': 1800,
            'mode': 'auto',
        },
        # Evaporate
        {
            'temp': 35.0,
            'pressure': 19.9983,
            'time': 1350.0,
            'mode': 'auto',
        },
        # Repeat
        {
            'repeats': 2,
            'children': [
                # Add
                {
                    'reagent': 'dichloromethane',
                    'volume': 5.0,
                    'stir': False,
                },
            ]
        },
        # Evaporate
        {
            'temp': 35.0,
            'pressure': 666.61,
            'time': 1800,
            'mode': 'auto',
        },
        # Evaporate
        {
            'temp': 35.0,
            'pressure': 19.9983,
            'time': 1350.0,
            'mode': 'auto',
        },
        # Distill
        {},
    ],
}
