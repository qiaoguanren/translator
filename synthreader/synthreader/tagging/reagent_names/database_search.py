from typing import List
from chemdata.synonyms import REAGENT_NAME_LIST
from .utils import (
    get_candidate_phrases,
    remove_sub_phrases,
    resolve_overlapping_phrases,
    apply_reagent_names
)
from .constants import MAX_REAGENT_NAME_LENGTH
from ...words import Word

REAGENT_NAME_LIST.extend([
    'alcohol',
    'DI water',
    'cracked ice',
    'ice-water',
])

def get_known_reagent_names(max_length: int) -> List[str]:
    """Return list of known reagent names. Currently this as a separate function
    is overkill, but not if you wanted to pull names from a big database.

    Args:
        max_length (int): Maximum number of characters in allowed in reagent
            name.

    Returns:
        List[str]: List of known reagent names.
    """
    return REAGENT_NAME_LIST

def database_reagent_name_tag(sentences: List[List[Word]]) -> List[List[Word]]:
    """Search for known reagent names in text and tag them as ReagentNameWords.

    Args:
        sentences (List[List[Word]]): Sentences to search for reagent names in.

    Returns:
        List[List[Word]]: Sentences with reagent names combined into
            ReagentNameWords.
    """
    # Get list of known reagent names.
    known_reagent_names = list(
        reversed(
            sorted(
                get_known_reagent_names(
                    max_length=MAX_REAGENT_NAME_LENGTH),
                key=lambda x: len(x))))
    reagent_name_positions = []
    # Get candidate phrases
    phrases = get_candidate_phrases(sentences, MAX_REAGENT_NAME_LENGTH)
    # Search for all reagent names in all phrases.
    for phrase in phrases:
        for reagent_name in known_reagent_names:
            if phrase[0].lower() == reagent_name.lower():
                reagent_name_positions.append(phrase[1])
                break
    # Remove sub phrases from reagent name positions, resolve overlaps and turn
    # reagent names to into ReagentName words.
    reagent_name_positions = remove_sub_phrases(reagent_name_positions)
    reagent_name_positions = resolve_overlapping_phrases(reagent_name_positions)
    sentences = apply_reagent_names(sentences, reagent_name_positions)
    return sentences
