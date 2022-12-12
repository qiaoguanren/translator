from typing import List, Union
import re
import copy

from ..words import (
    Word,
    NumberWord,

    VolumeUnitWord,
    MassUnitWord,
    TempUnitWord,
    TimeUnitWord,
    ConcUnitWord,
    MolUnitWord,
    PercentUnitWord,
    EquivalentsUnitWord,
    PressureUnitWord,
    StirSpeedUnitWord,
    LengthUnitWord,
    UnitWord,
    MolPercentUnitWord,

    VolumeWord,
    MassWord,
    ConcWord,
    TempWord,
    TimeWord,
    MolWord,
    PercentWord,
    EquivalentsWord,
    PressureWord,
    StirSpeedWord,
    LengthWord,
    MolPercentWord,

    RatioWord,
    QuantityWord,
    QuantityGroupWord,
    MultiplierWord,
    RangeWord,
    RepeatedVolumeWord,

    ReagentNameWord,
    PercentInSolventWord,

    YieldWord,
    SupplierWord,
    pHWord,

    BPWord,
    MPWord
)
from ..utils import apply_pattern, Optional
from ..constants import (
    TIME_UNITS,
    VOLUME_UNITS,
    MASS_UNITS,
    TEMP_UNITS,
    MOL_UNITS,
    EQUIVALENTS_UNITS,
    PERCENT_UNITS,
    PRESSURE_UNITS,
    CONC_UNITS,
    STIR_SPEED_UNITS,
    LENGTH_UNITS,
    MOL_PERCENT_UNITS,
    ratio_regex_pattern,
    multiplier_regex_pattern,
    range_float_regex_pattern,
    conc_regex_pattern,
    LITERAL_MULTIPLIER_DICT,
)

def quantity_tag(sentences: List[List[Word]]) -> List[List[Word]]:
    """Find quantities in sentences and return sentences with QuantityWords.

    Args:
        sentences (List[List[Word]]): Sentences after tokenization and POS
            tagging.

    Returns:
        List[List[Word]]: Sentences with quantity phrases combined into
            QuantityWords.
    """
    unit_quantity_types = [
        (VolumeUnitWord, VolumeWord),
        (MassUnitWord, MassWord),
        (TempUnitWord, TempWord),
        (TimeUnitWord, TimeWord),
        (ConcUnitWord, ConcWord),
        (MolUnitWord, MolWord),
        (EquivalentsUnitWord, EquivalentsWord),
        (PercentUnitWord, PercentWord),
        (PressureUnitWord, PressureWord),
        (StirSpeedUnitWord, StirSpeedWord),
        (LengthUnitWord, LengthWord),
        (MolPercentUnitWord, MolPercentWord),
    ]
    conc_tag(sentences)
    number_tag(sentences)
    unit_tag(sentences)
    ratio_tag(sentences)
    range_tag(sentences)
    multiplier_tag(sentences)

    quantity_patterns = []
    for unit_type, quantity_type in unit_quantity_types:
        quantity_patterns.append(([NumberWord, unit_type], quantity_type))
        # '1 additional hour', seen in OrgSyn
        quantity_patterns.append(
            ([NumberWord, 'additional', unit_type], quantity_type))
        quantity_patterns.append(([RangeWord, unit_type], quantity_type))

    # Add extra patterns for approximate quantities
    extra_patterns = []
    for pattern in quantity_patterns:
        for word in [
            ['about'],
            ['approximately'],
            ['a', 'final'],
            ['an', 'additional']
        ]:
            new_pattern = copy.deepcopy(pattern)
            for item in reversed(word):
                new_pattern[0].insert(0, item)
            extra_patterns.append(new_pattern)

    quantity_patterns.extend(extra_patterns)

    quantity_patterns = sorted(quantity_patterns, key=lambda x: 1 / len(x[0]))

    for pattern, quantity_type in quantity_patterns:
        apply_pattern(pattern, quantity_type, sentences)

    apply_pattern([PercentWord, 'aq'], ConcWord, sentences)

    volume_and_multiplier_tag(sentences)
    # quantity_group_tag(sentences)
    yield_tag(sentences)
    ph_tag(sentences)
    bp_mp_tag(sentences)

    remove_floating_units(sentences)

    # Final range word tag
    apply_pattern([QuantityWord, 'to', QuantityWord], RangeWord, sentences)
    return sentences

def remove_floating_units(sentences: List[List[Word]]) -> List[List[Word]]:
    for sentence in sentences:
        for i in range(len(sentence)):
            word = sentence[i]
            if isinstance(word, UnitWord):
                sentence[i] = Word(str(word), word.words[0].pos)
    return sentences

def conc_tag(sentences: List[List[Word]]) -> List[List[Word]]:
    """Tag concentration with no space between number and unit e.g. '3M'.

    Args:
        sentences (List[List[Word]]): Sentences to tag concentrations in.

    Returns:
        List[List[Word]]: Sentences with concentrations with no space between
            number and unit tagged.
    """
    for sentence in sentences:
        for j, word in enumerate(sentence):
            conc_match = re.match(conc_regex_pattern, str(word))
            if conc_match:
                sentence[j] = ConcWord([word])
    return sentences

def range_tag(sentences: List[List[Word]]) -> List[List[Word]]:
    """Find ranges in sentences (i.e. '8-18 hours') and return sentences with
    RangeWords.

    Args:
        sentences (List[List[Word]]): Sentences after tokenization.

    Returns:
        List[List[Word]]: Sentences with ranges converted to RangeWords.
    """
    for i, sentence in enumerate(sentences):
        for j, word in enumerate(sentence):
            if type(word) == Word:
                if re.match(range_float_regex_pattern, word.word):
                    sentences[i][j] = RangeWord([word])
    apply_pattern([NumberWord, 'to', NumberWord], RangeWord, sentences)
    return sentences

def multiplier_tag(sentences: List[List[Word]]) -> List[List[Word]]:
    """Find multipliers in sentences (i.e. 'washed 4x with...') and return
    sentences with MultiplierWords.

    Args:
        sentences (List[List[Word]]): Sentences after tokenization.
    Returns:
        List[List[Word]]: Sentences with multipliers converted to
            MultiplierWords.
    """
    multiplier_patterns = [
        [NumberWord, 'x'],
        [NumberWord, '×'],
        [NumberWord, 'Xx'],
        ['x', NumberWord],
        ['×', NumberWord],
        ['X', NumberWord],
        [NumberWord, 'times'],
    ]
    for i, sentence in enumerate(sentences):
        for j, word in enumerate(sentence):
            if type(word) == Word:
                if re.match(multiplier_regex_pattern, word.word):
                    sentences[i][j] = MultiplierWord([word])
    for item in LITERAL_MULTIPLIER_DICT:
        apply_pattern(item.split(), MultiplierWord, sentences)
    for item in multiplier_patterns:
        apply_pattern(item, MultiplierWord, sentences)
    return sentences

def volume_and_multiplier_tag(sentences):
    for pattern in [
        [MultiplierWord, VolumeWord],
        [VolumeWord, MultiplierWord],
    ]:
        apply_pattern(pattern, RepeatedVolumeWord, sentences)
    return sentences

def number_tag(sentences: List[List[Word]]) -> List[List[Word]]:
    """Find numbers in sentences and return sentences with NumberWords.

    Args:
        sentences (List[List[Word]]): Sentences after tokenization and POS
            tagging.
    Returns:
        List[List[Word]]: Sentences with numbers converted to NumberWords.
    """
    for i in range(len(sentences)):
        sentence = sentences[i]
        for j in range(len(sentence)):
            word = sentence[j]
            if type(word) == Word:
                try:
                    float(word.word.lstrip('~'))
                    sentences[i][j] = NumberWord(word)
                except ValueError:
                    pass
    return sentences

def unit_tag(sentences: List[List[Word]]) -> List[List[Word]]:
    """Find units in sentences and return sentences with UnitWords.

    Args:
        sentences (List[List[Word]]): Sentences after tokenization and POS
            tagging.
    Returns:
        List[List[Word]]: Sentences with units converted to UnitWords.
    """
    units = [
        (TIME_UNITS, TimeUnitWord),
        (MOL_UNITS, MolUnitWord),
        (TEMP_UNITS, TempUnitWord),
        (VOLUME_UNITS, VolumeUnitWord),
        (CONC_UNITS, ConcUnitWord),
        (MASS_UNITS, MassUnitWord),
        (PERCENT_UNITS, PercentUnitWord),
        (EQUIVALENTS_UNITS, EquivalentsUnitWord),
        (PRESSURE_UNITS, PressureUnitWord),
        (STIR_SPEED_UNITS, StirSpeedUnitWord),
        (LENGTH_UNITS, LengthUnitWord),
        (MOL_PERCENT_UNITS, MolPercentUnitWord),
    ]
    apply_pattern(['mol', '%'], MolPercentUnitWord, sentences)
    for i in range(len(sentences)):
        sentence = sentences[i]
        for j in range(len(sentence)):
            word = sentence[j]
            for unit_list, unit_class in units:
                if type(word) == Word and word.word in unit_list:
                    sentences[i][j] = unit_class(word)
    return sentences

def ratio_tag(sentences: List[List[Word]]) -> List[List[Word]]:
    """Find ratios (i.e. '1:1 mixture') in sentences and return sentences with
    RatioWords.

    Args:
        sentences (List[List[Word]]): Sentences after tokenization and POS
            tagging.
    Returns:
        List[List[Word]]: Sentences with ratios converted to RatioWords.
    """
    for i in range(len(sentences)):
        sentence = sentences[i]
        for j in range(len(sentence)):
            word = sentence[j]
            if type(word) == Word:
                if re.match(ratio_regex_pattern, word.word):
                    ratio_word = RatioWord([word])
                    sentence[j] = ratio_word
    return sentences

def get_quantity_group_patterns() -> List[Union[Word, str]]:
    """Return patterns corresponding to groups of quantities, i.e. stuff like
    '(30 mg, 0.02 mol)'.

    Returns:
        List[Union[Word, str]]: Patterns corresponding to groups of quantities.
    """
    single_quantity_pattern = ['(', QuantityWord, ')']
    patterns = [single_quantity_pattern]
    for i in range(1, 6):
        # [Quantity, Quantity...]
        pattern = ['(', Optional(NumberWord), Optional(',')]
        for _ in range(i):
            pattern.extend([QuantityWord, ','])
        pattern.pop()

        # Allow suppliers to be given in QuantityGroupWords
        new_pattern = copy.deepcopy(pattern)
        new_pattern.extend([',', SupplierWord])

        pattern.append(')')
        new_pattern.append(')')

        abbreviation_pattern = copy.deepcopy(pattern)
        abbreviation_pattern.insert(1, ReagentNameWord)
        abbreviation_pattern.insert(2, ',')

        patterns.append(pattern)
        patterns.append(new_pattern)
        patterns.append(abbreviation_pattern)

        # [Quantity Quantity...]
        pattern = ['(']
        for _ in range(i):
            pattern.append(QuantityWord)
        pattern.pop()

        # Allow suppliers to be given in QuantityGroupWords
        new_pattern = copy.deepcopy(pattern)
        new_pattern.extend([',', SupplierWord])

        pattern.append(')')
        new_pattern.append(')')

        patterns.append(pattern)
        patterns.append(new_pattern)

    # Handle OrgSyn quantity groups written like 100 g. (0.67 mol)
    extra_patterns = []
    for pattern in patterns:
        new_pattern = copy.deepcopy(pattern)
        new_pattern.insert(0, QuantityWord)
        extra_patterns.append(new_pattern)
    patterns.extend(extra_patterns)

    patterns = sorted(patterns, key=lambda x: 1 / len(x))

    return patterns

def percent_in_solvent_tag(sentences: List[List[Word]]) -> List[List[Word]]:
    """Tag stuff like '40% in water'.

    Args:
        sentences (List[List[Word]]): Sentences to tag.

    Returns:
        List[List[Word]]: Sentences with words combined into
            PercentInSolventWord objects.
    """
    for pattern in [
        [PercentWord, 'in', ReagentNameWord],
        [ConcWord, 'in', ReagentNameWord],
        [MassWord, ',', MolWord, 'in', VolumeWord,
            Optional('of'), ReagentNameWord],
        [MassWord, 'in', VolumeWord, Optional('of'), ReagentNameWord],
    ]:
        apply_pattern(pattern, PercentInSolventWord, sentences)
    return sentences

def quantity_group_tag(sentences: List[List[Word]]) -> List[List[Word]]:
    """Tag groups of quantities as QuantityGroupWords
    i.e. stuff like '(30 mg, 0.02 mol)'.

    Args:
        sentences (List[List[Word]]): Sentences to tag groups of quantities.

    Returns:
        List[List[Word]]: Sentences with QuantityGroupWords added.
    """
    for pattern in get_quantity_group_patterns():
        apply_pattern(pattern, QuantityGroupWord, sentences)
    return sentences

def yield_tag(sentences: List[List[Word]]) -> List[List[Word]]:
    """Tag yields e.g. 90 % yield.

    Args:
        sentences (List[List[Word]]): Sentences to tag yields in.

    Returns:
        List[List[Word]]: Sentences with yields tagged.
    """
    for pattern in [
        [PercentWord, 'yield']
    ]:
        apply_pattern(pattern, YieldWord, sentences)
    return sentences

def ph_tag(sentences: List[List[Word]]) -> List[List[Word]]:
    """Tag pHs e.g. 'pH 5'

    Args:
        sentences (List[List[Word]]): Sentences to tag pHs in.

    Returns:
        List[List[Word]]: Sentences with pHs tagged.
    """
    for pattern in [
        ['pH', NumberWord]
    ]:
        apply_pattern(pattern, pHWord, sentences)
    return sentences

def bp_mp_tag(sentences: List[List[Word]]) -> List[List[Word]]:
    """Tag boiling points and melting points

    Args:
        sentences (List[List[Word]]): Sentences to tag.

    Returns:
        List[List[Word]]: Sentences with boiling points and melting points
            tagged.
    """
    for pattern, word_type in [
        (['b.', 'p.', TempWord], BPWord),
        (['b.p.', TempWord], BPWord),
        (['m.', 'p.', TempWord], MPWord),
        (['m.p.', TempWord], MPWord)
    ]:
        apply_pattern(pattern, word_type, sentences)
    return sentences
