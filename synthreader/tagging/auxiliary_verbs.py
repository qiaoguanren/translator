from typing import List
from ..words import Word, AuxiliaryVerbWord
from ..utils import apply_pattern

AUXILIARY_VERB_PATTERNS: List[List[str]] = [
    ['was'],
    ['were'],
    ['is'],
    ['are'],
    ['should', 'be'],
    ['can', 'be'],
]

def auxiliary_verb_tag(sentences: List[List[Word]]) -> List[List[Word]]:
    """Find auxiliary verbs in sentences and return sentences with
    AuxiliaryVerbWords.

    Args:
        sentences (List[List[Word]]): Sentences for tagging.

    Returns:
        List[List[Word]]: Sentences with auxiliary verbs converted into
            AuxiliaryVerbWords.
    """
    for pattern in AUXILIARY_VERB_PATTERNS:
        apply_pattern(pattern, AuxiliaryVerbWord, sentences)
    return sentences
