from typing import List, Union, Any
import copy
from . import Optional

def sort_patterns(patterns: List[List[Any]], types_included: bool = False):
    """Sort patterns from longest to shortest not including Optional items when
    calculating length.

    Args:
        patterns (List[List[Any]]): Patterns to sort
        types_included (bool): If True, expect patterns to be list of
            [(pattern, type)...] else expect list of [pattern...]
    """
    if types_included:
        return sorted(
            patterns,
            key=lambda item: (
                1 / len([x for x in item[0] if type(x) != Optional])
            )
        )
    else:
        return sorted(
            patterns,
            key=lambda item: (
                1 / len([x for x in item if type(x) != Optional])
            )
        )

def copy_and_modify_pattern(
    pattern: List[Union[type, str]],
    mod_index: int,
    mod_obj: Union[type, str],
    mode: str,
) -> List[Union[type, str]]:
    """Copy pattern, modify it and return the modified pattern.

    Args:
        pattern (List[Union[type, str]]): Pattern to copy.
        mod_index (int): Index to change.
        mod_obj (Union[type, str]): Object to add.
        mode (str): 'insert' means new_pattern.insert(mod_index, mod_obj)
            'replace' means new_pattern[mod_index] = mod_obj

    Returns:
        List[Union[type, str]]: Copy of pattern with object at mod_index
            replaced by mod_obj.
    """
    new_pattern = copy.deepcopy(pattern)
    if mode == 'replace':
        new_pattern[mod_index] = mod_obj
    elif mode == 'insert':
        new_pattern.insert(mod_index, mod_obj)
    return new_pattern

def trim_patterns(patterns, word_bank):
    patterns = copy.deepcopy(patterns)
    for i in reversed(range(len(patterns))):
        pattern = patterns[i]
        if type(pattern[0]) == list:
            pattern = pattern[0]
        for item in pattern:
            if type(item) == str and item.lower() not in word_bank:
                patterns.pop(i)
                break
    return patterns
