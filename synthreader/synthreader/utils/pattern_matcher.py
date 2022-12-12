from typing import Type, List, Union, Tuple
import re
from ..words import Word

class Optional(Word):
    def __init__(self, word):
        self.word = word

class Regexp(object):
    def __init__(self, regexp):
        self.regexp = regexp

class Pos(object):
    def __init__(self, pos):
        self.pos = pos

class AnyOf(object):
    def __init__(self, words):
        self.words = words

def apply_pattern(
    pattern: List[Union[Type[Word], str, int]],
    word_class: Type[Word],
    sentences: List[List[Word]],
    replace_pos: Union[int, Tuple[int, int]] = None,
) -> List[List[Word]]:
    """Look for pattern in sentences and replace pattern matches with
    word_class object instantiated with pattern match. Return sentences with
    pattern matches replaces by word_class objects.

    Args:
        pattern (List[Union[Type[Word], str]]): Pattern to look for,
            i.e. [NumberWord, UnitWord]
        word_class (Type[Word]): Class to instantiate with pattern match.
        sentences (List[List[Word]]): Sentences to find and replace pattern
            with word_class object.
        replace_pos (Union[int, Tuple[int, int]]): Position in pattern to
            use for instantiating word_class. If not given entire pattern is
            used.
    """
    i = 0
    while i < len(sentences):
        words = sentences[i]
        j = 0
        while j < len(words):
            pattern_match = True
            pattern_idx = 0  # Index into pattern
            sentence_idx = 0  # Index into sentence

            # These need to be handled separately for OPTIONAL words.
            while pattern_idx < len(pattern):
                # If sentence index within sentence.
                if j + sentence_idx < len(words):
                    # Get target from pattern and word from words.
                    target = pattern[pattern_idx]
                    word = words[j + sentence_idx]
                    if type(target) == Optional:

                        # Try optional word
                        if is_match(target.word, word):
                            pattern_idx += 1
                            sentence_idx += 1
                            continue

                        else:
                            # Optional word not found, try next item in pattern
                            if pattern_idx + 1 < len(pattern):
                                pattern_idx += 1
                                continue
                            # Optional word not found and end of pattern reached
                            else:
                                break

                    # If target and word don't match, break otherwise continue
                    elif not is_match(target, word):
                        pattern_match = False
                        break

                # If sentence index not within sentence break.
                else:
                    if all([
                        type(item) == Optional
                        for item in pattern[pattern_idx:]]
                    ):
                        break
                    else:
                        pattern_match = False
                        break

                pattern_idx += 1
                sentence_idx += 1

            start_i = j
            if pattern_match:
                if replace_pos:
                    if type(replace_pos) == int:
                        start_i = j + replace_pos
                        end_i = start_i + 1
                    else:
                        start_i = j + replace_pos[0]
                        end_i = j + replace_pos[1]
                else:
                    start_i = j
                    end_i = j + sentence_idx
                # Normal tagging where type is specified.
                if type(word_class) == type:
                    new_words = [word_class(words[start_i: end_i])]
                # In interpreting lambda functions are used to return list of
                # Action objects.
                elif callable(word_class):
                    new_words = word_class(words[start_i: end_i])
                del sentences[i][start_i: end_i]
                for item in reversed(new_words):
                    sentences[i].insert(start_i, item)
            j = start_i + 1
        i += 1
    return sentences

def is_match(target: Union[type, str], word: Word) -> bool:
    """Return True is word is a match for target, otherwise False.

    Args:
        target (Union[type, str]): Item in pattern list.
        word (Word): Word object to check against target.

    Returns:
        bool: True if word matches target, otherwise False.
    """
    if type(target) == type:
        if not isinstance(word, target):
            return False

    elif type(target) == str:
        if type(word) == Word:
            if not target.lower() == word.word.lower():
                return False
        else:
            return False

    elif type(target) == Regexp:
        if re.match(target.regexp, str(word)):
            return True
        return False

    elif type(target) == Pos:
        if type(word) == Word:
            if word.pos.startswith(target.pos):
                return True
            else:
                return False
        else:
            return False

    elif type(target) == AnyOf:
        for subtarget in target.words:
            if is_match(subtarget, word):
                return True
        return False

    elif type(target) == Optional:
        return False
    return True
