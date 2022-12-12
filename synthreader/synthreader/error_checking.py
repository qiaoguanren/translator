import re
from .words.action_words import Action

IGNORE_UNTAGGED_PHRASES = [
    '.',
    ',',
    ', and',
    'and',
    'but',
    'to',
    'of',
    'in',
]

def get_errors(tagged_synthesis):
    errors = {
        'non_action_phrases': get_untagged_phrases(tagged_synthesis),
    }
    return errors

def get_untagged_phrases(tagged_synthesis):
    phrase = []
    phrases = []
    for sent in tagged_synthesis:
        for word in sent:
            if isinstance(word, Action):
                if phrase:
                    phrases.append(tidy_phrase(' '.join(phrase)))
                    phrase = []
            else:
                phrase.append(str(word))
        if phrase:
            phrases.append(tidy_phrase(' '.join(phrase)))
            phrase = []
    phrases = [
        phrase
        for phrase in list(set(phrases))
        if phrase not in IGNORE_UNTAGGED_PHRASES
    ]
    return phrases

def tidy_phrase(phrase):
    replacements = [
        (r' ([\.\,])', r'\1'),
    ]
    for regex, replacement in replacements:
        phrase = re.sub(regex, replacement, phrase)
    return phrase.strip()
