from typing import Dict, List, Tuple, Union
from xdl.chemputerxdl.steps import (
    Add,
    Dissolve,
    Separate,
    Filter,
    FilterThrough,
    WashSolid,
    Dry,
    HeatChill,
    HeatChillToTemp,
    StartHeatChill,
    StopHeatChill,
    Stir,
    StartStir,
    StopStir,
    Confirm,
    Evaporate,
    Transfer,
    RunColumn,
    Recrystallize,
    Sonicate,
    Distill,
    Evacuate
)
from xdl.steps.special_steps import Wait

#: Words that after an addition keyword signify that the addition should be
# performed slowly.
SLOW_ADDITION_WORDS: List[str] = [
    'carefully', 'slowly', 'portionwise', 'portions', 'syringe']

#: Words that after an addition keyword signify that the addition should be
# performed slowly.
DROPWISE_ADDITION_WORDS: List[str] = ['dropwise']

EVAPORATE_REMOVE_PHRASES: List[str] = ['under vacuum', 'in vacuo', 'in vacuum']

FAST_STIRRING_WORDS: List[str] = ['vigorous', 'vigorously']
SLOW_STIRRING_WORDS: List[str] = ['slowly', 'gently']

#: Words that signify reagent should be cold.
REAGENT_NAME_COLD_WORDS: Tuple[str] = ('cold ',)  # Don't delete this comma,
# tuple used in for loop

#: Words that signify reagent should be icecold
REAGENT_NAME_ICECOLD_WORDS: Tuple[str] = ('icecold ', 'ice-cold ', 'ice cold ',)

#: Default temp to add at if text says 'cold water was added'.
DEFAULT_COLD_REAGENT_TEMP: int = 10

#: Default temp to add at if text says 'ice cold water was added'.
DEFAULT_ICECOLD_REAGENT_TEMP: int = 2

#: Default temp to add at if text says 'warm water was added'.
DEFAULT_WARM_REAGENT_TEMP: int = 50

#: Default temp to add at if text says 'hot water was added'.
DEFAULT_HOT_REAGENT_TEMP: int = 80

#: Default liquid transfer speed for slow addition.
DEFAULT_SLOW_ADDITION_DISPENSE_SPEED: int = 10  # mL / min

#: Default liquid transfer speed for dropwise addition.
DEFAULT_DROPWISE_DISPENSE_SPEED: int = 3  # mL / min

#: Default aspiration speed for viscous liquids.
DEFAULT_VISCOUS_ASPIRATION_SPEED: int = 2  # mL / min

#: Default time to stir for if text says 'mixture was stirred thoroughly'.
DEFAULT_THOROUGH_STIR_TIME: int = 60 * 60  # s

#: Default time to dry if text says 'pressed as dry as possible'.
DEFAULT_AS_DRY_AS_POSSIBLE_DRYING_TIME: int = 3 * 60 * 60  # s

#: Maximum temperature jacketed filter can go to.
MAX_FILTER_TEMP: int = 200

#: Default time to cool for 'allowed to cool' if no time specified.
DEFAULT_ALLOWED_TO_COOL_TIME: int = 60 * 60 * 12

#: Default time limit for auto evaporation.
DEFAULT_AUTO_EVAPORATION_TIME_LIMIT: int = 60 * 30

#: Default time to stir for if no stirring time is given.
DEFAULT_STIRRING_TIME: int = 60 * 5

#: Default time for 'cooled briefly'.
DEFAULT_BRIEF_TIME: int = 60 * 5

#: Default volume to use for minimum volume of reagent
DEFAULT_MINIMUM_VOLUME: int = 10

#: Default solvent volume to use for separation if none given.
DEFAULT_SEPARATION_VOLUME: int = 25

DEFAULT_ANTICLOGGING_FILTER_ASPIRATION_SPEED: int = 2

#####################
### VESSEL SYSTEM ###
#####################

#: Link shortened vessel type names to full names needed in XDL.
COMPONENT_CLASS_NAME_DICT: Dict[str, str] = {
    'filter': 'ChemputerFilter',
    'reactor': 'ChemputerReactor',
    'separator': 'ChemputerSeparator',
    'rotavap': 'IKARV10',
}

#: For each steps a list of vessels that the reaction mixture moves through
# during the step, in order. For most steps it is just one vessel.
# Each vessel in chain is represented as
# (vessel_keyword_in_step_properties, resolution_rules)
# Possible resolution rules are:
#     next: Should be same as next vessel in vessel chain.
#     prev: Should be same as previous vessel in vessel chain.
#     filter: Must be filter vessel.
#     separator: Must be separator vessel.
#     rotavap: Must be rotavap vessel.
#     heatcool: Must have heating/cooling capabilities to temp defined in step.
STEP_VESSEL_CHAINS: Dict[type, List[List[Union[str, List[str]]]]] = {
    # Add resolution order chosen so that if an Add step causes crystallisation
    # the transfer to the filter vessel happens before the Add step.
    # i.e. Separate -> Add -> Filter, Add will resolve to Filter's filter_vessel.
    Add: [
        ['vessel', ['next', 'prev']],
    ],
    Separate: [
        ['from_vessel', 'prev'],
        ['separation_vessel', 'separator'],
        ['to_vessel', 'next'],
    ],
    Filter: [
        ['filter_vessel', 'filter'],
    ],
    FilterThrough: [
        ['from_vessel', 'prev'],
        ['to_vessel', 'next'],
    ],
    WashSolid: [
        ['vessel', ['prev']],
    ],
    Dry: [
        ['vessel', ['prev', 'next']],
    ],
    HeatChill: [
        ['vessel', ['heatcool', 'prev']],
    ],
    HeatChillToTemp: [
        ['vessel', ['heatcool', 'prev']],
    ],
    StartHeatChill: [
        ['vessel', 'prev', 'next'],
    ],
    StopHeatChill: [
        ['vessel', 'prev'],
    ],
    # Stir resolution order chosen as usually stuff is added then stirred, so
    # stir will be related to the steps before it.
    Stir: [
        ['vessel', 'prev'],
    ],
    StartStir: [
        ['vessel', ['prev', 'next']],
    ],
    StopStir: [
        ['vessel', ['prev', 'next']],
    ],
    Confirm: [],
    Wait: [],
    Evaporate: [
        ['rotavap_name', 'rotavap'],
    ],
    Transfer: [
        ['from_vessel', 'prev'],
        ['to_vessel', 'next'],
    ],
    Dissolve: [
        ['vessel', ['prev', 'next']],
    ],
    RunColumn: [
        ['from_vessel', 'prev'],
        ['to_vessel', 'next'],
    ],
    Recrystallize: [
        ['vessel', 'filter'],
    ],
    Sonicate: [],
    Distill: [],
    Evacuate: [
        ['vessel', ['next', 'prev']],
    ]
}

FINAL_TRY_STEP_VESSEL_CHAINS = {
    Stir: {'vessel': 'next'},
}

# Vessel types that are definite and don't require resolution.
DEFINITE_VESSELS: List[str] = [
    'separator', 'filter', 'rotavap', 'reactor', 'buffer_flask1']

#: Steps which inserted Transfer steps should come before.
TRANSFER_BEFORE_STEPS: List[type] = [StartHeatChill, StartStir]
