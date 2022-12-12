from typing import List, Dict, Tuple
import re
import itertools

from .common_english_words import COMMON_ENGLISH_WORDS
from .constants import (
    REAGENT_NAME_IGNORE_WORD_LIST,
    MIN_REAGENT_NAME_LENGTH,
    REAGENT_NAME_END_IGNORE_WORDS,
    REAGENT_NAME_IGNORE_CHAR_LIST,
    REAGENT_NAME_BEFORE_WORDS,
    REAGENT_NAME_IGNORE_FIRST_WORD,
    REAGENT_NAME_AFTER_WORDS
)
from ...words import (
    Word,
    ReagentNameFragmentWord,
    ReagentNameWord,
    ConcWord,
    TimeWord,
    PercentWord,
    NumberWord,
    AuxiliaryVerbWord,
    format_reagent_name,
)

####################
# PHRASE GATHERING #
####################

def is_candidate_reagent_word(word: str) -> bool:
    """Return True if the word could be part of a reagent name, otherwise False.

    Criteria:
        1) Word not in blacklist.

    Args:
        word (str): Word to decide if it could be part of a reagent name.

    Returns:
        bool: True if word could be part of a reagent name, otherwise False.
    """
    word = word.lower()
    if word in REAGENT_NAME_IGNORE_WORD_LIST:
        return False
    return True

def is_candidate_reagent_phrase(phrase: str) -> bool:
    """Return True if the phrase could be a reagent name, otherwise False.

    Criteria:
        1) Number of characters in word is > 1.

    Args:
        phrase (str): Phrase to decide if it could be a reagent name.

    Returns:
        bool: Word to decide if it could be part of a reagent name.
    """
    if len(phrase) < MIN_REAGENT_NAME_LENGTH:
        return False
    elif phrase[-1] in REAGENT_NAME_END_IGNORE_WORDS:
        return False
    elif phrase in REAGENT_NAME_IGNORE_WORD_LIST:
        return False
    # No uneven brackets
    for pair in [('(', ')'), ('[', ']'), ('{', '}')]:
        if phrase.count(pair[0]) != phrase.count(pair[1]):
            return False

    for char in REAGENT_NAME_IGNORE_CHAR_LIST:
        if char in phrase:
            return False

    # Stop two reagents in list being tagged, assume commas in reagent name will
    # always be something like '1,3-...'
    if ',' in phrase and not re.search(r'[0-9α],', phrase):
        return False
    return True

def get_candidate_phrases(
        sentences: List[List[Word]], max_length: int) -> List[str]:
    """Get a list of all possible phrases in sentences that haven't been ruled
    out as a reagent name.

    Args:
        sentences (List[List[Word]]): Sentences to take phrases from.
        max_length (int): Maximum number of characters allowed in a phrase.

    Returns:
        List[str]: List of phrases that haven't been ruled out as reagent names.
    """
    phrases = []
    for i in range(len(sentences)):
        sentence = sentences[i]
        for j, k in itertools.combinations(range(len(sentence) + 1), 2):
            if all([
                (
                    type(word) in [Word, ReagentNameFragmentWord]
                    and is_candidate_reagent_word(str(word))
                )
                for word in sentence[j: k]
            ]):
                phrase = format_reagent_name(sentence[j: k])
                if (len(phrase) <= max_length
                        and is_candidate_reagent_phrase(phrase)):
                    phrases.append([phrase, (i, j, k)])

    return sorted(phrases, key=lambda x: 1 / len(x))


#################################################
# DEAL WITH UNCOMPATIBLE REAGENT NAME POSITIONS #
#################################################

def is_sub_phrase(
    phrase_position: Tuple[int, int, int],
    sub_phrase_position: Tuple[int, int, int]
) -> bool:
    """Return True if phrases represented by phrase represented by
    sub_phrase_position is part of phrase represented by phrase_position,
    otherwise False.

    Args:
        phrase_position (Tuple[int, int, int]): sentence_i, start_word_i,
            end_word_i position.
        sub_phrase_position (Tuple[int, int, int]): sentence_i, start_word_i,
            end_word_i position.

    Returns:
        bool: if phrases represented by phrase represented by
            sub_phrase_position is part of phrase represented by
            phrase_position, otherwise False.
    """
    sentence_i, start_word_i, end_word_i = phrase_position
    sub_sentence_i, sub_start_word_i, sub_end_word_i = sub_phrase_position
    return (sentence_i == sub_sentence_i
            and sub_start_word_i >= start_word_i
            and sub_end_word_i <= end_word_i)

def remove_sub_phrases(reagent_name_positions: List[Tuple[int, int, int]]
                       ) -> List[Tuple[int, int, int]]:
    """Remove shorter reagent names that are part of longer reagent names, i.e.
    ['acetic acid', 'glacial acetic acid'], 'acetic acid' should be removed.
    Note: List returned is sorted differently to list passed in.

    Args:
        reagent_name_positions (List[Tuple[int, int, int]]): List of
            (sentence_i, start_word_i, end_word_i) positions corresponding to
            reagent names.

    Returns:
        List[Tuple[int, int, int]]: List of
            (sentence_i, start_word_i, end_word_i) positions corresponding to
            reagent names with shorter reagent names that were part of longer
            reagent names removed.
    """

    # Sort reagent names longest (by word count) -> shortest (by word count)
    sorted_reagent_positions = list(
        sorted(
            reagent_name_positions,
            key=lambda x: -(x[2] - x[1])))  # 1 / (end_word_i - start_word_i)
    # From longest to shortest name, search for shorter names in longer names
    # and remove them.
    i = 0
    while i < len(sorted_reagent_positions):
        # Unpack longer name position.
        phrase_position = sorted_reagent_positions[i]
        # Search from end of list back for shorter name within longer name.
        j = len(sorted_reagent_positions) - 1
        while j > i:
            # Unpack shorter name position.
            potential_sub_phrase_position = sorted_reagent_positions[j]
            # If longer name contains shorter name.
            if is_sub_phrase(phrase_position, potential_sub_phrase_position):
                sorted_reagent_positions.pop(j)
            j -= 1
        i += 1
    return sorted_reagent_positions

def resolve_overlapping_phrases(
    reagent_name_positions: List[Tuple[int, int, int]],
    position_raw_prediction_dict: Dict[Tuple[int, int, int], List] = None
) -> List[Tuple[int, int, int]]:
    """Remove one of overlapping pairs of reagent names, i.e. if an incorrect
    prediction was made you could have reagent names
    ['glacial acetic acid', 'acetic acid added',] for the phrase
    'glacial acetic acid added'. 'acetic acid added' should be removed.

    The name to remove is the name with the larger ratio of neural network
    prediction values is_reagent_name: not_reagent_name.

    Args:
        reagent_name_positions (List[Tuple[int, int, int]]): List of
            (sentence_i, start_word_i, end_word_i) positions corresponding to
            reagent names.
        position_raw_prediction_dict (Dict[Tuple[int, int, int], List]):
            Dict of {position: prediction array from model}

    Returns:
        List[Tuple[int, int, int]]: List of
            (sentence_i, start_word_i, end_word_i) positions corresponding to
            reagent names with one reagent name of all overlapping reagent name
            pairs removed.
    """
    i = 0
    # var used later to decide how to update i counter.
    # Go through reagent name positions
    while i < len(reagent_name_positions):
        # Unpack first reagent name position.
        position1 = reagent_name_positions[i]

        # Go through from end of list to start looking for overlapping names.
        j = len(reagent_name_positions) - 1
        popped_i = False
        while j > i:
            # Unpack second reagent name position.
            position2 = reagent_name_positions[j]

            # If check if first and second reagent name are overlapping.
            if is_overlapping(position1, position2):
                # If raw predictions are supplied decide which name to
                # discard base on is_reagent_name: not_reagent_name
                # neural network prediction ratio
                if position_raw_prediction_dict:
                    position_to_use = resolve_overlap(
                        position1, position2, position_raw_prediction_dict)

                    if position2 == position_to_use:
                        # Remove position2 and keep looking for more position2s
                        # overlapping with position1.
                        popped_i = False
                        reagent_name_positions.pop(j)

                    else:
                        # Remove position1, break and move onto next position1.
                        popped_i = True
                        reagent_name_positions.pop(i)
                        break

                # If no model predictions supplied arbitrarily remove
                # second reagent name.
                else:
                    reagent_name_positions.pop(j)
            j -= 1
        # If i has been popped next phrase will be in current i position.
        if not popped_i:
            i += 1
    return reagent_name_positions

def is_overlapping(
    position1: Tuple[int, int, int],
    position2: Tuple[int, int, int]
) -> bool:
    """Return True if phrases represented by position1 and position2 overlap,
    otherwise False.

    Args:
        position1 (Tuple[int, int, int]): sentence_i, start_word_i, end_word_i
            position.
        position2 (Tuple[int, int, int]): sentence_i, start_word_i, end_word_i
            position.

    Returns:
        bool: True if phrases represented by position1 and position2 overlap,
    otherwise False.
    """
    first_sentence_i, first_start_word_i, first_end_word_i = position1
    second_sentence_i, second_start_word_i, second_end_word_i = position2
    same_sentence = first_sentence_i == second_sentence_i
    overlap_pos1_start = (second_end_word_i > first_start_word_i
                          and second_start_word_i < first_start_word_i)
    overlap_pos1_end = (second_start_word_i < first_end_word_i
                        and second_end_word_i > first_end_word_i)
    return same_sentence and (overlap_pos1_start or overlap_pos1_end)

def resolve_overlap(
    position1: Tuple[int, int, int],
    position2: Tuple[int, int, int],
    position_raw_prediction_dict: Dict[Tuple[int, int, int], List]
) -> Tuple[int, int, int]:
    """Decide given two positions which one to keep based on the values in the
    model prediction array.

    Args:
        position1 (Tuple[int, int, int]): sentence_i, start_word_i, end_word_i
            position.
        position2 (Tuple[int, int, int]): sentence_i, start_word_i, end_word_i
            position.
        position_raw_prediction_dict (Dict[Tuple[int, int, int], List]):
            Dict of {position: model prediction array}

    Returns:
        Tuple[int, int, int]: Position which should be kept out of the two.
    """
    position1_pred = position_raw_prediction_dict[position1]
    position2_pred = position_raw_prediction_dict[position2]
    position1_certainty = position1_pred[1] / position1_pred[0]
    position2_certainty = position2_pred[1] / position2_pred[0]
    if position1_certainty > position2_certainty:
        return position1
    return position2


#####################################################
# CONVERT Word OBJECTS INTO ReagentNameWord OBJECTS #
#####################################################

def is_reagent_prefix(word: Word, reagent_name_words: List[Word]):
    """Return True if word is a recognised word that precedes reagent names,
    i.e. 'saturated', otherwise False.

    Args:
        word (Word): Word object to check if it is a reagent prefix.
        reagent_name (List[Word]): List of Words in reagent name so far.

    Returns:
        bool: True if word is a recognised reagent prefix otherwise False.
    """
    reagent_name = ' '.join([str(word) for word in reagent_name_words])
    is_prefix = False

    if type(word) == NumberWord:
        return True

    for item in REAGENT_NAME_BEFORE_WORDS:
        # Single word prefix i.e. 'saturated'
        if type(item) == str and str(word).lower() == item:
            is_prefix = True

        # Multiword prefixes i.e. ['half', 'saturated']
        elif type(item) == list:
            if item[0] == str(word):
                i = 1
                is_prefix = True
                # Check all words in prefix accounted for.
                while i < len(item) and i - 1 < len(reagent_name):
                    if item[i] != str(reagent_name_words[i - 1]):
                        is_prefix = False
                        break
                    i += 1
        if is_prefix:
            break

    is_concentration = type(word) in [ConcWord, TimeWord]
    is_percent = type(word) == PercentWord
    is_auxiliary_verb = type(word) == AuxiliaryVerbWord
    is_reagent_name_fragment = type(word) == ReagentNameFragmentWord
    opening_bracket = (
        type(word) == Word
        and word.word == '('
        and reagent_name.count(')') > reagent_name.count('(')
    )
    return (
        (is_prefix
         or is_percent
         or is_concentration
         or opening_bracket
         or is_reagent_name_fragment)
        and not is_auxiliary_verb
    )

def is_reagent_suffix(word: Word, reagent_name: List[Word]):
    """Return True if word is a recognised word that comes after reagent names,
    i.e. 'solution', otherwise False.

    Args:
        word (Word): Word object to check if it is a reagent suffix.
        reagent_name (List[Word]): List of Words in reagent name so far.

    Returns:
        bool: True if word is a recognised reagent suffix otherwise False.
    """
    reagent_name = ' '.join([str(word) for word in reagent_name])
    closing_bracket = (
        type(word) == Word
        and word.word == ')'
        and reagent_name.count('(') > reagent_name.count(')')
    )
    is_auxiliary_verb = type(word) == AuxiliaryVerbWord
    explicit_suffix = (
        type(word) == Word and word.word.lower() in REAGENT_NAME_AFTER_WORDS)
    return ((explicit_suffix
             or type(word) == NumberWord
             or closing_bracket)
            and not is_auxiliary_verb)

def apply_reagent_names(
    sentences: List[List[Word]],
    reagent_name_positions: List[Tuple[int, int, int]]
) -> List[List[Word]]:
    """Combine words corresponding to reagent_name_positions into
    ReagentNameWords and return updated sentences.

    Args:
        sentences (List[List[Word]]): Sentences to combine reagent name Words
            into ReagentNameWord objects.
        reagent_name_positions (List[Tuple[int, int, int]]):
            sentence_i, start_word_i, end_word_i positions corresponding to
            reagent names.

    Returns:
        List[List[Word]]: Sentences with reagent name Words combined into
            ReagentNameWords.
    """
    # Sort list descending by sentence_i then descending by start_word_i
    sorted_reagent_name_positions = sorted(
        reagent_name_positions,
        key=lambda x: (-x[0], -x[1]))

    for sentence_i, start_word_i, end_word_i in sorted_reagent_name_positions:
        sentence = sentences[sentence_i]
        # If there is a Word object just before the reagent name, and the word
        # is a common reagent name prefix, include it in the reagent name.
        while start_word_i > 0 and is_reagent_prefix(
                sentence[start_word_i - 1],
                sentence[start_word_i: end_word_i]):
            start_word_i -= 1

        # If there is a Word object just after the reagent name, and the word is
        # a common reagent name suffix, include it in the reagent name.
        while (end_word_i < len(sentence)
               and is_reagent_suffix(
                sentence[end_word_i],
                sentence[start_word_i: end_word_i])):
            end_word_i += 1

        # Look for abbreviations, e.g. 'sodium hydroxide (NaOH)'
        abbreviation = (
            end_word_i + 2 < len(sentence)
            and str(sentence[end_word_i]) == '('
            and str(sentence[end_word_i + 2]) == ')'
            and type(sentence[end_word_i + 1]) in [Word, ReagentNameWord]
        )
        if abbreviation:
            end_word_i += 3

        # If there is a Word object just after the reagent name, and the word is
        # a common reagent name suffix, include it in the reagent name.
        while (end_word_i < len(sentence)
               and is_reagent_suffix(
                sentence[end_word_i],
                sentence[start_word_i: end_word_i])):
            end_word_i += 1

        # Add on any numbers at end e.g. 'NbCl4(THF)2', if 2 hasn't already been
        # matched add it on here.
        if (end_word_i < len(sentence)
                and type(sentence[end_word_i]) == NumberWord):
            end_word_i += 1

        if str(sentence[start_word_i]) in REAGENT_NAME_IGNORE_FIRST_WORD:
            start_word_i += 1

        # Combine words into ReagentNameWord and add it to the sentence.
        if (' '.join([str(word) for word in sentence[start_word_i: end_word_i]])
                not in COMMON_ENGLISH_WORDS):
            reagent_name_word = ReagentNameWord(
                sentences[sentence_i][start_word_i: end_word_i])
            del sentences[sentence_i][start_word_i: end_word_i]
            sentences[sentence_i].insert(start_word_i, reagent_name_word)

    return sentences
