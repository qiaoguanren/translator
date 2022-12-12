from chemputerxdl.steps import *
from xdl.steps import *

CSSP17_TEXT = '''Use Schlenk techniques. Dry acetonitrile (700 ml) is added to a mixture of NbCl5 (50 g, Aldrich) and coarse aluminium powder (8 g) in a 2 l round bottom flask fitted with a stopcocked side-arm and a seriously big magnetic follower. An overhead stirrer could be used, but make sure there are no leaks. The suspension is stirred vigorously. After a brief induction period the yellow solution becomes very warm and should be cooled briefly in ice water (have this on hand). Don't chill the mixture as the reation may just stop. The solution turns red. After 3 h the solution is filtered through a bed of celite on an inert gas frit. [The Al powder remaining can be pyrophoric so exercise caution in its disposal). The solvent is removed under vacuum into a liquid nitrogen cooled trap on a Schlenk line. This gives a red crystalline solid that is allegedly NbCl4(CH3CN)3. Addition of THF (750 ml) followed by stirring overnight gives a YELLOW (mustard) solid and a red solution. The solid is isolated using vacuum filtration and washed with THF until the solution runs yellow or nearly colourless. The solid now needs to be dried in vacuo, but it contains a lot of "free" THF so exercise caution. The process will take some time and you will probably need to get in there with a spatula to break up the lumps. Once it is dry the solid is free-flowing. Yield 50 g (70%) of NbCl4(THF)2.'''

CSSP17_INFO = {
    'text': CSSP17_TEXT,
    'name': 'cssp17',
    'reagents': {
        'dry acetonitrile': {
            'quantities': ['700 ml'],
        },
        'water': {
            'quantities': [],
        },
        'THF': {
            'quantities': ['750 ml'],
        },
        'NbCl4(THF)2 (70 %)': {
            'quantities': ['50 g', '70 %'],
        },
    },
    'steps': [
        Add,
        Add,
        Stir,
        HeatChill,
        Wait,
        FilterThrough,
        Evaporate,
        Add,
        Stir,
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
        # Stir
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
        },
        # Evaporate
        {
            'rotavap_name': 'rotavap',
        },
        # Add
        {
            'vessel': 'rotavap',
        },
        # Stir
        {
            'vessel': 'rotavap',
        },
        # Transfer
        {
            'from_vessel': 'rotavap',
            'to_vessel': 'filter',
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
            'reagent': 'a mixture of NbCl5 ( 50 g , Aldrich ) and coarse aluminium powder ( 8 g )',
        },
        # Add
        {
            'reagent': 'dry acetonitrile',
            'volume': 700.0,
        },
        # Stir
        {
            'time': 300.0,
            'stir_speed': 600,
        },
        # HeatChill
        {
            'temp': 25.0,
            'time': 300.0,
        },
        # Wait
        {
            'time': 10800.0,
        },
        # FilterThrough
        {
            'through': 'celite',
        },
        # Evaporate
        {
            'temp': 50,
            'pressure': 153.0,
            'time': 1800,
            'mode': 'auto',
        },
        # Add
        {
            'reagent': 'THF',
            'volume': 750.0,
        },
        # Stir
        {
            'time': 57600.0,
        },
        # Transfer
        {
            'volume': 'all',
        },
        # Filter
        {
            'filter_vessel': 'filter',
        },
        # WashSolid
        {
            'solvent': 'THF',
            'repeat': 1,
        },
        # Dry
        {},
    ],
}
