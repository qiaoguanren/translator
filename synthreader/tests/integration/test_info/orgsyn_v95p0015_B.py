from chemputerxdl.steps import *
from xdl.steps import *

ORGSYN_V95P0015_B_TEXT = '''A two-necked (B24, diameter: 8 cm) 250 mL round-bottomed flask is open to air, equipped with an egg shaped magnetic stirring bar (2.5 x 1.0 cm) and a thermometer (-10 °C - 250 °C), and charged with toluene (80 mL) (Note 5). N-Hydroxy-N-phenylacetamide (4) (6.046 g, 40.0 mmol), 1-hexyne (5) (6.50 mL, 4.60 g, 56.0 mmol, 1.4 equiv), zinc trifluoromethanesulfonate (0.731 g, 2.0 mmol, 0.05 equiv), chloro[tris(2,4-di-tert-butylphenyl)phosphite]gold (I) (3) (176 mg, 0.2 mmol, 0.005 equiv), and silver bis(trifluoromethanesulfonyl)imide (78 mg, 0.2 mmol, 0.005 equiv) are successively added (Note 6). The color of the solution changes from colorless to yellow upon the addition of silver bis(trifluoromethanesulfonyl)imide into the solution, while white silver chloride precipitation is observed. (Figure 3)
Both necks of the flask are fitted with septa. The reaction mixture is heated in a 60 °C oil bath and stirred for 24 h. During its course, the reaction turns progressively from yellow to orange and finally to black (Figure 4).

A 150 mL Büchner funnel with fritted disc (diameter: 7 cm) is mounted on the top of a 250 mL one-necked round-bottomed flask and charged with 10.5 g celite (Note 7). While the funnel is connected to a vacuum source (375 mmHg), THF (10 mL) (Note 8) is poured into the funnel, followed by the reaction mixture, and THF (2 x 10 mL) (Note 8). The filtrate is washed with 50 mL saturated sodium bicarbonate solution (Note 9), and the aqueous solution is extracted with dichloromethane (3 x 10 mL) (Note 10). The combined organic layers are dried for 20 min over Na2SO4 (15 g) (Note 11). The volatiles are removed by rotatory evaporation (30 mmHg, 40 °C bath temperature), and then under a higher vacuum for 4 h (1 mmHg) (Note 12). The resulting solid is dissolved in dichloromethane (20 mL) (Note 10), and 10 g silica gel (Note 13) is added into the solution. After removing the solvent by rotatory evaporation (300 mmHg, 30 °C bath temperature), the silica gel with adsorbed crude material is charged on a silica gel (Note 13) column (5 cm diameter x 15 cm height). The column is packed with hexanes (800 mL) and eluted with hexanes/ethyl acetate (20/1, 1.3 L) using compressed air (2 atm) (Notes 14 and 15). Fractions 42-58 (Note 16) containing the pure product are concentrated by rotary evaporation (45 mmHg, 30 °C bath temperature). The resultant solid is dried under high vacuum (1.0 mmHg) for 10 h to afford indole 6 (7.77 g, 90% yield) as a white solid (Note 17) (Figure 5).'''

ORGSYN_V95P0015_B_INFO = {
    'text': ORGSYN_V95P0015_B_TEXT,
    'name': 'orgsyn_v95p0015_b',
    'reagents': {
        'toluene': {
            'quantities': ['80 mL'],
        },
        'N-Hydroxy-N-phenylacetamide': {
            'quantities': ['6.046 g', '40.0 mmol'],
        },
        '1 hexyne': {
            'quantities': ['6.50 mL', '4.60 g', '56.0 mmol', '1.4 equiv'],
        },
        'zinc trifluoromethanesulfonate': {
            'quantities': ['0.731 g', '2.0 mmol', '0.05 equiv'],
        },
        'chloro [ tris(2,4-di-tert-butylphenyl)phosphite ] gold(I)': {
            'quantities': ['176 mg', '0.2 mmol', '0.005 equiv'],
        },
        'silver bis(trifluoromethanesulfonyl)imide': {
            'quantities': ['78 mg', '0.2 mmol', '0.005 equiv'],
        },
        'the color': {
            'quantities': [],
        },
        'while white silver chloride': {
            'quantities': [],
        },
        'THF': {
            'quantities': ['10 mL', '2 x 10 mL'],
        },
        'saturated sodium bicarbonate solution': {
            'quantities': ['50 mL'],
        },
        'dichloromethane': {
            'quantities': ['3 x 10 mL', '20 mL'],
        },
        'Na2SO4': {
            'quantities': ['15 g'],
        },
        'silica gel': {
            'quantities': ['10 g'],
        },
        'the silica gel': {
            'quantities': [],
        },
        'hexanes': {
            'quantities': ['800 mL'],
        },
        'hexanes/ethyl acetate': {
            'quantities': ['1.3 L'],
        },
        'the resultant solid': {
            'quantities': [],
        },
        'indole 6': {
            'quantities': [],
        },
    },
    'steps': [
        Add,
        Add,
        Add,
        Add,
        Add,
        Add,
        HeatChillToTemp,
        Stir,
        Add,
        Repeat,
        Separate,
        Separate,
        Evaporate,
        Dry,
        Dissolve,
        Add,
        Evaporate,
        RunColumn,
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
        # Stir
        {
            'vessel': 'reactor',
        },
        # Add
        {
            'vessel': 'reactor',
        },
        # Repeat
        {
            'children': [
                # Add
                {
                    'vessel': 'reactor',
                }
            ]
        },
        # Separate
        {
            'from_vessel': 'reactor',
            'separation_vessel': 'separator',
            'to_vessel': 'rotavap',
            'waste_phase_to_vessel': 'separator',
        },
        # Separate
        {
            'from_vessel': 'separator',
            'separation_vessel': 'separator',
            'to_vessel': 'rotavap',
        },
        # Evaporate
        {
            'rotavap_name': 'rotavap',
        },
        # Dry
        {
            'vessel': 'rotavap',
        },
        # Dissolve
        {
            'vessel': 'rotavap',
        },
        # Add
        {
            'vessel': 'rotavap',
        },
        # Evaporate
        {
            'rotavap_name': 'rotavap',
        },
        # RunColumn
        {
            'from_vessel': 'rotavap',
            'to_vessel': 'rotavap',
            'column': 'column',
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
            'reagent': 'toluene',
            'volume': 80.0,
            'stir': False,
        },
        # Add
        {
            'reagent': 'N-Hydroxy-N-phenylacetamide',
            'mass': 6.046,
            'stir': True,
        },
        # Add
        {
            'reagent': '1 hexyne',
            'volume': 6.5,
            'stir': True,
        },
        # Add
        {
            'reagent': 'zinc trifluoromethanesulfonate',
            'mass': 0.731,
            'stir': True,
        },
        # Add
        {
            'reagent': 'chloro [ tris(2,4-di-tert-butylphenyl)phosphite ] gold(I)',
            'mass': 0.176,
            'stir': True,
        },
        # Add
        {
            'reagent': 'silver bis(trifluoromethanesulfonyl)imide',
            'mass': 0.078,
            'stir': True,
        },
        # HeatChillToTemp
        {
            'temp': 60.0,
        },
        # Stir
        {
            'time': 86400.0,
        },
        # Add
        {
            'reagent': 'THF',
            'volume': 10.0,
            'stir': True,
        },
        # Repeat
        {
            'repeats': 2,
            'children': [
                # Add
                {
                    'reagent': 'THF',
                    'volume': 10.0,
                    'stir': True,
                },
            ]
        },
        # Separate
        {
            'purpose': 'wash',
            'product_bottom': False,
            'solvent': 'saturated sodium bicarbonate solution',
            'solvent_volume': 50.0,
            'n_separations': 1,
            'through': 'Na2SO4'
        },
        # Separate
        {
            'purpose': 'extract',
            'product_bottom': True,
            'solvent': 'dichloromethane',
            'solvent_volume': 10.0,
            'n_separations': 3,
            'through': 'Na2SO4'
        },
        # Evaporate
        {
            'temp': 40.0,
            'pressure': 39.9966,
            'time': 1800,
            'mode': 'auto',
        },
        # Dry
        {
            'time': 14400.0,
            'vacuum_pressure': 1.33322,
        },
        # Dissolve
        {
            'solvent': 'dichloromethane',
            'volume': 20.0,
        },
        # Add
        {
            'reagent': 'silica gel',
            'mass': 10.0,
            'stir': True,
        },
        # Evaporate
        {
            'temp': 30.0,
            'pressure': 399.966,
            'time': 1800,
            'mode': 'auto',
        },
        # RunColumn
        {},
        # Evaporate
        {
            'temp': 30.0,
            'pressure': 59.9949,
            'time': 1800,
            'mode': 'auto',
        },
        # Dry
        {
            'time': 36000.0,
            'vacuum_pressure': 1.33322,
        },
    ],
}
