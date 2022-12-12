from ...utils import apply_pattern
from ...utils.pattern_matcher import Regexp
from ...words import ReagentNameFragmentWord

REAGENT_NAME_FRAGMENT_PATTERNS = [
    ['(', '+', ')'],
    ['(', '-', ')'],
    ['α', ',', 'α'],
    ['(', Regexp(r'[0-9](R|S)'), ',', Regexp(r'[0-9](R|S)'), ')'],
    ['(', Regexp(r'[0-9](R|S),[0-9](R|S)'), ')'],
]

def reagent_name_fragment_tag(sentences):
    for pattern in REAGENT_NAME_FRAGMENT_PATTERNS:
        apply_pattern(pattern, ReagentNameFragmentWord, sentences)
