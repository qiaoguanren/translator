from typing import List
from ..words import (
    Word, TechniqueWord, TimeWord, TempWord, PressureWord)
from ..words.modifiers import (
    TimeModifier, TemperatureModifier, PressureModifier)
from .preprocessing import preprocess
from .pos import tokenize_and_pos_tag
from .auxiliary_verbs import auxiliary_verb_tag
from .quantities import quantity_tag, quantity_group_tag, percent_in_solvent_tag
from .reagents import reagent_tag, reagent_placeholder_tag
from .reagent_names import reagent_name_tag
from .solutions import solution_tag
from .mixtures import mixture_tag
from .actions import (
    past_tense_action_tag, present_tense_action_tag, discontinue_action_tag)
from .techniques import technique_tag
from .vessels import vessel_tag, expand_vessels, vessel_component_group_tag
from .reagent_groups import reagent_group_tag
from .modifiers import (
    pattern_modifier_tag,
    non_pattern_modifier_tag,
)
from .colors import color_tag
from .suppliers import supplier_tag
from .details import details_tag
from .yields import yield_phrase_tag
from .wildcard import wildcard_tag
from ..utils import apply_pattern

def tag_synthesis(synthesis_text: str) -> List[List[Word]]:
    s = preprocess(synthesis_text)
    sentences = tokenize_and_pos_tag(s)
    word_bank = set([word.word.lower() for sent in sentences for word in sent])

    auxiliary_verb_tag(sentences)
    technique_tag(sentences, word_bank)
    vessel_tag(sentences, word_bank)
    supplier_tag(sentences)
    color_tag(sentences, word_bank)
    past_tense_action_tag(sentences, word_bank)
    quantity_tag(sentences)
    vessel_tag(sentences, word_bank)
    vessel_component_group_tag(sentences)
    expand_vessels(sentences)

    # This has to be done to match '40 % in water' as ReagentName needed to tag
    # PercentInSolventWord and then this has to become part of QuantityGroups.
    pattern_modifier_tag(sentences, word_bank)
    quantity_group_tag(sentences)
    apply_pattern([TimeWord], TimeModifier, sentences)

    reagent_placeholder_tag(sentences, word_bank)
    reagent_name_tag(sentences)
    percent_in_solvent_tag(sentences)
    quantity_group_tag(sentences)

    reagent_tag(sentences)
    reagent_group_tag(sentences)
    solution_tag(sentences)
    mixture_tag(sentences)
    reagent_group_tag(sentences)
    pattern_modifier_tag(sentences, word_bank)
    yield_phrase_tag(sentences, word_bank)
    non_pattern_modifier_tag(sentences)
    # Present tense actions tagged after modifiers so 'with stirring' tagged as
    # modifier not as action.
    convert_unused_technique_words(sentences)
    present_tense_action_tag(sentences, word_bank)
    details_tag(sentences)
    # Second modifier tag for present tense actions
    pattern_modifier_tag(sentences, word_bank)
    non_pattern_modifier_tag(sentences)
    discontinue_action_tag(sentences)
    wildcard_tag(sentences)
    apply_pattern([TempWord], TemperatureModifier, sentences)
    apply_pattern([PressureWord], PressureModifier, sentences)
    return sentences

def convert_unused_technique_words(
        sentences: List[List[Word]]) -> List[List[Word]]:
    """If TechniqueWords are left after modifier tagging, they should be
    converted back to normal Words so that present tense action tagging can use
    them. This was added to deal with '...followed by washing and vacuum
    filtration', where vacuum filtration wasn't being tagged as an action.

    Args:
       sentences (List[List[Word]]): Sentences to convert TechniqueWords back to
           normal Words.

    Returns:
        List[List[Word]]: Sentences with TechniqueWords converted back to normal
            Words.
    """
    i = len(sentences) - 1
    while i > 0:
        sentence = sentences[i]
        j = len(sentence) - 1
        while j > 0:
            word = sentence[j]
            if type(word) == TechniqueWord:
                sentence.pop(j)
                for word in reversed(word.words):
                    sentence.insert(j, word)
            j -= 1
        i -= 1
    return sentences
