from typing import List, Union, Type
import copy

from ..words import (
    Word,
    ReagentWord,
    SolutionWord,
    ReagentGroupWord,
    StirWord,
    AddWord,
    PercentWord,
    ConcWord,
)
from ..utils import apply_pattern, Optional, Pos

#: Patterns to match solution phrasees.
SOLUTION_PATTERNS: List[List[Union[str, Type[Word]]]] = [
    ['a', Optional(Pos('JJ')), 'solution', 'of',
     ReagentWord, 'in', ReagentWord],
    ['a', Optional(Pos('JJ')), 'solution', 'of',
     ReagentGroupWord, 'in', ReagentWord],
    ['a', Optional(Pos('JJ')), 'solution', 'of', ReagentGroupWord],
    ['a', Optional(Pos('JJ')), 'solution', 'of', ReagentWord],
    ['a', PercentWord, 'solution', 'of', ReagentWord],
    ['a', PercentWord, 'solution', 'of', ReagentWord, 'in', ReagentWord],
    ['a', ConcWord, 'solution', 'of', ReagentWord],
    ['a', ConcWord, 'solution', 'of', ReagentWord, 'in', ReagentWord],

    ['an', 'aqueous', 'solution', 'of', ReagentWord],
    ['an', 'aqueous', 'solution', 'of', ReagentGroupWord],
    [ReagentWord, 'in', ReagentWord],
    [ReagentGroupWord, 'in', ReagentWord],
    [ReagentWord, Optional(','), AddWord, 'in', ReagentWord],
    ['a', ReagentWord, 'of', ReagentWord],
    ['a', PercentWord, 'aqueous', 'solution', 'of', ReagentWord],
    ['a', ConcWord, 'aqueous', 'solution', 'of', ReagentWord],
    ['a', ConcWord, 'aqueous', 'solution', ReagentWord],
    ['an', 'aqueous', 'solution', 'of', ReagentWord],
]

# Add patterns to support 'a hot solution of...' or 'a cold solution of...'
extra_patterns = []
for pattern in SOLUTION_PATTERNS:
    hot_extra_pattern = copy.deepcopy(pattern)
    cold_extra_pattern = copy.deepcopy(pattern)
    stirred_extra_pattern = copy.deepcopy(pattern)
    stirring_extra_pattern = copy.deepcopy(pattern)
    viscous_extra_pattern = copy.deepcopy(pattern)

    if pattern[0] in ['a', 'an']:
        viscous_extra_pattern.insert(1, Optional('viscous'))
        del viscous_extra_pattern[0]
        extra_patterns.append(viscous_extra_pattern)

    for i, word in enumerate(pattern):
        if word == 'solution':
            hot_extra_pattern.insert(i, 'hot')
            cold_extra_pattern.insert(i, 'cold')
            stirred_extra_pattern.insert(i, StirWord)
            stirring_extra_pattern.insert(i, 'stirring')
            extra_patterns.extend([
                hot_extra_pattern,
                cold_extra_pattern,
                stirred_extra_pattern,
                stirring_extra_pattern,
            ])
            break
SOLUTION_PATTERNS.extend(extra_patterns)

SOLUTION_PATTERNS = sorted(SOLUTION_PATTERNS, key=lambda x: 1 / len(x))

def solution_tag(sentences: List[List[Word]]) -> List[List[Word]]:
    """Find solutions in sentences and return sentences with SolutionWords.

    Args:
        sentences (List[List[Word]]): Sentences after reagent tagging.

    Returns:
        List[List[Word]]: Sentences with solution phrases combined into
            SolutionWords.
    """
    for pattern in SOLUTION_PATTERNS:
        sentences = apply_pattern(pattern, SolutionWord, sentences)
    return sentences
