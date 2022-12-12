import re
from typing import List, Tuple
from .constants import (
    HTML_REPLACEMENTS, MISSING_SPACE_REPLACEMENTS, TACTICAL_REPLACEMENTS)

def preprocess(synthesis_text: str) -> str:
    """Preprocess synthesis text. Tasks are:
    1) Remove any HTML remnants (common in texts from Reaxys)
    2) Remove NMR from end of description.
    3) Fix missing/extra spaces.
    4) Apply tactical word/phrase replacements to simplify NLP tasks downstream
    in process.

    Args:
        synthesis_text (str): Description of synthetic procedure.

    Returns:
        str: Synthetic procedure cleaned up and ready for tagging.
    """
    s = synthesis_text
    s = apply_regex_replacements(s, HTML_REPLACEMENTS)
    # s = remove_nmr(s)
    s = apply_regex_replacements(s, MISSING_SPACE_REPLACEMENTS)
    s = apply_regex_replacements(s, TACTICAL_REPLACEMENTS)

    return s

def remove_nmr(synthesis_text: str) -> str:
    """Remove NMR from end of synthesis text.

    Args:
        synthesis_text (str): Description of synthetic procedure.

    Returns:
        str: Synthetic procedure with NMR at end removed.
    """
    s = synthesis_text
    if 'NMR' in s:
        s = s.split('NMR')[0][:-2]
    return s

def apply_regex_replacements(
        s: str, replacements: List[Tuple[str, str]]) -> str:
    """Apply regex replacements to given str.
    i.e. s='was then added', replacements=[('then', '')] will return
    'was added'.

    Args:
        s (str): text to apply replacements to.
        replacements (List[Tuple[str, str]]): List of tuples with pattern to
            replace and replacement.

    Returns:
        str: Original text with all replacements applied.
    """
    for target, replacement in replacements:
        s = re.sub(target, replacement, s)
    return s
