from typing import List
import copy
from ..utils import (
    apply_pattern,
    copy_and_modify_pattern,
    trim_patterns,
    Pos,
    Optional
)
from ..words import (
    Word,
    VesselWord,
    QuantityWord,
    VesselComponentWord,
    VesselComponentGroupWord,
    BathWord,
    NumberWord,
    TechniqueWord
)

VESSEL_PATTERNS = [
    ['round-bottom', 'flask'],
    ['round', 'bottom', 'flask'],
    ['round', 'bottom', 'flask'],
    ['round-bottomed', 'flask'],
    ['pressure', 'flask'],
    ['flask'],
    ['filter', 'flask'],
    ['buchner', 'funnel'],
    ['reaction', 'vessel'],
    ['hydrogenation', 'vessel'],
    ['separation', 'funnel'],
    ['rotary', 'evaporator'],
    ['separatory', 'funnel'],
    ['separating', 'funnel'],
    ['reactor'],
    ['system'],
]

VESSEL_DESCRIPTORS = [
    ['3-neck'],
    ['3-necked'],
    ['three-neck'],
    ['three-necked'],
    ['1-neck'],
    ['1-necked'],
    ['one-neck'],
    ['one-necked'],
]

# a, an, the, this etc...
for pattern in VESSEL_PATTERNS:
    pattern.insert(0, Optional(Pos('DT')))

VESSEL_PATTERNS = sorted(VESSEL_PATTERNS, key=lambda x: 1 / len(x))

COMPONENT_PATTERNS = [
    ['mechanical', 'stirrer'],
    ['magnetic', 'stirrer', 'bar'],
    ['stirrer', 'bar'],
    ['efficient', 'stirrer'],
    [Optional(Pos('JJ')), 'stirrer'],
    ['glass', Optional(Pos('JJ')), 'stirrer'],
    ['reflux', 'condenser'],
    ['condenser'],
    ['addition', 'funnel'],
    ['nitrogen', 'line'],
    ['filter', 'funnel'],
    ['glass', 'funnel'],
    ['medium', 'porosity', 'sintered', 'glass', 'funnel'],
    ['fine', 'porosity', 'sintered', 'glass', 'funnel'],
    ['dropping', 'funnel'],
    [Optional(Pos('JJ')), 'funnel'],
    ['funnel'],
    ['immersion', 'thermometer'],
    ['thermometer'],
    ['water', 'pump'],
    [Optional(Pos('JJ')), 'heating', 'mantle'],
    ['aluminium', 'heating', 'mantle'],
    ['aluminium', 'mantle'],
    [Optional(Pos('JJ')), 'mantle'],
    ['fritted', 'adapter'],
    ['liquid', 'nitrogen', 'cooled', 'probe'],
    ['cannula'],
    ['vacuum', 'pump'],
    [Optional('liquid'), Optional('nitrogen'), 'cold', 'trap'],
    ['cotton', 'wool'],
    [Optional(Pos('JJ')), 'helices'],
    [Optional(Pos('JJ')), 'side', 'arm'],
    ['rubber', 'stoppers'],
    [Optional(Pos('JJ')), 'septa'],
    [Optional(Pos('JJ')), 'septum'],
    ['balloon', 'of', 'argon', 'gas'],
    ['plug', Optional('of'), Optional(Pos('NN')), Optional(Pos('NN'))],
    [Optional(Pos('JJ')), 'arm'],
    [Optional(Pos('JJ')), 'spatula'],
    [Optional(Pos('JJ')), 'neck'],
    [Optional(Pos('JJ')), 'side', 'neck'],
    [Optional(Pos('JJ')), 'wool'],
    ['glass', 'wool'],
    ['cork'],
    [Optional(Pos('JJ')), 'rod'],
    ['glass', 'rod'],
    ['syringe'],
    ['syringe', 'pump'],
    [Optional(Pos('JJ')), 'pad'],
    [Optional(Pos('JJ')), 'pad', 'of', 'alumina'],
    ['silica', 'pad'],
    [Optional(Pos('JJ')), 'pad', 'of', 'silica', 'gel'],
    [Optional(Pos('JJ')), 'drying', 'tube'],
    ['water', 'aspirator'],
    [NumberWord, 'gauge', Optional(Pos('JJ')), 'wire'],
    [Optional(Pos('JJ')), 'wire'],
    ['thermostatically', 'controlled', 'stirrer-hotplate'],
    ['stirrer-hotplate'],
    ['stirrer', 'hotplate'],
    ['silica', 'gel', 'column'],
    [TechniqueWord, 'setup'],
    ['bunsen', 'flame'],
    ['bunsen', 'burner'],
    [Optional(Pos('JJ')), 'stopper'],
    ['heat', 'gun'],
    [Optional(Pos('JJ')), 'dam'],
    [Optional(Pos('JJ')), 'laboratory', 'steam', 'line'],
    [Optional(Pos('JJ')), 'steam', 'line'],
]

BATH_PATTERNS = [
    ['oil', 'bath'],
    ['water', 'bath'],
    ['room', 'temperature', 'water', 'bath'],
    ['ice', 'bath'],
    ['ice-water', 'bath'],
    ['ice-salt', 'bath'],
    ['bath', 'of', Optional(Pos('JJ')), 'water'],
    ['acetone/dry', 'ice', 'bath'],
    ['CH3CN-dry', 'ice', 'bath'],
]

BATH_PATTERNS = sorted(BATH_PATTERNS, key=lambda x: 1 / len(x))

for pattern in BATH_PATTERNS:
    pattern.insert(0, Optional(Pos('DT')))

extra_patterns = []
for pattern in COMPONENT_PATTERNS:
    extra_patterns.append(
        copy_and_modify_pattern(
            pattern=pattern,
            mod_index=0,
            mod_obj=QuantityWord,
            mode='insert'))
COMPONENT_PATTERNS.extend(extra_patterns)
extra_patterns = []
for item in COMPONENT_PATTERNS:
    for i in range(5):
        extra_pattern = copy.deepcopy(item)
        for _ in range(i):
            extra_pattern.insert(0, Optional(Pos('JJ')))
        extra_patterns.append(extra_pattern)
COMPONENT_PATTERNS.extend(extra_patterns)

# handle 'a stirrer bar'
extra_patterns = []
for pattern in COMPONENT_PATTERNS:
    for item in ['a', 'an', 'the']:
        extra_patterns.append(
            copy_and_modify_pattern(
                pattern=pattern,
                mod_index=0,
                mod_obj=item,
                mode='insert'))
COMPONENT_PATTERNS.extend(extra_patterns)
COMPONENT_PATTERNS = sorted(COMPONENT_PATTERNS, key=lambda x: 1 / len(
    [item for item in x if type(item) not in [int, Optional]]))

COMPONENT_GROUP_PATTERNS = [
    [VesselComponentWord],
    [VesselComponentWord, Optional(','), 'and', VesselComponentWord],
    [VesselComponentWord, ',', VesselComponentWord,
        Optional(','), 'and', VesselComponentWord],
    [VesselComponentWord, ',', VesselComponentWord, ',',
        VesselComponentWord, Optional(','), 'and', VesselComponentWord],
]

COMPONENT_GROUP_PATTERNS = sorted(
    COMPONENT_GROUP_PATTERNS, key=lambda x: 1 / len(x))

def vessel_tag(sentences: List[List[Word]], word_bank) -> List[List[Word]]:
    """Find vessels in sentences and return sentences with VesselWords.

    Args:
        sentences (List[List[Word]]): Sentences after tokenization.

    Returns:
        List[List[Word]]: Sentences with vessel phrases combined into
            VesselWords.
    """
    for pattern in trim_patterns(VESSEL_PATTERNS, word_bank):
        apply_pattern(pattern, VesselWord, sentences)
    for pattern in trim_patterns(COMPONENT_PATTERNS, word_bank):
        apply_pattern(pattern, VesselComponentWord, sentences)
    for pattern in trim_patterns(BATH_PATTERNS, word_bank):
        apply_pattern(pattern, BathWord, sentences)

    # A 5l flask
    apply_pattern([Pos('DT'), QuantityWord, VesselWord], VesselWord, sentences)
    apply_pattern([Pos('DT'), QuantityWord, VesselComponentWord],
                  VesselComponentWord, sentences)

    return sentences

def vessel_component_group_tag(sentences):
    for pattern in COMPONENT_GROUP_PATTERNS:
        apply_pattern(pattern, VesselComponentGroupWord, sentences)
    return sentences

def expand_vessels(sentences):
    """If vessel preceded by adjectives, combine these into longer word."""
    for sentence in sentences:
        i = len(sentence) - 1
        while i >= 0:
            word = sentence[i]
            if type(word) == VesselWord:
                j = i - 1
                while j >= 0:
                    if (str(sentence[j]) in VESSEL_DESCRIPTORS + [',']
                        or isinstance(sentence[j], QuantityWord)
                            or (type(sentence[j]) == Word
                                and sentence[j].pos == 'JJ')):
                        j -= 1
                    else:
                        break
                if j < i - 1:
                    sentence[i] = VesselWord(sentence[j:i] + word.words)
                    del sentence[j:i]
                    i = j
            i -= 1
    return sentences
