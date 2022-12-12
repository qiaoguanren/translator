from typing import List
from .constants import (
    PAST_ACTION_PATTERNS, PRESENT_ACTION_PATTERNS, DISCONTINUE_ACTION_PATTERNS)
from ...words import Word, DiscontinueWord
from ...utils import apply_pattern, trim_patterns

def past_tense_action_tag(
        sentences: List[List[Word]], word_bank) -> List[List[Word]]:
    """Find past tense actions in sentences i.e. 'stirred' and return sentences
    with ActionWords.

    Args:
        sentences (List[List[Word]]): Sentences after tokenization.

    Returns:
        List[List[Word]]: Sentences with action phrases combined into
            ActionWords.
    """
    for pattern in trim_patterns(PAST_ACTION_PATTERNS, word_bank):
        apply_pattern(pattern[0], pattern[1], sentences)
    # Need this not to mess up the combined organic extracts
    for sentence in sentences:
        for i in range(1, len(sentence)):
            if (str(sentence[i]) == 'combined' and i - 1 >= 0
                    and str(sentence[i - 1]).lower() == 'the'):
                sentence[i] = Word('combined', 'JJ')
    return sentences

def present_tense_action_tag(
        sentences: List[List[Word]], word_bank) -> List[List[Word]]:
    """Find  present tense actions, i.e. 'stirring' in sentences and return
    sentences with ActionWords.

    Args:
        sentences (List[List[Word]]): Sentences after tokenization.

    Returns:
        List[List[Word]]: Sentences with action phrases combined into
            ActionWords.
    """
    for pattern in trim_patterns(PRESENT_ACTION_PATTERNS, word_bank):
        apply_pattern(pattern[0], pattern[1], sentences)
    return sentences

def discontinue_action_tag(sentences: List[List[Word]]) -> List[List[Word]]:
    for pattern in DISCONTINUE_ACTION_PATTERNS:
        apply_pattern(pattern, DiscontinueWord, sentences)
    return sentences
