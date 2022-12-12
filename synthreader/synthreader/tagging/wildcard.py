from ..utils import apply_pattern, Optional, Pos
from ..words import ReagentPlaceholderWord
from ..words.modifiers import Modifier

WILDCARD_PATTERNS = [
    ([Pos('IN'), Optional(Pos('DT')), Optional(Pos('JJ')),
      Pos('NN'), Optional(Pos('NNS'))], Modifier),
    # 'until complete dissolution had occurred'
    ([Pos('IN'), Optional(Pos('DT')), Optional(Pos('JJ')),
      Pos('NN'), Pos('VBD'), Pos('VBN')], Modifier),
    ([Pos('DT'), Optional(Pos('JJ')), Pos('NN')], ReagentPlaceholderWord)
]

def wildcard_tag(sentences):
    """At end of tagging, tag unmatched phrases with certain POS patterns as
    generic types so that interpreting pattern matching is not messed up.

    Args:
        sentences (sentences): Sentences to tag POS patterns with generic types.
    """
    for pattern in WILDCARD_PATTERNS:
        apply_pattern(pattern[0], pattern[1], sentences)
