import os
import pytest
from synthreader.tagging.reagent_names.probabilistic_search import p_phrase_is_reagent
HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, 'files', 'reagent_name_phrases.tsv')) as fileobj:
    lines = [line.strip() for line in fileobj.readlines()]
    test_phrases = []
    for line in lines:
        split_line = line.split('\t')
        if len(split_line) > 1:
            test_phrases.append((split_line[0], int(split_line[1])))
test_phrases.append(('menthol', 1))

@pytest.mark.unit
def test_probabilistic_reagent_name_tagging():
    scores = []
    correct = 0
    for phrase, label in test_phrases:
        print(f'Phrase: {phrase}')
        p = p_phrase_is_reagent(phrase, p_general_phrase_is_reagent=0.46)
        print(f'p: {p:.2f}\n')
        if p >= 0.5:
            if label == 1:
                correct += 1
            else:
                print(f'INCORRECT: {phrase}')
            # assert label == 1
        else:
            if label == 0:
                correct += 1
            else:
                print(f'INCORRECT: {phrase}')
                # assert label == 0
    #     scores.append(((correct / len(test_phrases)) * 100, i))
    # for item in sorted(scores, key=lambda x: x[0]):
    #     print(item)
    # print(f'Naive bayes Best: {max(scores, key=lambda x: x[0])}')
    print(f'Naive Bayes: {(correct / len(test_phrases)) * 100:.2f} %')
