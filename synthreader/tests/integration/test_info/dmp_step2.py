from chemputerxdl.steps import *
from xdl.steps import *

DMP_STEP2_TEXT = '''A 1-L, three-necked, round-bottomed flask, equipped for magnetic stirring and
fitted with an immersion thermometer, is charged with 56 g of the moist solid
iodinane oxide, 96 mL of glacial acetic acid, and 192 mL of acetic anhydride
(Note 11). The flask is flushed with dry argon, and maintained under a dry argon
atmosphere. Magnetic stirring is commenced, and the mixture is heated to 85°C
(internal temperature) over 30 min by means of an oil bath, and kept at this
temperature until all the solids dissolve (~20 min) to afford a colorless to
clear yellow solution (Note 12). Heating and stirring are discontinued and the
reaction mixture is allowed to cool slowly to room temperature in the oil bath
for 24 hr. A large quantity of colorless crystals separate during this time (Note 13).
The resulting crystalline solids are isolated by careful vacuum filtration in the
reaction vessel under argon using a fritted adapter followed by washing the solids
with three 80-mL portions of anhydrous ether and subsequent vacuum filtration in
the reaction vessel as above (Note 14), (Note 15).
'''

DMP_STEP2_INFO = {
    'name': 'dmp_step2',
    'text': DMP_STEP2_TEXT,
    'reagents': {
        'the moist solid iodinane oxide': {
            'quantities': ['56 g'],
        },
        'glacial acetic acid': {
            'quantities': ['96 mL'],
        },
        'acetic anhydride': {
            'quantities': ['192 mL'],
        },
        'anhydrous ether': {
            'quantities': ['80 mL'],
        },
    },
    'steps': [
        Add,
        Add,
        Add,
        HeatChillToTemp,
        Stir,
        StopStir,
        StopHeatChill,
        Wait,
        Filter,
        WashSolid,
        Dry
    ],
    'vessels': [
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
        {},
        {'filter_vessel': 'filter'},
        {'vessel': 'filter'},
        {'vessel': 'filter'},
    ]
}
