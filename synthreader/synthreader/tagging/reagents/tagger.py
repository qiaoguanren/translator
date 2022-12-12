from typing import List
import copy

from ..reagent_names import reagent_name_tag
from ...utils import apply_pattern, copy_and_modify_pattern, Optional
from ...words import (
    Word,
    QuantityWord,
    MassWord,
    VolumeWord,
    EquivalentsWord,
    QuantityGroupWord,
    ReagentNameWord,
    ReagentPlaceholderWord,
    ReagentWord,
    NumberWord,
    MultiplierWord,
    RatioWord,
)

amount_word_types = [MassWord, VolumeWord, EquivalentsWord]

reagent_pattern_bases = [
    # '10 equiv of iron powder ( 0.30 g )'
    [QuantityWord, 'of', ReagentNameWord, QuantityGroupWord],
    [QuantityWord, 'rinse', 'of', ReagentNameWord],
    # '5 g (0.029 mol) of theophylline'
    [QuantityWord, QuantityGroupWord, 'of', ReagentNameWord],
    [QuantityWord, 'of', ReagentNameWord],  # '2 mL of glacial acetic acid'
    # Needed for OrgSyn compatibility. 100 g. (0.67 mole) of phthalic anhydride
    [QuantityGroupWord, 'of', ReagentNameWord],
    [QuantityWord, ReagentNameWord],
    # '(20.6 g, 0.145 mol) methyl iodide'
    [QuantityGroupWord, ReagentNameWord],
    [ReagentNameWord, QuantityGroupWord],  # 'ethanol (2 mL)'
    [ReagentNameWord, 'washes', QuantityGroupWord],
    [ReagentPlaceholderWord, QuantityGroupWord],  # the substrate (5 g)
    # 1,3-bis-long-reagent-name (1) (21 g)...
    [ReagentNameWord, '(', NumberWord, ')', QuantityGroupWord],
    # 'One 20-mL portion of water' NB. 'one' is converted to '1' in
    # preprocessing
    [NumberWord, QuantityWord, 'portion', 'of', ReagentNameWord],
    ['a', QuantityWord, 'portion', 'of', ReagentNameWord],
    [QuantityWord, 'portions', 'of', ReagentNameWord],
    # 'rinsed with water (6 x 100 mL)...'
    [ReagentNameWord, '(', MultiplierWord, QuantityWord, ')'],
    # '88.2 g of the moist solid iodinane oxide.
    [QuantityWord, 'of', ReagentPlaceholderWord, ReagentNameWord],
    # 'a diethyl ether (50 mL) slurry'
    ['a', ReagentNameWord, QuantityGroupWord, 'slurry'],
    [QuantityWord, 'of', 'eluent', '(', ReagentNameWord, ',', RatioWord, ')']
]

# Add QuantityGroupWord at end for sentences like this:
# '500 g. (620 cc., 11.4 moles) of freshly distilled acetaldehyde
# (b. p. 20–22°)'
extra_patterns = []
for pattern in reagent_pattern_bases:
    extra_pattern = copy.deepcopy(pattern)
    extra_pattern.append(QuantityGroupWord)
    extra_patterns.append(extra_pattern)
reagent_pattern_bases.extend(extra_patterns)

REAGENT_PATTERNS = []
for j in range(len(amount_word_types)):
    for pattern in reagent_pattern_bases:
        added = False
        for i in range(len(pattern)):
            if pattern[i] == QuantityWord:
                REAGENT_PATTERNS.append(
                    copy_and_modify_pattern(
                        pattern, i, amount_word_types[j], 'replace'))
                added = True
                break
        if not added:
            REAGENT_PATTERNS.append(pattern)

for pattern in REAGENT_PATTERNS:
    pattern.append(Optional(NumberWord))

REAGENT_PATTERNS = sorted(REAGENT_PATTERNS, key=lambda x: 1 / len(x))

def reagent_tag(sentences: List[List[Word]]) -> List[List[Word]]:
    """Find reagents in sentences and return sentences with ReagentWords.

    Args:
        sentences (List[List[Word]]): Sentences after quantity tagging.

    Returns:
        List[List[Word]]: Sentences with reagent phrases combined into
            ReagentWords.
    """
    sentences = reagent_name_tag(sentences)
    for pattern in REAGENT_PATTERNS:
        sentences = apply_pattern(pattern, ReagentWord, sentences)
    # After ReagentName words have been used in patterns, convert them all to
    # quantity-less ReagentWords for the next stages of the process.
    for i, sentence in enumerate(sentences):
        for j, word in enumerate(sentence):
            if type(word) == ReagentNameWord:
                sentences[i][j] = ReagentWord([word])

    apply_pattern([NumberWord, QuantityGroupWord], ReagentWord, sentences)
    return sentences
