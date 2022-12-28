from ..utils import apply_pattern
from ..words import SupplierWord

SUPPLIER_PATTERNS = [
    ['aldrich'],
    ['sigma', 'aldrich'],
    ['sigma-aldrich'],
    ['alfa', 'aesar'],
    ['alfa-aesar'],
]

def supplier_tag(sentences):
    for pattern in SUPPLIER_PATTERNS:
        apply_pattern(pattern, SupplierWord, sentences)
    return sentences
