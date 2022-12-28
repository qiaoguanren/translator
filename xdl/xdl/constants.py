from typing import List

#: XDL version number. Remember to increment after merging into master. Used
# in header at top of outputted XDL files.
XDL_VERSION: str = '0.4.6'

########
# MISC #
########

#: Valid platforms for XDL
VALID_PLATFORMS: List[str] = ['chemputer', 'chemobot']

#: Chemicals that will be recognised as inert gas.
INERT_GAS_SYNONYMS: List[str] = ['nitrogen', 'n2', 'ar', 'argon']


#: Chemical name if found in graph to used as air source.
AIR: str = 'air'

#: Default duration for base steps when the command is basically instantaneous
DEFAULT_INSTANT_DURATION = 1  # s

#: Room temperature in °C
ROOM_TEMPERATURE: int = 25

#: Keywords that if found in reagent name signify that the reagent is aqueous.
AQUEOUS_KEYWORDS: List[str] = ['water', 'aqueous', 'acid', ' m ', 'hydroxide']

#: Attributes of the <Synthesis> element.
SYNTHESIS_ATTRS = [
    {
        'name': 'graph_sha256',
        'type': str,
        'default': '',
    }
]

# Prop type if property should be reagent declared in Reagent section
REAGENT_PROP_TYPE = 'reagent'

# Prop type if property should be vessel declared in Hardware section
VESSEL_PROP_TYPE = 'vessel'
