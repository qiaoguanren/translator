from typing import List
from ..utils import apply_pattern, trim_patterns
from ..words import Word, ColorWord

COLORS = [
    'blue',
    'red',
    'yellow',
    'green',
    'orange',
    'purple'
]

COLOR_ADJECTIVES = [
    'bright',
    'light',
    'deep',
    'pale',
    'dark'
]

COLOR_PATTERNS = []
for color in COLORS:
    COLOR_PATTERNS.append([color])
    for adjective in COLOR_ADJECTIVES:
        COLOR_PATTERNS.append([adjective, color])

COLOR_PATTERNS = sorted(COLOR_PATTERNS, key=lambda x: 1 / len(x))

def color_tag(sentences: List[List[Word]], word_bank) -> List[List[Word]]:
    """Tag colors in sentences.

    Args:
        sentences (List[List[Word]]): Sentences to tag colors in.

    Returns:
        List[List[Word]]: Sentences with colors tagged.
    """
    for pattern in trim_patterns(COLOR_PATTERNS, word_bank):
        apply_pattern(pattern, ColorWord, sentences)
    return sentences
