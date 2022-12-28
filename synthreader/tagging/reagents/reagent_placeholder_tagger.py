from typing import List, Union
import copy

from ...utils import apply_pattern, Pos, Optional, trim_patterns, sort_patterns
from ...words import (
    Word,
    ReagentPlaceholderWord,
    ColorWord,
    CoolWord,
    VesselWord,
    StirWord,
    ActionWord,
    QuantityWord
)

OPTIONAL_ADJECTIVE = Optional(Pos('JJ'))

#: Patterns to search for reagent placeholders phrases, i.e. 'the mixture',
# 'the product' etc.
REAGENT_PLACEHOLDER_PATTERNS: List[List[Union[int, str]]] = [
    ['the', OPTIONAL_ADJECTIVE, 'compound'],
    ['the', OPTIONAL_ADJECTIVE, 'product', Optional('solution')],
    ['the', OPTIONAL_ADJECTIVE, 'crude', 'product', Optional('solution')],
    ['the', OPTIONAL_ADJECTIVE, 'mixture'],
    ['the', OPTIONAL_ADJECTIVE, 'solvent'],
    ['the', OPTIONAL_ADJECTIVE, 'slurry'],
    ['the', OPTIONAL_ADJECTIVE, 'solution'],
    ['the', OPTIONAL_ADJECTIVE, 'suspension'],
    ['the', OPTIONAL_ADJECTIVE, 'residue'],
    ['the', OPTIONAL_ADJECTIVE, 'reaction', 'mixture'],
    ['the', Optional('crude'), 'reaction', 'mixture'],
    ['the', 'reaction', VesselWord],
    ['the', StirWord, 'solution'],
    ['the', OPTIONAL_ADJECTIVE, 'filter', 'cake'],
    ['the', OPTIONAL_ADJECTIVE, 'amide'],
    ['the', OPTIONAL_ADJECTIVE, 'solid'],
    ['the', OPTIONAL_ADJECTIVE, 'solids'],
    ['the', Optional('combined'), 'aqueous', 'extracts'],
    ['the', Optional('combined'), 'organic', 'extracts'],
    ['the', Optional('combined'), Optional('separated'), 'organic', 'phase'],
    ['the', Optional('combined'), 'organic', 'phases'],
    ['the', Optional('combined'), 'aqueous', 'phases'],
    ['the', Optional('combined'), Optional(ActionWord), 'aqueous', 'phase'],
    ['the', Optional('combined'), 'organic', 'layers'],
    ['the', Optional('combined'), 'aqueous', 'layers'],
    ['the', Optional('combined'), 'extracts'],
    ['the', 'upper', 'layer'],
    ['the', 'lower', 'layer'],
    ['the', Optional(Pos('JJ')), 'oil'],
    ['impure', 'fractions', 'from', 'the', 'initial', 'column'],
    ['residual', 'solvent'],
    ['the', 'residual', 'solvent'],
    ['the', 'residual', 'liquid'],
    ['the', 'residual'],
    ['the', Optional('combined'), 'organic', 'layer'],
    ['the', Optional('combined'), 'aqueous', 'layer'],
    ['the', 'batch'],
    ['the', OPTIONAL_ADJECTIVE, 'needles'],
    ['the', OPTIONAL_ADJECTIVE, 'reaction'],
    ['the', 'completed', 'reaction'],
    ['the', 'reaction', 'solution'],
    ['the', OPTIONAL_ADJECTIVE, 'material'],
    ['this', 'material'],
    ['the', 'solid', 'material'],
    ['the', 'liquid'],
    ['the', 'volatile', 'materials'],
    ['the', 'volatiles'],
    ['the', 'fractions', 'containing', 'the', 'product'],
    ['the', OPTIONAL_ADJECTIVE, 'organic', 'material'],
    ['the', OPTIONAL_ADJECTIVE, 'crystals'],
    ['the', OPTIONAL_ADJECTIVE, 'filtrate'],
    ['the', 'substrate'],
    ['the', OPTIONAL_ADJECTIVE, 'precipitate'],
    ['the', 'gummy', 'precipitate'],
]
extra_patterns = []
for pattern in REAGENT_PLACEHOLDER_PATTERNS:
    if pattern[1] is OPTIONAL_ADJECTIVE:
        extra_pattern = copy.deepcopy(pattern)
        extra_pattern.insert(1, ',')
        extra_pattern.insert(1, OPTIONAL_ADJECTIVE)
        extra_patterns.append(extra_pattern)

        extra_pattern = copy.deepcopy(pattern)
        extra_pattern[1] = ColorWord
        extra_patterns.append(extra_pattern)
REAGENT_PLACEHOLDER_PATTERNS.extend(extra_patterns)

for i in range(len(REAGENT_PLACEHOLDER_PATTERNS)):
    new_pattern = copy.deepcopy(REAGENT_PLACEHOLDER_PATTERNS[i])
    # 'the resulting slurry' etc.
    new_pattern.insert(1, 'resulting')
    REAGENT_PLACEHOLDER_PATTERNS.append(new_pattern)

    new_pattern = copy.deepcopy(REAGENT_PLACEHOLDER_PATTERNS[i])
    # 'the resulted slurry' etc.
    new_pattern.insert(1, 'resulted')
    REAGENT_PLACEHOLDER_PATTERNS.append(new_pattern)

REAGENT_PLACEHOLDER_PATTERNS = sort_patterns(REAGENT_PLACEHOLDER_PATTERNS)

def reagent_placeholder_tag(
        sentences: List[List[Word]], word_bank) -> List[List[Word]]:
    """Find reagent placeholder phrases in sentences and return sentences with
    ReagentPlaceholderWords. This is stuff like 'the product', 'the mixture'...

    Args:
        sentences (List[List[Word]]): Sentences after reagent tagging.

    Returns:
        List[List[Word]]: Sentences with reagent placeholder phrases combined
            into ReagentWords.
    """
    # Liberate 'cooled' words
    for sentence in sentences:
        for i, word in enumerate(sentence):
            if str(word) == 'cooled':
                sentence[i] = Word('cooled', 'JJ')

    for pattern in trim_patterns(REAGENT_PLACEHOLDER_PATTERNS, word_bank):
        apply_pattern(pattern, ReagentPlaceholderWord, sentences)

    # Reapply 'cooled' as CoolWord
    for sentence in sentences:
        for i, word in enumerate(sentence):
            if str(word) == 'cooled':
                sentence[i] = CoolWord([word])
    for pattern in [
        [QuantityWord, 'of', ReagentPlaceholderWord],
        ['the', 'rest', 'of', ReagentPlaceholderWord],
    ]:
        apply_pattern(pattern, ReagentPlaceholderWord, sentences)

    return sentences
