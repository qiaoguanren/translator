from ..words import DetailsWord, ActionWord, VolumeWord
from ..words.modifiers import TemperatureModifier, TimeModifier

def details_tag(sentences):
    for sentence in sentences:
        j = 0
        brackets_open = []
        which_commas_open = []
        while j < len(sentence):
            word = sentence[j]
            if str(word) == '(':
                brackets_open.append(j)

            elif (str(word) == ','
                  and j + 1 < len(sentence)
                  and str(sentence[j + 1]) == 'which'):
                which_commas_open.append(j)

            elif str(word) == ')':
                try:
                    opening_pos = brackets_open.pop()
                    if not brackets_open:
                        sentence_slice = sentence[opening_pos:j + 1]
                        details = DetailsWord(sentence_slice)
                        if not any([
                            isinstance(
                                word,
                                (TemperatureModifier, TimeModifier, VolumeWord)
                            )
                            for word in sentence_slice
                        ]):
                            del sentence[opening_pos:j + 1]
                            sentence.insert(opening_pos, details)
                            j = opening_pos
                except IndexError:
                    pass

            elif str(word) == ',':
                try:
                    opening_pos = which_commas_open.pop()
                    if not which_commas_open:
                        sentence_slice = sentence[opening_pos:j + 1]
                        # Only make DetailsWord if no ActionWords will be lost
                        if not any([
                            isinstance(word, (ActionWord))
                            for word in sentence_slice
                        ]):
                            details = DetailsWord(sentence_slice)
                            del sentence[opening_pos:j + 1]
                            sentence.insert(opening_pos, details)
                            j = opening_pos
                except IndexError:
                    pass

            j += 1
    return sentences
