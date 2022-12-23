from typing import List
from ..words import (
    AbstractReagentWord,
    VesselComponentGroupWord,
    VesselWord,
    DiscontinueWord,
    AuxiliaryVerbWord,
    TechniqueWord,
    RequireWord,
    BathWord,
)
from ..words.modifiers import TimeModifier
from ..words.action_words import ActionWord, AffordWord

#: Words if encountered to skip when searching forward for Vessel/Action
# modifiers.
MODIFIER_SEARCH_CONTINUE_WORDS: List[str] = [
    ',',
    '(',
    ')',
    'by',
    'again',
    'usually',
    'successively',
    'along',
    'before',
    'ensuring',
    'that',
    'it',
    'sequentially',
    # 'then',
    'further',
]

#: Words that don't add any meaning but make patterns harder to match.
MEANINGLESS_WORDS: List[str] = [
    'then',
    'subsequent',
    'again',
    'first',
    'successively',
    ['which', 'precipitated'],
    ['in', 'turn'],
    'along',
    'additional',
    'sequentially',
    'further',
    'next',
    # 'before',
    # 'being',
]

# Sentence start fragments
extract_subjects = [
    AbstractReagentWord,
    'it',
    VesselWord,
    VesselComponentGroupWord,
    BathWord,
    ActionWord
]

extract_sentence_start_fragments = [
    [AuxiliaryVerbWord],
    ['now', 'needs', 'to', 'be'],
    # Hack to get the following working
    # '''The resulting mixture is then vacuum filtered while cold through a
    # sintered-glass funnel (Note 3) to collect the yellow needles (Note 4),
    # which are rinsed with pre-cooled (0 °C) anhydrous diethyl ether
    # (4 × 50 mL) (Notes 1, 5 and 6).'''
    # The rinse needs to have the yellow needles as the subject so it is
    # interpreted as WashSolid not as Add.
    [',', 'which', AuxiliaryVerbWord],
    # [],
]

extract_sentence_starts = []
for subject in extract_subjects:
    for start_fragment in extract_sentence_start_fragments:
        if 'which' in start_fragment and subject == ActionWord:
            continue
        extract_sentence_starts.append(
            ([subject] + start_fragment, {'subject': 0}))

# Sentence end fragments (stuff that comes after 'X was...')
extract_sentence_action_lists = [
    ([ActionWord], {'actions': [0]}),
    ([ActionWord, 'and', ActionWord], {'actions': [0, 2]}),
    ([ActionWord, 'and', ActionWord, 'and',
      ActionWord], {'actions': [0, 2, 4]}),
    ([ActionWord, ',', 'and', ActionWord, 'and',
      ActionWord], {'actions': [0, 3, 5]}),
    ([ActionWord, ',', 'and', ActionWord], {'actions': [0, 3]}),
    ([ActionWord, ',', ActionWord, 'and', ActionWord], {'actions': [0, 2, 4]}),
    ([ActionWord, ',', ActionWord, ',', 'and', ActionWord],
     {'actions': [0, 2, 5]}),

    # Very long patterns just in case people go mental while writing sentence
    ([ActionWord, ',', ActionWord, ',', ActionWord, 'and', ActionWord],
     {'actions': [0, 2, 4, 6]}),
    ([ActionWord, 'and', ActionWord, ',', ActionWord, 'and', ActionWord],
     {'actions': [0, 2, 4, 6]}),
    ([ActionWord, 'and', ActionWord, ',', ActionWord, ',', ActionWord, ',',
      'and', ActionWord],
     {'actions': [0, 2, 4, 6, 9]}),
    ([ActionWord, ',', ActionWord, ',', ActionWord, ',', ActionWord, 'and',
      ActionWord],
     {'actions': [0, 2, 4, 6, 8]}),
    ([ActionWord, ',', ActionWord, ',', ActionWord, ',', ActionWord, ',',
      ActionWord, 'and', ActionWord],
     {'actions': [0, 2, 4, 6, 8, 10]}),
    ([ActionWord, ',', ActionWord, ',', ActionWord, ',', ActionWord, ',',
      ActionWord, ',', ActionWord, 'and', ActionWord],
     {'actions': [0, 2, 4, 6, 8, 10, 12]}),
    ([ActionWord, ',', ActionWord, ',', ActionWord, ',', ActionWord, ',',
      ActionWord, ',', ActionWord, ',', ActionWord, 'and', ActionWord],
     {'actions': [0, 2, 4, 6, 8, 10, 12, 14]}),

    # Below is to handle sentences like 'X is Yed and Zed, then Wed. The word
    # 'then' is removed before these patterns are applied so is not included in
    # these patterns.
    ([ActionWord, ',', ActionWord], {'actions': [0, 2]}),
    ([ActionWord, ',', ActionWord, ',', ActionWord], {'actions': [0, 2, 4]}),
    ([ActionWord, 'and', ActionWord, ',', ActionWord], {'actions': [0, 2, 4]}),
    ([ActionWord, ',', ActionWord, 'and', ActionWord, ',', ActionWord],
     {'actions': [0, 2, 4, 6]}),
    ([ActionWord, ',', ActionWord, ',', ActionWord, ',', ActionWord],
     {'actions': [0, 2, 4, 6]}),
    ([ActionWord, ',', ActionWord, ',', ActionWord, ',', 'and', ActionWord],
     {'actions': [0, 2, 4, 7]}),

    # Stuff like 'The solution was filtered through celite and the solvent
    # evaporated...'
    ([ActionWord, 'and', AbstractReagentWord, ActionWord],
     {'actions': [0, 3], 'subject': [None, 2]}),
    ([ActionWord, ',', ActionWord, 'and', AbstractReagentWord, ActionWord],
     {'actions': [0, 2, 5], 'subject': [None, None, 4]}),
    ([ActionWord, ',', AbstractReagentWord, ActionWord, 'and',
      AbstractReagentWord, ActionWord],
     {'actions': [0, 3, 6], 'subject': [None, 2, 5]}),
    ([ActionWord, 'and', AbstractReagentWord, ActionWord, 'and', ActionWord],
     {'actions': [0, 3, 5], 'subject': [None, 2, None]}),
    ([ActionWord, ',', 'and', AbstractReagentWord, ActionWord],
     {'actions': [0, 4], 'subject': [None, 3]}),

    # Cinnamaldehyde is added and the reaction stirred for 15 minutes,
    # then cooled to -78.
    ([ActionWord, 'and', AbstractReagentWord, ActionWord, ',', ActionWord],
     {'actions': [0, 3, 5], 'subject': [None, 2, None]}),

    # The reaction mixture was then transferred to a separatory funnel along
    # with 100 mL of EtOAc, and washed with saturated NaHCO 3 solution, dried
    # over anhydrous MgSO4, filtered and concentrated to give a yellow liquid.
    ([ActionWord, ',', 'and', ActionWord, ',', ActionWord, ',', ActionWord,
      'and', ActionWord],
     {'actions': [0, 3, 5, 7, 9]}),

    ([ActionWord, 'while', 'being', ActionWord], {'actions': [0, 3]}),
]

extra_patterns = []
for pattern, action_indexes in extract_sentence_action_lists:
    new_pattern = [ActionWord, 'by'] + pattern
    new_action_indexes = [i
                          for i in range(len(new_pattern))
                          if i > 0 and new_pattern[i] == ActionWord]
    extra_patterns.append((new_pattern, {'actions': new_action_indexes}))

    new_pattern = [ActionWord, 'followed', 'by'] + pattern
    new_action_indexes = [i
                          for i in range(len(new_pattern))
                          if new_pattern[i] == ActionWord]
    extra_patterns.append((new_pattern, {'actions': new_action_indexes}))

    new_pattern = [ActionWord, ',', 'followed', 'by'] + pattern
    new_action_indexes = [i
                          for i in range(len(new_pattern))
                          if new_pattern[i] == ActionWord]
    extra_patterns.append((new_pattern, {'actions': new_action_indexes}))
extract_sentence_action_lists.extend(extra_patterns)

# Sentence pre fragments (stuff that can be before proper sentence start)
extract_sentence_pre_starts = [
    ([], {'actions': []}),
    (['after', ActionWord, ','], {'actions': [1]}),
    (['after', ActionWord, 'and', ActionWord, ','], {'actions': [1, 3]}),
    (['after', ActionWord], {'actions': [1]}),
    (['after', TimeModifier], {'actions': [1]}),
    (['after', TimeModifier, ','], {'actions': [1]}),
]

EXTRACT_ACTION_PATTERNS = []
for pre in extract_sentence_pre_starts:
    for start in extract_sentence_starts:
        for action_list in extract_sentence_action_lists:
            pattern = []
            action_indexes = []
            subject_indexes = []
            subject = 0
            # Add sentence pre start
            if pre[0]:
                pattern.extend(pre[0])
                action_indexes.extend(pre[1]['actions'])
                if 'subject' not in pre[1]:
                    subject_indexes.extend(
                        [None for _ in range(len(pre[1]['actions']))])
                else:
                    subject_indexes.extend(pre[1]['subject'])

            # Add sentence start
            offset = len(pattern)
            pattern.extend(start[0])
            subject = start[1]['subject'] + offset

            # Add sentence end
            offset = len(pattern)
            pattern.extend(action_list[0])
            action_indexes.extend(
                [i + offset for i in action_list[1]['actions']])
            if 'subject' not in action_list[1]:
                subject_indexes.extend(
                    [None for _ in range(len(action_list[1]['actions']))])
            else:
                for item in action_list[1]['subject']:
                    if item is None:
                        subject_indexes.append(item)
                    else:
                        subject_indexes.append(item + offset)

            # Fill in default subject if not explicitly given
            for i in range(len(subject_indexes)):
                if subject_indexes[i] is None:
                    subject_indexes[i] = subject
            EXTRACT_ACTION_PATTERNS.append((
                pattern,
                subject_indexes,
                action_indexes))

YIELDED_WORDS = ['gives', 'gave', 'yielded', ]

# 'Addition of THF (750 mL) followed by stirring overnight gives a YELLOW
# (mustard) solid and a red solution.'
for item in YIELDED_WORDS:
    EXTRACT_ACTION_PATTERNS.append(
        ([ActionWord, 'followed', 'by', ActionWord, item, ],
         4,  # This is the word  'gives'. Bit of a hack to avoid matching actual
         # subject as this can be annoying e.g. 'a YELLOW (mustard) solid'
         [0, 3]))

# There is then added through the separatory funnel, with stirring, 315 g.
# (235 cc., 2.5 moles) of dimethyl sulfate (Note 2).
EXTRACT_ACTION_PATTERNS.append(
    (['there', AuxiliaryVerbWord, ActionWord, AbstractReagentWord],
     -1,
     [-2]))
EXTRACT_ACTION_PATTERNS.append(
    (['there', AuxiliaryVerbWord, ActionWord, ',', AbstractReagentWord],
     -1,
     [-3]))

# The addition requires...
EXTRACT_ACTION_PATTERNS.append(
    (['the', ActionWord, RequireWord], 1, [2]))
EXTRACT_ACTION_PATTERNS.append(
    (['this', ActionWord, RequireWord], 1, [2]))
EXTRACT_ACTION_PATTERNS.append(
    (['this', 'operation', RequireWord], 1, [2]))

# 'flask column chromatography provided...'
EXTRACT_ACTION_PATTERNS.append(
    ([TechniqueWord, ActionWord],
     0,
     [1])
)

EXTRACT_ACTION_PATTERNS.append((
    [ActionWord, AbstractReagentWord],
    1,
    [0]))

EXTRACT_ACTION_PATTERNS.append((
    [ActionWord, AffordWord, AbstractReagentWord],
    2,
    [0]))

EXTRACT_ACTION_PATTERNS.append(
    # is Xed... This was added to deal with the sentence:
    # 'The product separates as a granular white solid and is isolated by
    #  vacuum filtration.'
    # Not really happy with this as a solution, seems hacky.
    ([AuxiliaryVerbWord, ActionWord],
     0,
     [1])
)

EXTRACT_ACTION_PATTERNS.extend([
    (['after', ActionWord], 0, [1]),
    (['after', ActionWord, 'and', ActionWord], 0, [1, 3])
])

EXTRACT_ACTION_PATTERNS.append(
    # before being Xed... This was added to deal with the sentence:
    # '''The product separates as a granular white solid and is isolated by
    #  vacuum filtration.'
    # Not really happy with this as a solution, seems hacky.'''
    # Ideally would have a longer pattern that matches the whole sentence,
    # but this should be here as a backup so the action is not completely lost.
    (['before', 'being', ActionWord],
     0,
     [2])
)

EXTRACT_ACTION_PATTERNS.append(
    (['to', AbstractReagentWord, AuxiliaryVerbWord, ActionWord,
      AbstractReagentWord],
     4,
     [3])
)

EXTRACT_ACTION_PATTERNS.append(([DiscontinueWord], 0, [0]))

EXTRACT_ACTION_PATTERNS.append(([TechniqueWord, ActionWord], 0, [1]))

# Sort patterns longest to shortest so that sub patterns don't match first.
EXTRACT_ACTION_PATTERNS = sorted(
    EXTRACT_ACTION_PATTERNS, key=lambda x: 1 / len(x[0]))

for i, item in enumerate(EXTRACT_ACTION_PATTERNS):
    pattern, subject_index, action_indexes = item
    if type(subject_index) == int:
        EXTRACT_ACTION_PATTERNS[i] = (
            pattern,
            [subject_index for _ in range(len(action_indexes))],
            action_indexes
        )
