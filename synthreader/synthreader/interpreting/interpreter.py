import copy
from typing import List
import re
from ..logging import get_logger
from .constants import (
    MODIFIER_SEARCH_CONTINUE_WORDS,
    EXTRACT_ACTION_PATTERNS,
    MEANINGLESS_WORDS,
)
from ..words import (
    Action,
    Word,
    ActionWord,
    ReagentWord,
    ReagentPlaceholderWord,
    ReagentGroupWord,
    SolutionWord,
    WashWord,
    DryWord,
    AddWord,
    WashSolidWord,
    FilterWord,
    IsolateWord,
    VesselWord,
    VesselComponentGroupWord,
    AbstractReagentWord,
    DiscontinueWord,
    AuxiliaryVerbWord,
    HeatWord,
    PlaceWord,
    StirWord,
    WaitWord,
    CoolWord,
    QuantityGroupWord,
    ExtractWord,
    TempWord,
    VolumeWord,
    EvacuateWord,
    PurifyWord,
    TechniqueWord,
)

from ..words.modifiers import (
    Modifier,
    TemperatureModifier,
    ReagentModifier,
    TimeModifier,
    DetailsModifier,
    StirringModifier,
    MethodModifier,
    AdditionModifier,
)
from ..utils import apply_pattern

def combine_actions_and_modifiers(
        sentences: List[List[Word]]) -> List[List[Word]]:
    """
    Squash all Modifiers into their respective ActionWords.

    Args:
        sentences (List[List[Word]]): Sentences to look for ActionWords in and
            Modifiers in.

    Returns:
        List[List[Word]]: Sentences with Modifiers contained in their parent
            ActionWords.
    """
    for i in range(len(sentences)):
        sentence = sentences[i]
        j = 0
        while j < len(sentence):
            word = sentence[j]
            # Don't apply modifiers to discontinue word as actions that word
            # applies to are already contained in the word. Bit hacky.
            if (isinstance(word, (VesselWord, ActionWord, TechniqueWord))
                    and not type(word) == DiscontinueWord):
                k = 1
                modifiers_start = j
                is_modified = False
                new_modifier_group = False
                while j + k < len(sentence):
                    # Check for modifier or reagent as present tense verbs can
                    # be followed by reagents e.g. '...by washing the solids...'
                    if (isinstance(sentence[j + k], Modifier)
                        or (isinstance(sentence[j + k], ReagentPlaceholderWord)
                            and str(sentence[j + k - 1]).endswith('ing'))):
                        k += 1
                        is_modified = True
                        continue
                    # This is a massive hack to get 'to X at 70 C was added Y
                    # over 45 mins.' Problem was modifiers after Y aren't picked
                    # up.
                    elif (str(sentence[j + k - 1]).endswith('ed')
                          and isinstance(sentence[j + k], AbstractReagentWord)):
                        k += 1
                        is_modified = True
                        modifiers_start += 1
                        continue
                    elif str(sentence[j + k]) in MODIFIER_SEARCH_CONTINUE_WORDS:
                        k += 1
                        continue
                    elif (str(sentence[j + k]) in ['and', 'then']
                          and is_modified):
                        k += 1
                        new_modifier_group = j + k
                        continue
                    else:
                        break

                if is_modified:
                    # For sentences like
                    # '''The reaction mixture is stirred vigorously at bath
                    #    temperature (approximately 0 °C) for 2 h and at room
                    #    temperature for 22 h.'''
                    # Modifiers need to be split into two groups and extra
                    # action added with second modifier group.
                    if new_modifier_group and any(
                        [isinstance(slice_word, Modifier)
                         for slice_word in sentence[new_modifier_group: j + k]]
                    ):
                        # Cut off any non modifiers from end i.e. ',', 'and',
                        # etc.
                        while (j + k - 1 >= 0
                               and not isinstance(sentence[j + k - 1], Modifier)
                               ):
                            k -= 1
                        slice1 = sentence[modifiers_start
                                          + 1: new_modifier_group - 1]
                        slice2 = sentence[new_modifier_group: j + k]
                        word.process_modifiers(slice1)

                        if not all([type(mod) == Modifier for mod in slice2]):
                            del sentence[modifiers_start + 1: j + k]
                            new_word = copy.deepcopy(word)
                            new_word.modifiers = []
                            new_word.process_modifiers(slice2)
                            sentence.insert(modifiers_start + 1, new_word)
                            sentence.insert(modifiers_start + 1,
                                            Word('and', 'CC'))

                            # Grab any modifiers from initial word that don't
                            # conflict with new word modifiers
                            new_word_mod_types = [type(mod)
                                                  for mod in new_word.modifiers]
                            banned_mod_types = new_word_mod_types + \
                                [DetailsModifier]
                            extra_mods = []
                            for mod in word.modifiers:
                                if type(mod) not in banned_mod_types:
                                    extra_mods.append(mod)
                            new_word.process_modifiers(extra_mods)
                            j += 2
                        else:
                            del sentence[modifiers_start
                                         + 1: new_modifier_group - 1]

                    else:
                        # Cut off any non modifiers from end i.e. ',', 'and',
                        # etc.
                        while (j + k - 1 >= 0
                               and not isinstance(sentence[j + k - 1], Modifier)
                               ):
                            k -= 1
                        word.process_modifiers(
                            sentence[modifiers_start + 1: j + k])
                        del sentence[modifiers_start + 1: j + k]
            j += 1
    return sentences

def combine_actions_and_modifiers_backwards(
        sentences: List[List[Word]]) -> List[List[Word]]:
    """Combine actions and modifiers in sentences like

    'In air, to a solution of 2,6-diisopropylaniline
    (197 g, 1.00 mol, 2.00 equiv) and HOAc (1.0 mL, 0.018 mol, 0.035 equiv) in
    250 mL of MeOH at 50°C in a flask was added a solution of glyoxal
    (73 g, 0.50 mol, 1.0 equiv) in 250 mL of MeOH.'

    Format is Modifier, Modifier... was Action Reagent.

    Args:
        sentences (List[List[Word]]): Sentences to combine actions and
            modifiers.

    Returns:
        List[List[Word]]: Sentences with actions and modifiers combined.
    """
    for i in range(len(sentences)):
        sentence = sentences[i]
        j = 0
        while j < len(sentence):
            word = sentence[j]

            if isinstance(word, ActionWord) and str(word).endswith('ed'):
                if j > 0:
                    # Word is past tense, next word is AbstractReagentWord and
                    # previous word is auxiliary word, see sentence in docstring
                    if (type(sentence[j - 1]) == AuxiliaryVerbWord
                        and j + 1 < len(sentence)
                            and isinstance(
                                sentence[j + 1], AbstractReagentWord)):
                        k = j - 1
                        while (k - 1 >= 0
                               and (sentence[k - 1] in ['and', ',']
                                    or isinstance(sentence[k - 1], Modifier))):
                            k -= 1
                        if k < j - 1:
                            word.process_modifiers(
                                [item for item in sentence[k: j]
                                 if isinstance(item, Modifier)])
                            del sentence[k: j]
                            j = k

                    # ..., then slowly acidified to pH 5. Combine slowly into
                    # acidify action.
                    elif isinstance(sentence[j - 1], Modifier):
                        k = j - 1
                        word.process_modifiers(sentence[k:j])
                        del sentence[k]
                        j = k
            j += 1
    return sentences

def fill_in_modifier_blanks(sentences: List[List[Word]]) -> List[List[Word]]:
    """If modifiers refer to something else in sentence, find this item in the
    sentence and update the modifier attributes accordingly.

    Args:
        sentences (List[Word]): List of List of Words corresponding to
            sentences.
    """
    reagents_grab_unbound_quantities(sentences)

    for i, sentence in enumerate(sentences):
        for j, word in enumerate(sentence):
            # Deal with 'at this temperature' by looking back to get temperature
            # which is being referred to.
            # 'The reaction mixture was warmed to 70−73 °C over 20 min and
            #  mechanically stirred at this temperature for 3 h.'
            if (type(word) == TemperatureModifier
                    and str(word) == 'at this temperature'):
                look_back_word_i = j
                look_back_sent_i = i
                found_temp = False
                while look_back_sent_i >= 0:
                    while look_back_word_i >= 0:
                        look_back_word_i -= 1
                        look_back_word = sentences[
                            look_back_sent_i][look_back_word_i]
                        if (type(look_back_word) == TemperatureModifier
                                and look_back_word.temp is not None):
                            word.temp = look_back_word.temp
                            # If inexact 'heated using an oil bath' modifier is
                            # found, keep looking for exact one, but only to
                            # start of current sentence.
                            if 'bath' in str(look_back_word):
                                found_temp = 'inexact'
                                continue
                            else:
                                found_temp = True
                                break
                    if found_temp:
                        break

                    else:
                        look_back_sent_i -= 1
                        look_back_word_i = len(sentences[look_back_sent_i])
    return sentences

def grab_unbound_modifiers(sentences: List[List[Word]]) -> List[List[Word]]:
    """Grab modifiers that have been missed in previous modifier combining.
    This is very vague as the modifiers are just looked for anywhere in the
    sentence, so is only applied to certain actions where any modifier is
    probably better than None. I.e. Wait action needs a time.

    Args:
        sentences (List[List[Word]]): Sentences to grab unbound  modifiers

    Returns:
        List[List[Word]]: Sentences with unbound modifiers added to action
            words.
    """
    # Rules follow format
    # (target_type, target_modifier_to_grab, direction_to_look_for_modifier)
    grab_rules = [
        (WaitWord, TimeModifier, ['forward']),
    ]

    for sentence in sentences:
        for j, word in enumerate(sentence):
            for target_type, modifier_type, search_directions in grab_rules:
                # Word is target type and doesn't have target modifier type.
                if (type(word) == target_type
                    and not any([type(modifier) == modifier_type
                                 for modifier in word.modifiers])):

                    # Forward search for missing modifier
                    if 'forward' in search_directions:
                        k = j + 1
                        while k < len(sentence):
                            if type(sentence[k]) == modifier_type:
                                word.modifiers.append(sentence[k])
                                break
                            k += 1

                    # Backward search for missing modifier
                    if 'back' in search_directions:
                        k = j - 1
                        while k >= 0:
                            if type(sentence[k]) == modifier_type:
                                word.modifiers.append(sentence[k])
                                break
                            k -= 1
    return sentences

def reagents_grab_unbound_quantities(
        sentences: List[List[Word]]) -> List[List[Word]]:
    """If a reagnet doesn't have a quantity, search elsewhere in sentence for
    unbound quantities.

    Args:
        sentences (List[List[Word]]): Sentences to associate reagents with
            unbound quantities.

    Returns:
        List[List[Word]]: Sentences with reagents associated with unbound
            quantities.
    """
    for sentence in sentences:
        for j, word in enumerate(sentence):
            for modifier_type, word_type in [
                (ReagentModifier, QuantityGroupWord),
                (ReagentModifier, VolumeWord),
            ]:
                # Word is target type and doesn't have target modifier type.
                if (type(word) == modifier_type
                    and len(word.reagents) == 1
                    and not any([type(subword) == word_type
                                 for subword in word.reagents[0].words])):

                    # Forward search for missing word
                    k = j + 1
                    while k < len(sentence):
                        if type(sentence[k]) == word_type:
                            word.reagents[0].words.append(sentence[k])
                            word.reagents[0].__init__(word.reagents[0].words)
                            break

                        elif (type(sentence[k]) == DetailsModifier
                              and (type(sentence[k].words[0].words[0])
                                   == word_type)):
                            word.reagents[0].words.append(
                                sentence[k].words[0].words[0])
                            word.reagents[0].__init__(word.reagents[0].words)
                            break
                        k += 1

                    # Backward search for missing word
                    k = j - 1
                    while k >= 0:
                        if type(sentence[k]) == word_type:
                            word.reagents[0].words.append(sentence[k])
                            word.reagents[0].__init__(word.reagents[0].words)
                            break

                        elif (type(sentence[k]) == DetailsModifier
                              and (type(sentence[k].words[0].words[0])
                                   == word_type)):
                            word.reagents[0].words.append(
                                sentence[k].words[0].words[0])
                            word.reagents[0].__init__(word.reagents[0].words)
                            break
                        k -= 1
    return sentences

def remove_meaningless_words(sentences: List[List[Word]]) -> List[List[Word]]:
    """Remove meaningless words that don't really add any meaning and makes
    patterns harder to match i.e. 'was then rinsed' -> 'was rinsed'.

    Args:
        sentences (List[List[Word]]): Sentences to remove meaningless words
            from.

    Returns:
        List[List[Word]]: Sentences with meaningless words removed.
    """
    i = len(sentences) - 1
    while i >= 0:
        sentence = sentences[i]
        j = len(sentence) - 1
        while j >= 0:
            word = sentences[i][j]
            for meaningless_word in MEANINGLESS_WORDS:
                # Meaningless word is more than one words e.g.
                # 'which precipitated'
                if type(meaningless_word) == list:
                    if str(word) == meaningless_word[0]:
                        match = True
                        for k in range(len(meaningless_word)):
                            if (not (j + k < len(sentence)
                                     and str(sentence[j + k])
                                     == meaningless_word[k])):
                                match = False
                                break
                        if match:
                            for _ in range(len(meaningless_word)):
                                sentences[i].pop(j)
                            break

                # Meaningless word is single word
                else:
                    if str(word) == meaningless_word:
                        sentences[i].pop(j)
                        break

                    # 'continued stirring' -> 'stirring'
                    elif (str(word) == 'continued'
                          and j + 1 < len(sentence)
                          and isinstance(sentence[j + 1], ActionWord)):
                        sentences[i].pop(j)
                        break
            j -= 1
        i -= 1
    return sentences

def prioritise_competing_temperature_modifiers(
        sentences: List[List[Word]]) -> List[List[Word]]:
    """If something is heated to 'to 150C using an oil bath', the 150C exact
    temp modifier should be kept and the oil bath inexact temp modifier should
    be discarded.

    Args:
        sentences (List[List[Word]]): Sentences to handle competing temp
            modifiers

    Returns:
        List[List[Word]]: Sentences with all groups of competing temp modifiers
            narrowed down to one.
    """
    for sentence in sentences:
        for word in sentence:
            if isinstance(word, ActionWord):
                if (len([modifier
                         for modifier in word.modifiers
                         if type(modifier) == TemperatureModifier]) > 1):
                    non_specific = []
                    specific = []
                    reflux = []
                    for i in reversed(range(len(word.modifiers))):

                        modifier = word.modifiers[i]
                        if type(modifier) == TemperatureModifier:
                            if any([
                                type(subword) in [TempWord, QuantityGroupWord]
                                for subword in modifier.words
                            ]):
                                specific.append(i)
                            elif 'reflux' in str(modifier):
                                reflux.append(i)
                            else:
                                non_specific.append(i)
                    if specific:
                        for i in reversed(sorted(non_specific + reflux)):
                            word.modifiers.pop(i)
                    elif reflux:
                        for i in reversed(non_specific):
                            word.modifiers.pop(i)

    return sentences

def ignore_details(sentences: List[List[Word]]) -> List[List[Word]]:
    """Remove all DetailsModifiers so they don't mess up the action list pattern
    matching.

    Args:
        sentences (List[List[Word]]): Tagged sentences

    Returns:
        List[List[Word]]: Tagged sentences with DetailsModifiers removed.
    """
    for sentence in sentences:
        for j in reversed(range(len(sentence))):
            if type(sentence[j]) == DetailsModifier:
                sentence.pop(j)
    return sentences

def split_reagent_groups(sentences: List[List[Word]]) -> List[List[Word]]:
    """Split ReagentGroupWords if it looks like each half of reagent group word
    belongs to a different verb.
    E.g. 'To the mixture is added X and Y is removed by filtration.'
    'X and Y' shouldn't be a reagent group.

    Args:
        sentences (List[List[Word]]): Sentences to split incorrect reagent
            groups

    Returns:
        List[List[Word]]: Sentences with incorrect reagent groups split.
    """
    for sentence in sentences:
        j = 0
        while j < len(sentence):
            word = sentence[j]
            if type(word) == ReagentGroupWord:
                if len(word.reagents) == 2:
                    action_before, action_after = False, False

                    if j - 1 >= 0:
                        if isinstance(sentence[j - 1], ActionWord):
                            action_before = True
                        elif str(sentence[j - 1]) in [',', 'and']:
                            j += 1
                            continue

                    if (not action_before
                        and j - 2 >= 0
                            and isinstance(sentence[j - 2], ActionWord)):
                        action_before = True

                    if (j + 1 < len(sentence)
                            and isinstance(sentence[j + 1], ActionWord)):
                        action_after = True

                    if (not action_after
                        and j + 2 < len(sentence)
                            and isinstance(sentence[j + 2], ActionWord)):
                        action_after = True

                    if action_before and action_after:
                        first_reagent = word.reagents[0]
                        second_reagent = word.reagents[1]
                        sentence.pop(j)
                        sentence.insert(j, second_reagent)
                        sentence.insert(j, 'and')
                        sentence.insert(j, first_reagent)
                        j += 2
            j += 1
    return sentences

def pop_adverbs(sentences: List[List[Word]]) -> List[List[Word]]:
    """Convert 'slowly acidified' to 'acidified' to simplify things. If word
    before verb is a recognised modifier then add it to actions modifier list.
    """
    for sentence in sentences:
        i = len(sentence) - 1
        while i >= 0:
            word = sentence[i]
            if isinstance(word, ActionWord):
                if i - 1 >= 0:
                    prev_word = sentence[i - 1]
                    if isinstance(prev_word, Modifier):
                        if (len(prev_word.words) == 1
                            and type(prev_word.words[0]) == Word
                                and prev_word.words[0].pos.startswith('RB')):
                            word.process_modifiers([sentence.pop(i - 1)])
                            i -= 1

                    elif (type(prev_word) == Word
                          and prev_word.pos.startswith('RB')
                          and prev_word.word not in ['also']):
                        sentence.pop(i - 1)
                        i -= 1
            i -= 1
    return sentences


def preprocess_tagged_sentences(
        sentences: List[List[Word]]) -> List[List[Word]]:
    """Perform a variety of tasks to prepare the tagged sentences for pattern
    matching to extract the action list.

    Args:
        sentences (List[List[Word]]): Tagged sentences

    Returns:
        List[List[Word]]: Sentences prepared for action list pattern matching.
    """
    pop_adverbs(sentences)
    fill_in_modifier_blanks(sentences)
    combine_actions_and_modifiers(sentences)
    combine_actions_and_modifiers_backwards(sentences)
    grab_unbound_modifiers(sentences)
    prioritise_competing_temperature_modifiers(sentences)
    remove_meaningless_words(sentences)
    ignore_details(sentences)
    split_reagent_groups(sentences)
    return sentences

def postprocess_action_list(action_list: List[Action]) -> List[Action]:
    action_list = grab_modifiers_from_previous_actions(action_list)
    action_list = [action for action in action_list if type(
        action.action) != ActionWord]
    action_list = order_duplicate_additions(action_list)
    action_list = sort_addition_funnels(action_list)
    sort_wash_extract_ambiguity(action_list)
    return action_list

def sort_wash_extract_ambiguity(action_list):
    """'The aqueous layer is separated and washed with Et2O (3 x 150 mL).
    The combined organic layers are washed sequentially'

    Wash should be interpreted as extract.
    """
    for i in range(len(action_list)):
        if i > 0:
            action = action_list[i]
            prev_action = action_list[i - 1]
            if (type(prev_action.action) == WashWord
                    and type(action.action) == WashWord):
                # Washing aq with org, then extracting org. First wash should be
                # treated as extraction
                if ('aqueous' in str(prev_action.subject)
                        and 'organic' in str(action.subject)):
                    prev_action.action = ExtractWord(prev_action.words)
    return action_list

def sort_addition_funnels(action_list):
    """'The addition funnel was charged with X, which is then added...'
    X should be transferred as the subject to the second Add action and the
    first add action should be removed.
    """
    pops = []
    for i, action in enumerate(action_list):
        if type(action.action) == AddWord:
            if (i + 1 < len(action_list)
                    and type(action_list[i + 1].action) == AddWord):
                next_action = action_list[i + 1]
                # Don't allow big long vessel descriptions that include
                # 'addition funnel'
                if re.match(
                    r'([aA]n|[tT]he) (same )?addition funnel',
                    str(action.subject)
                ):
                    for mod in action.modifiers:
                        if type(mod) == ReagentModifier:
                            next_action.subject = mod.reagents[0]
                            pops.append(i)
    for i in reversed(pops):
        action_list.pop(i)
    return action_list

def grab_modifiers_from_previous_actions(action_list):
    previous_action_modifier_grabs = {
        CoolWord: [
            {
                'modifier': TemperatureModifier,
                'filter': lambda phrase: 'allowed' in phrase,
                'modifier_filter': lambda modifier: modifier.temp > 25
            },
            # If previous action involves adding water bath, this should trigger
            # active cooling rather than the default inactive cooling for an
            # 'allowed to cool' CoolWord.
            # e.g.
            # '''...then the oil bath is removed and replaced with a room
            # temperature water bath. The vigorously stirred reaction mixture is
            # allowed to cool to 28°C over 15 min...'''
            # Because water bath is explicitly mentioned active cooling should
            # be used. Inclusion of MethodModifier triggers this in action
            # sanitizer.
            {
                'modifier': MethodModifier,
                'filter': lambda phrase: (
                    'allowed' not in phrase and 'left' not in phrase),
                'modifier_filter': lambda modifier: (
                    'water bath' not in str(modifier))
            },
        ],
        HeatWord: [
            {
                'modifier': TemperatureModifier,
                'filter': lambda phrase: 'allowed' in phrase,
                'modifier_filter': lambda modifier: modifier.temp < 20
            },
        ]
    }
    # If action is missing a critical modifier, try and take it from the
    # previous.
    # This was written to handle the following:
    # ...and placed in an ice bath (Note 4). After the reaction flask is cooled
    # for 10 min...
    # The 'cooled for 10 mins' should grab the 'in an ice bath' temperature
    # modifier.
    for i, action in enumerate(action_list):
        if type(action.action) in previous_action_modifier_grabs:
            for modifier_grab_info in previous_action_modifier_grabs[
                    type(action.action)]:

                if modifier_grab_info['filter'](str(action.action)):
                    continue

                modifier_type = modifier_grab_info['modifier']

                if not any([type(modifier) == modifier_type
                            for modifier in action.modifiers]):
                    if i - 1 >= 0:
                        prev_action = action_list[i - 1]
                        prev_step_modifiers = [
                            modifier
                            for modifier in prev_action.modifiers
                            if type(modifier) == modifier_type
                        ]
                        if prev_step_modifiers:
                            if not modifier_grab_info['modifier_filter'](
                                    prev_step_modifiers[0]):
                                action.modifiers.append(prev_step_modifiers[0])
    return action_list


def order_duplicate_additions(action_list):
    i = 0
    while i < len(action_list):
        action = action_list[i]
        if i + 1 < len(action_list):
            next_action = action_list[i + 1]
            if type(action.subject) not in [ReagentWord, SolutionWord]:
                i += 1
                continue
            if (type(next_action.action) in [AddWord, PlaceWord]
                    and type(action.action) in [AddWord, PlaceWord]):
                if (action.subject is next_action.subject
                        and not any([
                            type(mod) == ReagentModifier
                            for mod in next_action.modifiers
                        ])):
                    USEFUL_MODIFIERS = [TemperatureModifier,
                                        TimeModifier, AdditionModifier]
                    score = len([mod for mod in action.modifiers
                                 if type(mod) in USEFUL_MODIFIERS])
                    next_score = len([mod for mod in next_action.modifiers
                                      if type(mod) in USEFUL_MODIFIERS])
                    if next_score > score:
                        action_list.pop(i)
                    else:
                        action_list.pop(i + 1)
        i += 1
    return action_list


def extract_actions(sentences: List[List[Word]]) -> List[Action]:
    """Convert sentences into list of Actions.

    Args:
        sentences (List[List[Word]]): Sentences to convert into list of actions.

    Returns:
        List[Action]: List of actions extracted from sentences.
    """
    logger = get_logger()
    preprocess_tagged_sentences(sentences)

    action_sentences = sentences
    # Convert Action patterns into Action objects.
    for pattern, subject_indexes, action_indexes in EXTRACT_ACTION_PATTERNS:
        apply_pattern(
            pattern,
            lambda words: [
                Action(subject=words[subject_indexes[pos]],
                       action=words[i],
                       words=words,
                       action_order_pos=pos,)
                for pos, i in enumerate(action_indexes)
            ],
            action_sentences
        )

    # Pull Action objects out of sentences in order and append to action_list.
    action_list = []
    for sentence in action_sentences:
        for i, word in enumerate(sentence):
            # ActionWords tag words that are not converted to XDL so shouldn't
            # be included here, only subclasses.
            # 'Once X is added' shouldn't be included as 'once' indicates that
            # it is restating an action that has already been described.
            if (type(word) == Action
                and not (i - 1 >= 0
                         and str(sentence[i - 1]).lower() == 'once')):

                if action_list:

                    # 'The rxn mixture was heated to 100C for 1 hr. After
                    # heating to 1hr at 100C,...'
                    # Should only be interpreted as one action.
                    if (str(word.words[0]).lower() == 'after'
                        and type(word.action) == type(action_list[-1].action)  # noqa: E721, E501
                        and type(word.action) in [
                            HeatWord, CoolWord, StirWord]):
                        continue

                    last_step_was_filtration = (
                        type(action_list[-1].action) in [
                            FilterWord, PurifyWord, IsolateWord, WashSolidWord])
                    solid_in_subject = (' solid' in str(word.subject)
                                        or ' filter cake' in str(word.subject)
                                        or ' needles' in str(word.subject)
                                        or ' precipitate' in str(word.subject))
                    liquid_in_subject = (' liquid' in str(word.subject)
                                         or ' mixture' in str(word.subject)
                                         or ' solution' in str(word.subject))
                    subject_not_reagent = type(word.subject) in [
                        VesselWord,
                        VesselComponentGroupWord,
                        ReagentPlaceholderWord
                    ]

                    # If WashWord or AddWord comes after FilterWord assumes it
                    # should be WashSolidWord.
                    if type(word.action) == WashWord:
                        if ((last_step_was_filtration or solid_in_subject)
                                and not liquid_in_subject):
                            word.action = WashSolidWord(word.action.words)

                    # i.e. 'washed with...', or 'rinsed with...' in this context
                    # means WashSolid
                    elif type(word.action) == AddWord:
                        add_action_is_wash = ('rins' in str(word.action)
                                              or 'washed' in str(word.action))
                        if (((last_step_was_filtration and subject_not_reagent)
                             or solid_in_subject)
                                and add_action_is_wash):
                            word.action = WashSolidWord(word.action.words)

                    # If Filter, WashSolid, Filter sequence encountered assume
                    # last Filter should be interpreted as a Dry.
                    elif (type(word.action) == FilterWord
                          and len(action_list) > 1):
                        if (type(action_list[-1].action) == WashSolidWord
                            and type(action_list[-2].action) in [
                                FilterWord, IsolateWord]):
                            word.action = DryWord(word.action.words)

                    # If HeatWord has no specific temp given look back in
                    # sentence for temperature that the word refers to
                    elif type(word.action) in [HeatWord, StirWord]:
                        if not any([type(modifier) == TemperatureModifier
                                    for modifier in word.action.modifiers]):
                            j = i
                            stop_search = False
                            while j > 0:
                                j -= 1
                                if type(sentence[j]) == Action:
                                    for modifier in sentence[j].modifiers:
                                        if (type(modifier)
                                                == TemperatureModifier):
                                            word.action.modifiers.append(
                                                modifier)
                                            stop_search = True
                                            break
                                if stop_search:
                                    break
                        # 'the mixture is stirred vigorously (Note 5) and 24 g
                        # of a 50% aqueous solution of sodium hydroxide (NaOH)
                        # (12.0 g, 0.30 mol in 12 mL of H2O) (Note 6) is added'
                        # Here stirring should happen during addition, not
                        # before So don't add StirWord to action list and add
                        # StirringModifier to next action.
                        if type(word.action) == StirWord:
                            if (not any([
                                type(modifier) in [
                                    TimeModifier, ReagentModifier]
                                for modifier in word.modifiers])
                                and not (isinstance(
                                    word.subject, AbstractReagentWord)
                                and not (type(word.subject)
                                         == ReagentPlaceholderWord))):
                                j = i + 1
                                while (j < len(sentence) and not isinstance(
                                        sentence[j], Action)):
                                    j += 1
                                if j < len(sentence):
                                    mod_words = copy.deepcopy(word.action.words)
                                    for mod in word.modifiers:
                                        mod_words.extend(mod.words)
                                    sentence[j].modifiers.append(
                                        StirringModifier(mod_words))
                                    sentence[j].modifiers.extend(word.modifiers)
                                    continue

                action_list.append(word)

            elif type(word) == VesselWord:
                for inert_word in ['nitrogen', 'purge', 'evacuat', 'inert']:
                    if inert_word in str(word):
                        action_list.append(
                            Action(subject=None,
                                   action=EvacuateWord(word.words),
                                   words=word.words,
                                   action_order_pos=0))
                        break

    action_list = postprocess_action_list(action_list)

    logger.debug('\nAction list\n-----------\n')
    for action in action_list:
        logger.debug(
            f'Action: {type(action.action).__name__}\
 {[str(word) for word in action.words]}')
        logger.debug(f'Subject: {str(action.subject)}')
        logger.debug('Modifiers:\n'
                     + '\n'.join([str(item) for item in action.modifiers]))
        logger.debug('\n')
    return action_list
