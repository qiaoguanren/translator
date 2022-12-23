from typing import List
import copy

from ..words import (
    Word,
    ReagentGroupWord,
    AbstractReagentWord,
    ReagentPlaceholderWord,
    QuantityWord,
    AuxiliaryVerbWord
)
from ..words.action_words import ActionWord
from ..utils import apply_pattern
from ..utils.pattern_matcher import Optional, Pos

REAGENT_GROUP_PATTERNS = [
    [AbstractReagentWord, ',', AbstractReagentWord],
    [AbstractReagentWord, ',', AbstractReagentWord, ',', AbstractReagentWord],
    [AbstractReagentWord, ',', AbstractReagentWord, ',',
        AbstractReagentWord, ',', AbstractReagentWord],
    [AbstractReagentWord, ',', 'followed', 'by',
        AbstractReagentWord, Optional(',')],
]
for i in range(6):
    pattern = [AbstractReagentWord, Optional(
        ','), 'and', Optional('a'), AbstractReagentWord]
    for _ in range(i):
        pattern.insert(0, ',')
        pattern.insert(0, AbstractReagentWord)
    REAGENT_GROUP_PATTERNS.append(pattern)

extra_patterns = []
for pattern in REAGENT_GROUP_PATTERNS:
    extra_pattern = copy.deepcopy(pattern)
    extra_pattern.insert(-1, 'then')
    extra_patterns.append(extra_pattern)

REAGENT_GROUP_PATTERNS.extend(extra_patterns)
REAGENT_GROUP_PATTERNS.extend([
    [QuantityWord, 'of', AbstractReagentWord],
])

for pattern in REAGENT_GROUP_PATTERNS:
    pattern.insert(0, Optional('remaining'))
    pattern.insert(0, Optional(Pos('DT')))

REAGENT_GROUP_PATTERNS = sorted(
    REAGENT_GROUP_PATTERNS, key=lambda x: 1 / len(x))
FOLLOWED_BY_PATTERNS = []
for i in reversed(range(len(REAGENT_GROUP_PATTERNS))):
    if 'followed' in REAGENT_GROUP_PATTERNS[i]:
        FOLLOWED_BY_PATTERNS.insert(0, REAGENT_GROUP_PATTERNS.pop(i))

def reagent_group_tag(sentences: List[List[Word]]) -> List[List[Word]]:
    """Find reagent groups in sentences and return sentences with
    ReagentGroupWords.

    Args:
        sentences (List[List[Word]]): Sentences after reagent group tagging.

    Returns:
        List[List[Word]]: Sentences with reagent group phrases combined into
            ReagentGroupWord objects.
    """
    for pattern in REAGENT_GROUP_PATTERNS:
        sentences = apply_pattern(pattern, ReagentGroupWord, sentences)
    for pattern in FOLLOWED_BY_PATTERNS:
        apply_pattern(pattern, ReagentGroupWord, sentences)
    do_not_allow_reagent_placeholders_in_group(sentences)
    split_reagent_groups(sentences)
    return sentences

def split_reagent_groups(sentences):
    for sentence in sentences:
        action_passed = False
        and_passed = False
        i = 0
        while i < len(sentence):
            word = sentence[i]
            if isinstance(word, ActionWord):
                action_passed = True
            if str(word) == 'and':
                and_passed = True
            if (action_passed
                and not and_passed
                and type(word) == ReagentGroupWord
                    and len(word.reagents) == 2):

                if (i + 1 < len(sentence)
                    and type(sentence[i + 1]) == AuxiliaryVerbWord
                    and i + 2 < len(sentence)
                        and isinstance(sentence[i + 2], ActionWord)):
                    reagents = word.reagents
                    sentence.pop(i)
                    sentence.insert(i, reagents[1])
                    sentence.insert(i, Word('and'))
                    sentence.insert(i, reagents[0])
                    i += 2
            i += 1
    return sentences

def do_not_allow_reagent_placeholders_in_group(sentences):
    # Don't allow nested ReagentGroupWords e.g.

    # 'The isothiourea (3.9 g, 0.02 mole) was dissolved in ethanol and
    # hydrazine hydrate (5 ml) and the mixture heated under reflux for 3 h.'

    # This sentence shouldn't have 'ethanol and hydrazine hydrate (5 ml) and the
    # mixture'
    # tagged as a ReagentGroupWord
    for sentence in sentences:
        i = 0
        while i < len(sentence):
            word = sentence[i]
            if type(word) == ReagentGroupWord:
                if any(
                    [type(subword) in [ReagentGroupWord, ReagentPlaceholderWord]
                     for subword in word.words]):
                    words = word.words
                    del sentence[i]
                    for subword in reversed(words):
                        sentence.insert(i, subword)
                    i = i + len(words)
                else:
                    i += 1
            else:
                i += 1
    return sentences
