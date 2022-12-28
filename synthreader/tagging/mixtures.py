from typing import List, Union, Type
from ..words import (
    Word,
    RatioWord,
    MixtureWord,
    AbstractReagentWord,
)
from ..utils import apply_pattern, Optional, Pos

MIXTURE_PATTERNS: List[List[Union[str, Type[Word]]]] = [
    [Pos('DT'), Optional(Pos('JJ')), 'mixture', 'of', AbstractReagentWord],
    [Pos('DT'), Optional(Pos('JJ')), Optional(RatioWord), 'mixture',
     'of', AbstractReagentWord, 'and', AbstractReagentWord],
]

MIXTURE_PATTERNS = sorted(MIXTURE_PATTERNS, key=lambda x: 1 / len(x))

def mixture_tag(sentences: List[List[Word]]) -> List[List[Word]]:
    """Find mixture phrases in sentences and return sentences with MixtureWords.

    Args:
        sentences (List[List[Word]]): Sentences after reagent tagging.

    Returns:
        List[List[Word]]: Sentences with mixture phrases combined into
            MixtureWords.
    """
    for pattern in MIXTURE_PATTERNS:
        apply_pattern(pattern, MixtureWord, sentences)
    return sentences
