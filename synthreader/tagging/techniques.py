from typing import List
from ..words import Word, TechniqueWord
from ..utils import apply_pattern, trim_patterns

TECHNIQUE_PATTERNS = [
    ['filtration'],
    ['vacuum', 'filtration'],
    ['cannula', 'filtration'],
    ['TLC'],
    ['flash', 'column', 'chromatography'],
    ['flash', 'chromatography'],
    ['column', 'chromatography'],
    ['short', 'path', 'vacuum', 'distillation'],
    ['vacuum', 'distillation'],
    ['rapid', 'vacuum', 'distillation'],
    ['chromatography'],
    ['silica', 'gel', 'chromatography'],
    ['silica-gel', 'chromatography'],
    ['kugelrohr', 'distillation'],
    ['rotary', 'evaporation'],
    ['rotatory', 'evaporation'],
]

TECHNIQUE_PATTERNS = sorted(TECHNIQUE_PATTERNS, key=lambda x: 1 / len(x))

def technique_tag(sentences: List[List[Word]], word_bank) -> List[List[Word]]:
    """Find techniques in sentences and return sentences with TechniqueWords.

    Args:
        sentences (List[List[Word]]): Sentences after tokenization.

    Returns:
        List[List[Word]]: Sentences with action phrases combined into
            ActionWords.
    """
    for pattern in trim_patterns(TECHNIQUE_PATTERNS, word_bank):
        apply_pattern(pattern, TechniqueWord, sentences)
    return sentences
