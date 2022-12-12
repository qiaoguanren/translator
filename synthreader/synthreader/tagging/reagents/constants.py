REAGENT_NAME_STRIPS = [
    ', ', ',', ' ,'
]

REAGENT_NAME_IGNORE_LIST = [
    'was',
    'by',
    'in',
    'with',
    'to',
    'of',
    'ASOLUTIONOF',
    'ANAQUEOUSSOLUTIONOF',
    'containing',
    'portion',
    'portions',
]

REAGENT_NAME_INCLUDE_LIST = [
    'conc',
    'concentrated',
    'methyl',
    'ethyl',
    'propyl',
    'butyl',
    'hydride',
    'hydroxide',
    'hydrate',
    'anhydride',
    'chloride',
    'iodide',
    'bromide',
    'saturated',
    'aqueous',
]

REAGENT_NLP_TAGS = (
    'VBD', 'VBG', 'RB', 'J', 'N', 'REAGENT',
)

REAGENT_CHAR_IGNORE_LIST = [
    ' ', 'a', 'A',
]
