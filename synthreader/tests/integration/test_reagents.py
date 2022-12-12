import pytest
from .generator import get_reagents
from synthreader.tagging import tag_synthesis

def test_reagents(test_info, tagged_synthesis=None):
    """Test that all reagents are found with quantities."""
    if not tagged_synthesis:
        tagged_synthesis = tag_synthesis(test_info['text'])
    reagents = get_reagents(tagged_synthesis)
    for correct_reagent in test_info['reagents']:
        assert correct_reagent in reagents
        for quantity in test_info['reagents'][correct_reagent]['quantities']:
            assert quantity in reagents[correct_reagent]['quantities']
