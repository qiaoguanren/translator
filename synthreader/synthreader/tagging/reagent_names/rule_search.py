from typing import List, Tuple, Callable
import re

from .utils import (
    apply_reagent_names, remove_sub_phrases, resolve_overlapping_phrases)
from ...words import Word

def caps_after_first_letter(
        sentences: List[List[Word]]) -> List[Tuple[int, int, int]]:
    """Any word with length greater than 2 and capital letters after the
    first letter is a reagent name, e.g. DCM, DEAD, EtOAc, BuLi etc...

    Args:
        sentences (List[List[Word]]): Sentences to get positions of reagent
            names.

    Returns:
        List[Tuple[int, int, int]]: List of position in sentences where reagent
            names have been found. [(sentence_i, start_word_i, end_word_i)...]
    """
    pos = []
    for i, sentence in enumerate(sentences):
        for j, word in enumerate(sentence):
            if type(word) == Word:
                if len(str(word)) > 2 and re.search('[A-Z]', str(word)[1:]):
                    pos.append((i, j, j + 1))
    return pos


REAGENT_NAME_RULES: List[Callable] = [
    caps_after_first_letter,
]

def rule_reagent_name_tag(sentences: List[List[Word]]) -> List[List[Word]]:
    """Tag reagent names based on logical rules for what kind of words are
    reagent names.

    Args:
        sentences (List[List[Word]]): Sentences to tag with reagent names.

    Returns:
        List[List[Word]]: Sentences with reagent names tagged.
    """
    pos = []
    for rule in REAGENT_NAME_RULES:
        pos.extend(rule(sentences))
    pos = remove_sub_phrases(pos)
    pos = resolve_overlapping_phrases(pos)
    apply_reagent_names(sentences, pos)
    return sentences
