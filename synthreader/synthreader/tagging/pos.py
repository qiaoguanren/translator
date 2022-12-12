from typing import List
import nltk
import re

from ..words import Word

# Tactical replacements like in preprocessing, applied here so they are isolated
# to individual sentences.
SENTENCE_REPLACEMENTS: List[str] = [
    # Discard extra information about equipment e.g.
    # '''A 250-mL, three-necked, round-bottomed flask equipped with a septum,
    # a 3.8 cm Teflon-coated magnetic stir bar and a condenser connected to a
    # drying tube containing Drierite® is charged...'''
    # should become
    # '''A 250-mL, three-necked, round-bottomed flask is charged...'''
    (r'(is )?(equipped|fitted) (for|with) (.*?(?=(is|are|charged|placed|dried|and dried) ))', r'\1'),  # noqa: E501
    (r' is and ', ' is '),  # Bug introduced by pattern above
    # (r'(is )?(equipped|fitted) (for|with) (.*?(?=are ))', r''),
    # (r'(is )?(equipped|fitted) (for|with) (.*?(?=charged ))', r''),
    # (r'(is )?(equipped|fitted) (for|with) (.*?(?=placed ))', r''),
    # (r'(is )(equipped|fitted) (with|for) (.*?(?=charged ))', r''),
]

def tokenize_and_pos_tag(synthesis_text: str) -> List[List[Word]]:
    """
    Split synthesis text into sentences/words and get part-of-speech tags for
    each word.

    Args:
        synthesis_text (str): Synthetic procedure description to tokenize and
            assign part-of-speech tags.

    Returns:
        List[List[Word]: List of sentences, which are lists of Word objects.
    """
    sentences = nltk.sent_tokenize(synthesis_text)
    for i in range(len(sentences)):
        for regex, replacement in SENTENCE_REPLACEMENTS:
            sentences[i] = re.sub(regex, replacement, sentences[i])

    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    for i in range(len(sentences)):
        for j in range(len(sentences[i])):
            word, pos_tag = sentences[i][j]
            sentences[i][j] = Word(word, pos_tag)

    return sentences
