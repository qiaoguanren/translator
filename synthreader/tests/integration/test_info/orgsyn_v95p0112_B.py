from chemputerxdl.steps import *
from xdl.steps import *

ORGSYN_V95P0112_B_TEXT = '''A three-necked 250 mL round-bottomed flask equipped with a septum, a glass stopper, a vacuum tap and 2 cm Teflon coated stirrer bar is flame-dried under vacuum (0.12 mmHg) for 1 min and then backfilled with nitrogen. The evacuation/nitrogen purge is repeated a total of 3 times, and then the reaction vessel is allowed to cool to room temperature (22 °C) under a positive pressure of nitrogen. The flask is sequentially charged with N-benzyl-4-methyl-N-(phenylethynyl)benzene-sulfonamide (Note 16) (4.69 g, 13.0 mmol), dichloro(2-pyridinecarboxylato)gold (Note 17) (51.02 mg, 0.13 mmol) and ((tert-butoxycarbonyl)glycyl)(pyridin-1-ium-1-yl)amide (3.60 g, 14.3 mmol, 1.1 equiv). Toluene (130 mL) (Note 18) is added and the flask is placed in a preheated aluminium mantle and stirred at 90 °C (controlled by an external probe) for 5.5 h (Note 19). The heterogeneous mixture becomes a homogenous orange-brown solution over the first hour.

Upon completion, the flask is removed from the heating mantle and the reaction is allowed to cool to room temperature for 1 h. The crude reaction mixture is filtered through a silica pad (Note 20) and then the reaction flask is rinsed with ethyl acetate (2 x 50 mL) (Note 21), which is then added to the silica pad. The pad is then flushed with ethyl acetate (320 mL) into a 1 L single-necked round-bottomed flask. The solvent is removed under reduced pressure (150-75 mmHg, 40 °C). The product is transferred, with the assistance of ethyl acetate washes (2 x 10 mL), to a 250 mL single-necked, round-bottomed flask and evaporated further (160 mmHg to 30 mmHg). The resultant white-yellowish solid is then broken up with a glass rod (Figure 4a). A 3 cm Teflon coated stir bar is added followed by ethanol (Note 22) (150 mL), and the flask is equipped with a water-cooled condenser. The flask is heated to reflux in an aluminium heating mantle and stirred for 25 min until complete dissolution to give a yellow solution. The flask is allowed to cool to room temperature and then placed in a freezer at -22 °C for 19 h. The resultant crystals were filtered off and washed with hexane (3 x 25 mL) (Note 23) to give fine off-white crystals (Figure 4b).

The crystals are transferred to a 100 mL single-necked flask and then toluene (30 mL) (Note 24) is added to give a slightly grey suspension (Figure 4c). The solvents are removed under reduced pressure (75 mmHg to 35 mmHg, 40 °C) and then the product is dried under vacuum (0.14 mmHg, 1 h, room temperature) to give a fine off white powder (Figure 4d) (Note 25). The powder is transferred to a 250 mL single-necked, round-bottomed flask (using 10 mL dichloromethane to rinse the flask) containing a 3 cm Teflon coated stir bar. Dichloromethane (80 mL) is added, the mixture is stirred for 10 min and then the yellow solution (Figure 4e) is filtered through cotton wool (Note 26), which is then washed with dichloromethane (4 x 10 mL), eluting under gravity into a 250 mL round-bottomed flask (Note 27). The solvent is evaporated (450 mmHg - 35 mmHg, 40 °C) to give a white solid (Figure 4f), which is broken up with a glass rod and then dried under vacuum (60 °C, 0.12 mmHg, 96 h) (6.67 g, 96%, >99% purity) (Notes 28, 29, 30, and 31).'''

ORGSYN_V95P0112_B_INFO = {
    'text': ORGSYN_V95P0112_B_TEXT,
    'name': 'orgsyn_v95p0112_b',
    'reagents': {
        'n-benzyl-4 methyl-N-(phenylethynyl)benzene-sulfonamide': {
            'quantities': ['4.69 g', '13.0 mmol'],
        },
        'dichloro(2-pyridinecarboxylato)gold': {
            'quantities': ['51.02 mg', '0.13 mmol'],
        },
        '((tert-butoxycarbonyl)glycyl)(pyridin-1-ium-1-yl)amide': {
            'quantities': ['3.60 g', '14.3 mmol', '1.1 equiv'],
        },
        'toluene': {
            'quantities': ['130 mL', '30 mL'],
        },
        'ethyl acetate': {
            'quantities': ['2 x 50 mL', '320 mL', '2 x 10 mL'],
        },
        'the resultant': {
            'quantities': [],
        },
        'ethanol': {
            'quantities': ['150 mL'],
        },
        'hexane': {
            'quantities': ['3 x 25 mL'],
        },
        'dichloromethane': {
            'quantities': ['80 mL', '4 x 10 mL'],
        },
    },
    'steps': [
        Dry,
        HeatChillToTemp,
        Add,
        Add,
        Add,
        Add,
        HeatChill,
        Wait,
        FilterThrough,
        FilterThrough,
        FilterThrough,
        Evaporate,
        Repeat,
        Evaporate,
        Add,
        HeatChillToTemp,
        Stir,
        HeatChillToTemp,
        HeatChill,
        Filter,
        WashSolid,
        Dry,
        Add,
        Evaporate,
        Dry,
        Add,
        Stir,
        FilterThrough,
        Evaporate,
        Dry,
    ],
    'vessels': [
        # Dry
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
        # Wait
        {},
        # FilterThrough
        {
            'from_vessel': 'reactor',
            'to_vessel': 'rotavap',
            'through': 'silica',
        },
        # FilterThrough
        {
            'from_vessel': 'rotavap',
            'to_vessel': 'rotavap',
            'through': 'silica',
        },
        # FilterThrough
        {
            'from_vessel': 'rotavap',
            'to_vessel': 'rotavap',
            'through': 'silica',
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
            ],
        },
        # Evaporate
        {
            'rotavap_name': 'rotavap',
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
        # HeatChillToTemp
        {
            'vessel': 'filter',
        },
        # Stir
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
        # Transfer
        {
            'from_vessel': 'filter',
            'to_vessel': 'rotavap',
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
        # Add
        {
            'vessel': 'rotavap',
        },
        # Stir
        {
            'vessel': 'rotavap',
        },
        # FilterThrough
        {
            'from_vessel': 'rotavap',
            'to_vessel': 'rotavap',
            'through': 'cotton wool',
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
        # Dry
        {
            'time': 60.0,
            'vacuum_pressure': 0.1599864,
        },
        # HeatChillToTemp
        {
            'temp': 25,
            'active': False,
            'continue_heatchill': False,
        },
        # Add
        {
            'reagent': 'n-benzyl-4 methyl-N-(phenylethynyl)benzene-sulfonamide',
            'mass': 4.69,
            'stir': False,
        },
        # Add
        {
            'reagent': 'dichloro(2-pyridinecarboxylato)gold',
            'mass': 0.05102,
            'stir': False,
        },
        # Add
        {
            'reagent': '((tert-butoxycarbonyl)glycyl)(pyridin-1-ium-1-yl)amide',
            'mass': 3.6,
            'stir': False,
        },
        # Add
        {
            'reagent': 'toluene',
            'volume': 130.0,
            'stir': False,
        },
        # HeatChill
        {
            'temp': 90.0,
            'time': 19800.0,
        },
        # Wait
        {
            'time': 3600.0,
        },
        # FilterThrough
        {
            'eluting_solvent': 'ethyl acetate',
            'eluting_volume': 50,
            'eluting_repeats': 2,
        },
        # FilterThrough
        {},
        # FilterThrough
        {
            'eluting_solvent': 'ethyl acetate',
            'eluting_volume': 320.0,
        },
        # Evaporate
        {
            'temp': 40.0,
            'pressure': 149.98725000000002,
            'time': 1800,
            'mode': 'auto',
        },
        # Repeat
        {
            'repeats': 2,
            'children': [
                # Add
                {
                    'reagent': 'ethyl acetate',
                    'volume': 10.0,
                    'stir': False,
                },

            ]
        },
        # Evaporate
        {
            'pressure': 126.6559,
            'time': 1800,
            'mode': 'auto',
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Add
        {
            'reagent': 'ethanol',
            'volume': 150.0,
            'stir': True,
        },
        # HeatChillToTemp
        {
            'temp': 78.5,
        },
        # Stir
        {
            'time': 1500.0,
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
            'time': 68400.0,
        },
        # Filter
        {
            'filter_vessel': 'filter',
        },
        # WashSolid
        {
            'solvent': 'hexane',
            'volume': 25.0,
            'repeat': 3,
        },
        # Dry
        {},
        # Transfer
        {
            'volume': 'all',
        },
        # Add
        {
            'reagent': 'toluene',
            'volume': 30.0,
            'stir': False,
        },
        # Evaporate
        {
            'temp': 40.0,
            'pressure': 73.3271,
            'time': 1800,
            'mode': 'auto',
        },
        # Dry
        {
            'vacuum_pressure': 0.18665080000000003,
        },
        # Add
        {
            'reagent': 'dichloromethane',
            'volume': 80.0,
            'stir': False,
        },
        # Stir
        {
            'time': 600.0,
        },
        # FilterThrough
        {
            'eluting_solvent': 'dichloromethane',
            'eluting_volume': 10.0,
            'eluting_repeats': 4,
        },
        # Evaporate
        {
            'temp': 40.0,
            'pressure': 46.6627,
            'time': 1800,
            'mode': 'auto',
        },
        # Dry
        {
            'time': 345600.0,
            'temp': 60.0,
            'vacuum_pressure': 0.1599864,
        },
    ],
}
