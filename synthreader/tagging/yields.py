import copy
from ..utils import apply_pattern, trim_patterns
from ..words import YieldPhraseWord, QuantityGroupWord, QuantityWord

YIELD_PATTERNS = [
    ['yielding', QuantityWord],
    ['to', 'yield', QuantityWord],
    ['to', 'provide', QuantityWord],
    ['to', 'afford', QuantityWord],
    ['providing', QuantityWord],
    ['affording', QuantityWord],
]

extra_patterns = []
for pattern in YIELD_PATTERNS:
    extra_pattern = copy.deepcopy(pattern)
    extra_pattern[-1] = QuantityGroupWord
    extra_patterns.append(extra_pattern)
YIELD_PATTERNS.extend(extra_patterns)

def yield_phrase_tag(sentences, word_bank):
    for pattern in trim_patterns(YIELD_PATTERNS, word_bank):
        apply_pattern(pattern, YieldPhraseWord, sentences)
