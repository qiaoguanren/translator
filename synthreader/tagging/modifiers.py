from typing import List, Tuple, Union, Type
from ..words.modifiers import (
    TechniqueModifier,
    MethodModifier,
    AtmosphereModifier,
    RepeatModifier,
    TimeModifier,
    ReagentModifier,
    DetailsModifier,
    PressureModifier,
    VesselModifier,
    TemperatureModifier,
    StirringModifier,
    AdditionModifier,
    Modifier
)
from ..words import (
    Word,
    ActionWord,
    TimeWord,
    TempWord,
    PressureWord,
    TechniqueWord,
    HeatWord,
    # ActionWord,
    VesselWord,
    VesselComponentGroupWord,
    MultiplierWord,
    NumberWord,
    QuantityGroupWord,
    ReagentPlaceholderWord,
    AbstractReagentWord,
    WaitWord,
    AuxiliaryVerbWord,
    pHWord,
    DetailsWord,
    BathWord,
    StirSpeedWord,
    MassWord,
)
# InertAtmosphereWord)
from ..utils import (
    apply_pattern,
    trim_patterns,
    Pos,
    Optional
)

MODIFIER_PATTERNS: List[
    Tuple[List[Union[str, int, Type[Word]]], Type[Modifier]]] = [
    # Stirring modifiers
    (['while', 'stirring'], StirringModifier),
    (['with', 'stirring'], StirringModifier),
    (['with', Optional(Pos('JJ')), 'shaking'], StirringModifier),
    (['with', 'continual', 'stirring'], StirringModifier),
    (['with', Optional(Pos('JJ')), 'stirring'], StirringModifier),
    (['with', Optional(Pos('JJ')), Optional(Pos('JJ')), 'stirring'],
     StirringModifier),
    (['with', 'slow', 'stirring'], StirringModifier),
    (['with', 'hand', ' stirring'], StirringModifier),
    (['with', 'vigorous', 'stirring'], StirringModifier),
    (['with', 'rapid', 'stirring'], StirringModifier),
    (['with', 'intermittent', 'shaking'], StirringModifier),
    (['with', 'mechanical', 'stirring'], StirringModifier),
    (['at', 'a', 'moderate', 'speed'], StirringModifier),
    (['with', 'stirring', 'at', 'a', 'rate', 'of', StirSpeedWord],
     StirringModifier),
    (['with', Optional(Pos('JJ')), 'agitation'], StirringModifier),
    (['with', 'swirling'], StirringModifier),

    # Addition modifiers
    (['in', 'portions'], AdditionModifier),
    (['in', NumberWord, 'portions'], AdditionModifier),
    (['(', MassWord, 'every', TimeWord, ')'], AdditionModifier),
    (['dropwise'], AdditionModifier),
    (['portionwise'], AdditionModifier),

    # Temperature modifiers
    (['at', TempWord], TemperatureModifier),
    (['to', 'below', TempWord], TemperatureModifier),
    (['to', TempWord, 'or', 'below'], TemperatureModifier),
    (['at', 'room', 'temperature'], TemperatureModifier),
    (['down', 'to', 'room', 'temperature'], TemperatureModifier),
    (['up', 'to', 'room', 'temperature'], TemperatureModifier),
    (['down', 'to', 'rt'], TemperatureModifier),
    (['up', 'to', 'rt'], TemperatureModifier),
    (['to', 'room', 'temperature'], TemperatureModifier),
    (['at', 'rt'], TemperatureModifier),
    (['to', 'rt'], TemperatureModifier),
    (['with', 'ice'], TemperatureModifier),
    (['with', 'ice', 'water'], TemperatureModifier),
    (['with', 'an', 'ice-salt', 'mixture'], TemperatureModifier),
    (['at', 'ambient', 'temperature'], TemperatureModifier),
    (['to', 'ambient', 'temperature'], TemperatureModifier),
    (['to', TempWord], TemperatureModifier),
    (['until', VesselComponentGroupWord, 'reaches', TempWord],
     TemperatureModifier),
    (['so', 'that', 'the', 'temperature', 'rises', 'from', TempWord, 'to',
      TempWord],
     TemperatureModifier),
    (['the', 'temperature', 'of', BathWord, AuxiliaryVerbWord,
      WaitWord, 'at', TempWord], TemperatureModifier),
    (['in', 'a', TempWord, 'freezer'], TemperatureModifier),
    (['that', AuxiliaryVerbWord, 'preheated', 'to', TempWord],
     TemperatureModifier),
    (['preheated', 'to', TempWord], TemperatureModifier),

    # (['while', 'maintaining', 'the', 'temperature', 'below', TempWord],
    #  TemperatureModifier),
    # (['while', 'maintaining', 'the', 'temperature', 'above', TempWord],
    #  TemperatureModifier),
    (['at', 'ambient temperature', ], TemperatureModifier),
    (['at', 'this', 'temperature', ], TemperatureModifier),
    (['internal', 'temperature'], TemperatureModifier),
    (['at', 'reflux'], TemperatureModifier),
    (['to', 'reflux'], TemperatureModifier),
    (['under', 'reflux'], TemperatureModifier),
    (['over', 'a', Optional(Pos('JJ')), 'flame'], TemperatureModifier),
    (['with', 'a', Optional(Pos('JJ')), 'flame']),
    (['by', 'means', 'of', BathWord], TemperatureModifier),
    (['on', BathWord], TemperatureModifier),
    (['in', BathWord], TemperatureModifier),
    (['in', BathWord, HeatWord, 'to', TempWord], TemperatureModifier),
    (['in', 'a', 'room-temperature', Optional('('), Optional(TempWord),
      Optional(')'), BathWord], TemperatureModifier),
    (['using', BathWord], TemperatureModifier),
    (['at', 'bath', 'temperature'], TemperatureModifier),
    (['in', 'a', TempWord, BathWord], TemperatureModifier),
    ([Optional('while'), 'maintaining', Optional('the'), 'internal',
      'temperature', 'below', TempWord], TemperatureModifier),

    # Time modifiers
    (['about', TimeWord], TimeModifier),
    (['for', TimeWord], TimeModifier),
    (['for', Optional('an'), 'additional', TimeWord], TimeModifier),
    (['for', 'a', 'further', TimeWord], TimeModifier),
    (['for', 'approximately', TimeWord], TimeModifier),
    (['for', 'about', TimeWord], TimeModifier),
    (['for', 'another', TimeWord], TimeModifier),
    # (['as', 'long', 'as', 'possible'], TimeModifier),
    (['over', Pos('DT'), 'period', 'of', TimeWord], TimeModifier),
    (['over', 'approximately', TimeWord], TimeModifier),
    (['over', 'about', TimeWord], TimeModifier),
    (['over', 'a', 'period', 'of', 'approximately', TimeWord], TimeModifier),
    (['immediately'], TimeModifier),
    (['as', 'long', 'as', 'possible'], TimeModifier),
    (['over', TimeWord], TimeModifier),
    (['over', 'the', 'course', 'of', TimeWord], TimeModifier),
    (['in', TimeWord], TimeModifier),
    (['overnight'], TimeModifier),
    (['briefly'], TimeModifier),
    (['(', 'overnight', ')'], TimeModifier),
    (['until', 'the', 'reaction', 'completed'], TimeModifier),
    (['until', 'the', 'reaction', AuxiliaryVerbWord, 'complete'], TimeModifier),
    (['in', 'the', 'course', 'of', 'about', TimeWord], TimeModifier),
    (['over', 'a', TimeWord, 'period'], TimeModifier),
    (['for', 'at', 'least', TimeWord], TimeModifier),

    # Pressure modifiers
    (['under', 'atmospheric', 'pressure'], PressureModifier),
    (['under', 'reduced', 'pressure'], PressureModifier),
    (['under', 'diminished', 'pressure'], PressureModifier),
    (['at', PressureWord], PressureModifier),
    (['to', PressureWord], PressureModifier),

    # Reagent Modifiers
    (['with', 'some', 'of', AbstractReagentWord], ReagentModifier),
    (['with', 'the', 'assistance', 'of', AbstractReagentWord], ReagentModifier),
    (['with', 'the', 'aid', 'of', AbstractReagentWord], ReagentModifier),
    (['of', AbstractReagentWord], ReagentModifier),
    (['using', AbstractReagentWord], ReagentModifier),
    (['by', 'injecting', AbstractReagentWord], ReagentModifier),
    (['in', AbstractReagentWord], ReagentModifier),
    ([Optional('along'), 'with', Optional(Pos('JJ')),
      AbstractReagentWord], ReagentModifier),
    (['with', Optional('a'), AbstractReagentWord], ReagentModifier),
    (['with', 'sufficient', AbstractReagentWord], ReagentModifier),
    (['with', 'small', 'quantities', 'of', AbstractReagentWord],
     ReagentModifier),
    (['with', 'an', 'excess', 'of', AbstractReagentWord], ReagentModifier),
    (['in', 'the', 'presence', 'of', AbstractReagentWord], ReagentModifier),
    (['with', 'additional', AbstractReagentWord], ReagentModifier),
    (['with', 'a', 'little', AbstractReagentWord], ReagentModifier),
    (['with', 'an', 'additional', AbstractReagentWord], ReagentModifier),
    # 'washed with 3 80 mL portions of ether...'
    (['with', NumberWord, AbstractReagentWord], ReagentModifier),
    (['with', NumberWord, AbstractReagentWord, 'and',
      NumberWord, AbstractReagentWord], ReagentModifier),
    (['on', AbstractReagentWord], ReagentModifier),
    (['onto', AbstractReagentWord], ReagentModifier),
    (['containing', AbstractReagentWord], ReagentModifier),
    (['to', 'the', AbstractReagentWord], ReagentModifier),
    (['to', Optional('an'), AbstractReagentWord], ReagentModifier),
    (['into', AbstractReagentWord], ReagentModifier),
    (['followed', 'by', AbstractReagentWord], ReagentModifier),
    (['with', 'an', 'additional', AbstractReagentWord], ReagentModifier),
    (['with', 'equal', 'volumes', 'of', AbstractReagentWord], ReagentModifier),
    (['by', 'addition', 'of', AbstractReagentWord], ReagentModifier),
    (['over', AbstractReagentWord], ReagentModifier),
    (['while', 'washing', 'with', AbstractReagentWord], ReagentModifier),
    (['eluting', 'with', AbstractReagentWord], ReagentModifier),
    (['with', 'the', 'remaining', AbstractReagentWord], ReagentModifier),

    # Method modifiers
    (['to', 'cool'], MethodModifier),
    (['from', ReagentPlaceholderWord], ReagentModifier),
    (['vigorously'], MethodModifier),  # 'by stirring vigorously...'
    (['slowly'], MethodModifier),
    (['very', 'slowly'], MethodModifier),
    (['carefully'], MethodModifier),
    (['careful'], MethodModifier),
    (['thoroughly'], MethodModifier),
    (['all', 'at', 'once'], MethodModifier),
    # Hack as 'once' becomes MultiplierWord during quantity tagging.
    (['all', 'at', MultiplierWord], MethodModifier),
    (['as', 'dry', 'as', 'possible'], MethodModifier),
    (['to', VesselWord], MethodModifier),
    (['in', VesselWord], MethodModifier),
    (['through', VesselWord], MethodModifier),
    (['into', VesselWord], MethodModifier),
    (['on', VesselWord], MethodModifier),
    (['onto', VesselComponentGroupWord], MethodModifier),
    # via an addition funnel.
    (['via', VesselComponentGroupWord], MethodModifier),
    (['from', BathWord], MethodModifier),
    (['with', 'the', 'aid', 'of', VesselWord], MethodModifier),
    (['with', 'the', 'aid', 'of', VesselComponentGroupWord], MethodModifier),
    (['on', VesselComponentGroupWord], MethodModifier),
    (['to', VesselComponentGroupWord], MethodModifier),
    (['to', VesselWord], MethodModifier),
    (['with', VesselWord], MethodModifier),
    (['on', 'top', 'of', VesselComponentGroupWord], MethodModifier),
    (['via', 'cannula'], MethodModifier),
    (['through', VesselComponentGroupWord], MethodModifier),
    (['in', VesselComponentGroupWord], MethodModifier),
    (['using', VesselComponentGroupWord], MethodModifier),
    (['using', BathWord], MethodModifier),
    (['with', BathWord], MethodModifier),
    (['preheated', 'with', VesselComponentGroupWord], MethodModifier),
    (['by', VesselComponentGroupWord], MethodModifier),
    (['into', VesselComponentGroupWord], MethodModifier),
    (['by', 'means', 'of', VesselComponentGroupWord], MethodModifier),
    (['by', 'means', 'of', VesselComponentGroupWord], MethodModifier),
    (['until', 'all', ReagentPlaceholderWord, 'dissolve'], MethodModifier),
    (['with', 'slow', 'warming'], MethodModifier),
    (['well'], MethodModifier),
    (['to', pHWord], MethodModifier),
    (['together'], MethodModifier),
    (['until', 'completion'], MethodModifier),
    (['rapidly'], MethodModifier),
    (['until', 'crystallisation', 'begins', 'to', 'occur'], MethodModifier),
    (['until', 'crystallization', 'begins', 'to', 'occur'], MethodModifier),
    (['by', 'immersion', 'in', 'ice', 'water'], MethodModifier),
    (['in', 'a', 'vacuum', 'oven'], MethodModifier),
    (['gently'], MethodModifier),
    (['under', 'a', 'gentle', 'stream', 'of', 'nitrogen'], MethodModifier),
    (['under', 'a', 'higher', 'vacuum'], MethodModifier),
    (['with', Optional(Pos('JJ')), 'suction'], MethodModifier),
    (['with', Optional(Pos('JJ')), 'nitrogen'], MethodModifier),
    (['with', 'hydrogen'], MethodModifier),
    (['with', Optional(Pos('JJ')), 'argon'], MethodModifier),
    (['in', 'batches'], MethodModifier),
    (['into', Pos('DT'), ActionWord, 'reaction'], MethodModifier),
    (['to', 'dissolve', AbstractReagentWord], MethodModifier),
    (['in', 'order', 'to', 'dissolve', AbstractReagentWord], MethodModifier),
    (['until', 'complete', 'dissolution', 'had', 'occurred'], MethodModifier),
    (['until', 'complete', 'dissolution', 'occurs'], MethodModifier),
    (['using', 'a', 'vacuum', 'line'], MethodModifier),
    (['to', 'wash', AbstractReagentWord], MethodModifier),
    (['to', 'dryness'], MethodModifier),
    (['to', 'rinse', VesselWord], MethodModifier),

    # Technique modifiers
    (['using', TechniqueWord], TechniqueModifier),
    (['(', TechniqueWord, ')'], TechniqueModifier),
    (['by', TechniqueWord], TechniqueModifier),
    (['via', TechniqueWord], TechniqueModifier),
    (['to', TechniqueWord], TechniqueModifier),
    (['using', TechniqueWord], TechniqueModifier),
    (['by', Optional(Pos('JJ')), TechniqueWord], TechniqueModifier),
    (['on', 'a', 'glass', 'filter'], TechniqueModifier),
    (['through', 'Whatman', NumberWord, 'filter', 'paper'], TechniqueModifier),
    (['through', 'celite'], TechniqueModifier),
    (['through', 'celite', QuantityGroupWord], TechniqueModifier),
    (['through', VesselComponentGroupWord, 'of', 'celite'], TechniqueModifier),
    (['through', 'a', 'bed', 'of', 'celite'], TechniqueModifier),
    (['through', 'a', 'celite', VesselComponentGroupWord], TechniqueModifier),
    (['through', 'a', 'celite', QuantityGroupWord,
      VesselComponentGroupWord], TechniqueModifier),
    (['through', 'a', 'silica', 'gel', VesselComponentGroupWord],
     TechniqueModifier),
    (['through', 'a', 'filter', 'paper'], TechniqueModifier),
    (['by', 'standing', 'over', AbstractReagentWord], TechniqueModifier),
    (['over', 'celite'], TechniqueModifier),
    (['through', 'a', 'very', 'small', 'amount',
      'of', 'dry', 'celite'], TechniqueModifier),
    (['in', 'vacuo'], TechniqueModifier),
    (['in', 'vacuum'], TechniqueModifier),
    (['under', 'vacuum'], TechniqueModifier),
    (['under', 'high', 'vacuum'], TechniqueModifier),
    (['by', 'recrystallization'], TechniqueModifier),
    (['in', 'a', 'freezer'], TechniqueModifier),

    # Repeat modifiers
    ([MultiplierWord], RepeatModifier),

    # Atmosphere modifiers
    (['under', 'argon'], AtmosphereModifier),
    (['under', 'nitrogen'], AtmosphereModifier),
    (['under', 'an', 'atmosphere', 'of', 'nitrogen'], AtmosphereModifier),
    (['under', 'an', 'atmosphere', 'of', 'argon'], AtmosphereModifier),
    (['in', 'air'], AtmosphereModifier),
    (['using', 'schlenk', 'techniques'], AtmosphereModifier),

    # Random details
    ([DetailsWord], DetailsModifier),

    # Here so observations not interpreted as actions, e.g.
    # 'the yellow heterogeneous reaction turns colorless two seconds after the
    # addition of...'
    ([TimeModifier, 'after', ActionWord], DetailsModifier),

    # Modifiers that won't be used later on.
    (['on', 'top', 'of', AbstractReagentWord],
     Modifier),  # on top of the silica gel
    (['to', 'give', ReagentPlaceholderWord], Modifier),
]

# Need to be sorted not including optionals otherwise 'eluting with Reagent'
# comes after 'with OPTIONAL_ADJETICE Reagent'
MODIFIER_PATTERNS = sorted(MODIFIER_PATTERNS, key=lambda x: 1 / len(
    [item for item in x[0] if type(item) not in [int, Optional]]))

VESSEL_MODIFIER_PATTERNS: List[
    Tuple[List[Union[str, int, Type[Word]]], Type[Modifier]]] = [
    (['with', VesselComponentGroupWord], VesselModifier),
    # equipped with VC, VC, and VC
    (['equipped', 'with', VesselComponentGroupWord, ',',
      VesselComponentGroupWord, ',', 'and', VesselComponentGroupWord],
     VesselModifier),
    # equipped with VC, VC and VC
    (['equipped', 'with', VesselComponentGroupWord, ',',
      VesselComponentGroupWord, 'and', VesselComponentGroupWord],
     VesselModifier),
    # equipped with VC, and VC
    (['equipped', 'with', VesselComponentGroupWord, ',', 'and',
      VesselComponentGroupWord],
     VesselModifier),
    # equipped with VC and VC
    (['equipped', 'with', VesselComponentGroupWord, 'and',
      VesselComponentGroupWord],
     VesselModifier),
    # equipped with VC
    (['equipped', 'with', VesselComponentGroupWord], VesselModifier),
    (['equipped', 'for', 'magnetic', 'stirring'], VesselModifier),
    (['fitted', 'with', VesselComponentGroupWord], VesselModifier),
]
MODIFIER_PATTERNS.extend(VESSEL_MODIFIER_PATTERNS)

def pattern_modifier_tag(
        sentences: List[List[Word]], word_bank) -> List[List[Word]]:
    """Look for phrases that modify actions in sentences and combine them into
    Modifiers.

    Args:
        sentences (List[List[Word]]): Sentences to look for phrases that modify
            actions in.

    Returns:
        List[List[Word]]: Sentences with phrases that modify actions combined
            into Modifier objects.
    """
    for pattern in trim_patterns(MODIFIER_PATTERNS, word_bank):
        if len(pattern) == 2:
            sentences = apply_pattern(pattern[0], pattern[1], sentences)
        elif len(pattern) == 3:
            sentences = apply_pattern(
                pattern[0], pattern[1], sentences, replace_pos=pattern[2])
    return sentences

def non_pattern_modifier_tag(sentences: List[List[Word]]) -> List[List[Word]]:
    """Look for phrases that modify actions in sentences and combine them into
    Modifiers. This is for specific situations where Word objects need to be
    inspected, simple pattern matching isn't enough.

    Args:
        sentences (List[List[Word]]): Sentences to look for phrases that modify
            actions in.

    Returns:
        List[List[Word]]: Sentences with phrases that modify actions combined
            into Modifier objects.
    """
    for i, sentence in enumerate(sentences):
        # Last word in sentence can't be subject so should be modifier.
        if (len(sentence) >= 3
            and isinstance(sentence[-2], AbstractReagentWord)
                and not isinstance(sentence[-3], ActionWord)):
            sentence[-2] = ReagentModifier(sentence[-2:-1])
        for j, word in enumerate(sentence):
            # Match modifiers hidden in quantity groups
            if type(word) == QuantityGroupWord:
                if len(word.quantities) == 1:
                    quantity = word.quantities[0]
                    if type(quantity) == TimeWord:
                        sentences[i][j] = TimeModifier([word])
                        break

                    elif type(quantity) == TempWord:
                        sentences[i][j] = TemperatureModifier([word])
                        break

                    elif type(quantity) == StirSpeedWord:
                        sentences[i][j] = StirringModifier([word])
                        break

                    elif type(quantity) == PressureWord:
                        sentences[i][j] = PressureModifier([word])
                        break
                    else:
                        sentences[i][j] = DetailsModifier([DetailsWord([word])])
                else:
                    sentences[i][j] = DetailsModifier([DetailsWord([word])])

            # Match 'The reaction was quenched by adding X', bWut only for
            # present tense verbs.
            elif isinstance(word, ActionWord) and str(word).endswith('ing'):
                if (j + 1 < len(sentence)
                        and isinstance(sentence[j + 1], AbstractReagentWord)):
                    sentence[j + 1] = ReagentModifier(sentence[j + 1: j + 2])

            # 'The solution was left stirring', stirring should be treated as
            # TechniqueModifier
            elif (type(word) == WaitWord
                  and j + 1 < len(sentence)
                  and str(sentence[j + 1]).endswith('ing')):
                sentence[j + 1] = TechniqueModifier(sentence[j + 1].words)
    return sentences

def mystery_modifier_tag(sentences):
    """UNUSED. Method to tag generic modifier phrases according to POS rules,
    regardless of specific words used. Caused more problems than it solved.
    """
    for sentence in sentences:
        i = 2
        while i < len(sentence):
            if type(sentence[i]) == Word:
                if sentence[i].pos == 'IN':
                    j = i
                    while True:
                        j += 1
                        if j >= len(sentence):
                            break
                        if type(sentence[j]) == Word:
                            if sentence[j].pos in ['IN', ',']:
                                break
                            else:
                                continue
                        if not isinstance(
                            sentence[j],
                            (Modifier, ActionWord, AbstractReagentWord)
                        ):
                            continue
                        else:
                            break
                    # found_noun = False
                    # while (j < len(sentence)
                    #        and type(sentence[j]) == Word
                    #        and sentence[j].pos == 'JJ'):
                    #     j += 1
                    # while (j < len(sentence)
                    #        and type(sentence[j]) == Word
                    #        and sentence[j].pos == 'DT'):
                    #     j += 1
                    # while (j < len(sentence)
                    #        and type(sentence[j]) == Word
                    #        and sentence[j].pos in ['NN', 'VBG']):
                    #     found_noun = True
                    #     j += 1
                    # if found_noun:
                    if (j > i + 1 and not (j + 1 < len(sentence) and isinstance(sentence[j + 1], ActionWord))):  # noqa: E501
                        mod = Modifier(sentence[i:j])
                        del sentence[i: j]
                        sentence.insert(i, mod)
            i += 1
    return sentences
