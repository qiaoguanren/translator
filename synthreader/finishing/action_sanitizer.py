from typing import List, Dict, Callable, Union, Tuple
from .constants import (
    SLOW_ADDITION_WORDS,
    DROPWISE_ADDITION_WORDS,
    SLOW_STIRRING_WORDS,
    FAST_STIRRING_WORDS,
    DEFAULT_THOROUGH_STIR_TIME,
    DEFAULT_AS_DRY_AS_POSSIBLE_DRYING_TIME,
    DEFAULT_ALLOWED_TO_COOL_TIME,
    DEFAULT_COLD_REAGENT_TEMP,
    DEFAULT_ICECOLD_REAGENT_TEMP,
    DEFAULT_HOT_REAGENT_TEMP,
    DEFAULT_WARM_REAGENT_TEMP,
    REAGENT_NAME_COLD_WORDS,
    REAGENT_NAME_ICECOLD_WORDS,
    DEFAULT_STIRRING_TIME,
    DEFAULT_BRIEF_TIME,
    DEFAULT_MINIMUM_VOLUME,
    EVAPORATE_REMOVE_PHRASES,
)
from .utils import get_reagent_temp
from ..words import *
from ..words.modifiers import *

#############################
### SEPARATION SANITIZERS ###
#############################

def sanitize_actions(action_list: List[Action]) -> List[Action]:
    """Sanitize all actions in action list so they are ready for their
    respective action -> XDL converter.

    Args:
        action_list (List[Action]): List of actions extracted from labelled text
            by ..interpreting.extract_actions.

    Returns:
        List[Action]: Sanitized list of Actions ready for
            action -> XDL converters.
    """
    for i, action in enumerate(action_list):
        if type(action) == SolutionWord:
            action_list[i] = sanitize_solution_word(action)
        else:
            action_list[i] = SANITIZE_FN_DICT[type(action.action)](action)
    action_list = [action for action in action_list if action]
    postprocess_action_list(action_list)
    return action_list

def get_separation_groups(action_list: List[Action]) -> List[List[Word]]:
    """Get groups of consecutive Separate steps from XDL object."""
    separation_groups = []
    separation_group = []
    non_separations = 0
    for action in action_list:
        if type(action.action) == WashWord:
            if not action.addition_funnel and not action.flask_wash:
                non_separations = 0
                separation_group.append(action)

        elif type(action.action) == ExtractWord:
            non_separations = 0
            separation_group.append(action)

        else:
            non_separations += 1
            if non_separations > 1 and separation_group:
                separation_groups.append(separation_group)
                separation_group = []
    if separation_group:
        separation_groups.append(separation_group)
    return separation_groups

def get_simplified_separation_sequence(sep_group):
    """For ever separation in group of separations find purpose, layer to be
    washed/extracted ('aq' or 'org') and solvent_type ('aq' or 'org'). Return as
    list of tuples [(purpose, target_layer, solvent_type)...]
    """
    seq = []
    for sep in sep_group:
        if not sep.separations:
            if 'organic' in str(sep.subject):
                target_layer = 'aq'
                solvent_type = 'org'
            else:
                target_layer = 'org'
                solvent_type = 'aq'
            seq.append(('extract', target_layer, solvent_type))
        for separation in sep.separations:
            # Get purpose
            purpose = 'extract'
            if type(sep.action) == WashWord:
                purpose = 'wash'
            # Get target layer
            target_layer = None
            if 'aqueous' in str(sep.subject):
                target_layer = 'aq'
            elif 'organic' in str(sep.subject):
                target_layer = 'org'

            # Get solvent type
            solvent_type = 'org'
            for item in [
                ' m ',
                'acid',
                'hydroxide',
                'nacl',
                'naoh',
                'water',
                'brine',
                'solution',
                'aqueous',
                'hcl',
                'h2o',
            ]:
                if item in separation['solvent_name'].lower():
                    solvent_type = 'aq'
            seq.append((purpose, target_layer, solvent_type))
    return seq

def get_to_vessels(
    purpose,
    solvent_type,
    next_purpose,
    next_target_layer,
    next_solvent_type,
    next_purpose2,
    next_target_layer2,
    next_solvent_type2,
):
    """Return step to_vessel and waste_phase_to_vessel based on step purpose
    ('wash' or 'extract'), solvent_type ('aq' or 'org') and next step target
    layer ('aq' or 'org').
    """
    if purpose == 'wash':
        if next_target_layer:
            # Wash, where next separation requires waste layer.
            # Send product layer to group_to and waste layer back to separator.
            if solvent_type == next_target_layer:
                return ('group_to', 'separator')

            # Wash, where next separation requires product layer.
            else:
                # Wash where next separations are wash followed by extract.
                if next_purpose2 and next_purpose2 == 'extract' and next_purpose == 'wash':
                    # First wash should send waste to buffer to be used by extract later
                    return ('separator', 'buffer_flask1')
                else:
                    return ('separator', None)

        else:
            if next_solvent_type == solvent_type:
                return ('separator', None)
            else:
                return ('group_to', 'separator')
            return (None, None)

    elif purpose == 'extract':
        if next_target_layer:
            if solvent_type == next_target_layer:
                return ('separator', None)
            else:
                return ('group_to', 'separator')
        else:
            if next_solvent_type != solvent_type:
                return ('separator', None)
            else:
                return ('group_to', 'separator')
            return (None, None)
    return None

def sanitize_separation_vessels(action_list):
    """Vessels used in separation need to take action subject into account,
    e.g. 'the combined aqueous layers were extracted', could mean waste phases
    need to be retained for further extraction. Do this here.
    """
    # Get groups of consecutive separations steps
    sep_groups = get_separation_groups(action_list)
    for grp in sep_groups:
        # Get simplified separation sequence [(purpose, target_layer, solvent_type)...]
        # where target_layer and solvent_type are either 'org' or 'aq' (Organic or aqueous),
        # and purpose is either 'wash' or 'extract'.
        simple_sep_seq: Tuple[str, str,
                              str] = get_simplified_separation_sequence(grp)

        # List to hold all separations in. Different to grp as some items in grp
        # correspond to multiple separations
        separations = []
        i = 0
        for sep in grp:
            # Don't include combined flag that triggers Transfer step if there has only
            # been 1 previous separation
            if sep.combined and i < 2:
                sep.combined = False
            if not sep.separations:
                separations.append({})
                i += 1
            for separation in sep.separations:
                separations.append(separation)
                i += 1

        for i, item in enumerate(simple_sep_seq):
            purpose, target_layer, solvent_type = item
            separations[i]['to_vessel'] = None
            separations[i]['waste_phase_to_vessel'] = None
            separations[i]['from_vessel'] = None

            next_purpose2, next_target_layer2, next_solvent_type2 = None, None, None
            if i + 2 < len(simple_sep_seq):
                next_purpose2, next_target_layer2, next_solvent_type2 = simple_sep_seq[i + 2]
            if i + 1 < len(simple_sep_seq):
                next_purpose, next_target_layer, next_solvent_type = simple_sep_seq[i + 1]

                to_vessel, waste_phase_to_vessel = get_to_vessels(
                    purpose,
                    solvent_type,
                    next_purpose,
                    next_target_layer,
                    next_solvent_type,
                    next_purpose2,
                    next_target_layer2,
                    next_solvent_type2,
                )
                separations[i]['to_vessel'] = to_vessel
                separations[i]['waste_phase_to_vessel'] = waste_phase_to_vessel

            if i > 0:
                separations[i]['from_vessel'] = 'separator'

def postprocess_action_list(action_list):
    sanitize_separation_vessels(action_list)


###########################
### ADDITION SANITIZERS ###
###########################

def sanitize_add_action(add_action: Action) -> Action:
    """Sanitize Action where AddWord is the action word.

    Args:
        add_action (Action): Action to sanitize.

    Returns:
        Action: Sanitized action.
    """
    add_action.time = None
    add_action.temp = None
    add_action.slow_addition = False
    add_action.dropwise = False
    add_action.time_reagent_cutoff = None
    add_action.explicit_stirring = False
    add_action.slow_stirring = False
    add_action.fast_stirring = False
    add_action.column = False
    add_action.evaporate = False
    add_action.filter = False
    add_action.wash_solid = False
    add_action.through = None
    add_action.mass_at_interval = None
    add_action.n_portions = None
    add_action.transfer_to_separator = False
    add_action.flask_rinse = False
    add_action.forced_vessels = {}
    add_action.viscous = False

    reagents = []
    if str(add_action.action) == 'used':
        if (isinstance(add_action.subject, AbstractReagentWord)
            and type(add_action.subject) != ReagentPlaceholderWord
                and not 'resulting' in str(add_action.subject)):
            if not hasattr(add_action.subject, 'used'):
                reagents.extend(sanitize_reagent(add_action.subject))
                add_action.subject.used = True

        for mod in add_action.modifiers:
            if type(mod) == MethodModifier:
                if 'rinse' in str(mod) and any([isinstance(word, VesselWord) for word in mod.words]):
                    add_action.flask_rinse = True
                for word in mod.words:
                    if isinstance(word, AbstractReagentWord):
                        for item in ['na2so4', 'celite', 'mgso4', 'cotton wool', 'alumina']:
                            if item in str(word).lower():
                                add_action.through = word.name.replace(
                                    'the ', '')
                        if not add_action.through:
                            add_action.wash_solid = True
                            return sanitize_washsolid_action(add_action)

        add_action.reagents = reagents
        return add_action

    # Generally, only ReagentPlaceholderWords are transferred so shouldn't explicitly
    # be included. If something is 'transferred, along with X...', addition of X
    # should be explicitly included.
    elif str(add_action.action) == 'transferred':
        if (isinstance(add_action.subject, AbstractReagentWord)
                and type(add_action.subject) != ReagentPlaceholderWord):
            if not (type(add_action.subject) == ReagentWord and not (add_action.subject.volume or add_action.subject.mass)):
                # This is a bit hacky but necessary.
                # If a subject is used by two actions, one of which is spawned by a
                # second modifier group, only the first one should add the subject.
                if not hasattr(add_action.subject, 'used'):
                    reagents.extend(sanitize_reagent(add_action.subject))
                    add_action.subject.used = True

    else:
        # This is a bit hacky but necessary.
        # If a subject is used by two actions, one of which is spawned by a
        # second modifier group, only the first one should add the subject.
        if not hasattr(add_action.subject, 'used'):
            reagents.extend(sanitize_reagent(add_action.subject))
            add_action.subject.used = True

    if 'viscous' in str(add_action.subject):
        add_action.viscous = True

    def process_reagent_modifier(reagent_modifier):
        initial_reagent_length = len(reagents)
        # 'X was added to Y', Y should be added first.
        if reagent_modifier.preposition in TO_PREPOSITIONS:
            # Time should only apply to Y addition
            add_action.time_reagent_cutoff = ('after', len(reagents) - 1)
            for reagent in reagent_modifier.reagents:
                for item in sanitize_reagent(reagent):
                    reagents.insert(0, item)

        # 'X was charged with Y', X should be added first.
        elif reagent_modifier.preposition in WITH_PREPOSITIONS:
            # Time should only apply to Y addition.
            add_action.time_reagent_cutoff = ('before', len(reagents) - 1)
            for reagent in reagent_modifier.reagents:
                reagents.extend(sanitize_reagent(reagent))

        # If no preposition assume 'with' type preposition.
        else:
            # Time should only apply to Y addition
            add_action.time_reagent_cutoff = ('before', len(reagents) - 1)
            for reagent in reagent_modifier.reagents:
                reagents.extend(sanitize_reagent(reagent))

        # Get what is being added to what correct in this case:
        # 'The rxn mixture is poured into hexanes (500 mL).'
        # Don't apply to 'X was poured into the solution'.
        reagents_found = len(reagents) != initial_reagent_length
        if str(reagent_modifier).startswith('into ') and reagents_found:
            add_action.forced_vessels[reagents[-1].name] = 'split_with_next'

    def process_method_or_addition_modifier(modifier):

        for word in SLOW_ADDITION_WORDS:
            if word in str(modifier):
                add_action.slow_addition = True
                break

        for word in DROPWISE_ADDITION_WORDS:
            if word in str(modifier):
                add_action.dropwise = True
                break

        if type(modifier) == AdditionModifier:
            if modifier.mass_at_interval:
                add_action.mass_at_interval = modifier.mass_at_interval

            if modifier.n_portions:
                add_action.n_portions = modifier.n_portions

        if 'column' in str(modifier):
            add_action.column = True
            return add_action

        if 'separat' in str(modifier) and str(add_action.action) in [
                'transferred', 'poured']:
            add_action.transfer_to_separator = True

        for word in ['porosity', 'filtration', 'pad']:
            if word in str(modifier):
                add_action.filter = True
                return sanitize_filter_action(add_action)

        return None

    def process_time_modifier(time_modifier):
        add_action.time = time_modifier.time

    def process_temp_modifier(temp_modifier):
        add_action.temp = temp_modifier.temp

    def process_technique_mod(technique_modifier):
        add_action.evaporate = True
        return sanitize_evaporate_action(add_action)

    def process_stirring_modifier(stirring_modifier):
        if any([word in str(stirring_modifier) for word in FAST_STIRRING_WORDS]):
            add_action.fast_stirring = True
            add_action.explicit_stirring = True

        elif any([word in str(stirring_modifier) for word in SLOW_STIRRING_WORDS]):
            add_action.slow_stirring = True
            add_action.explicit_stirring = True

    mod_processors = {
        TemperatureModifier: process_temp_modifier,
        StirringModifier: process_stirring_modifier,
        TechniqueModifier: process_technique_mod,
        TimeModifier: process_time_modifier,
        MethodModifier: process_method_or_addition_modifier,
        AdditionModifier: process_method_or_addition_modifier,
        ReagentModifier: process_reagent_modifier,
    }

    process_modifiers(add_action, mod_processors)

    add_action.reagents = reagents
    return add_action

def sanitize_reagent(
    reagent: Union[ReagentWord, ReagentGroupWord, SolutionWord]
) -> List[ReagentWord]:
    """Unpack ReagentWords from variety of word types found in ReagentModifiers
    and return as list.

    Args:
        reagent (Union[ReagentWord, ReagentGroupWord, SolutionWord]): Word to
            unpack.

    Returns:
        List[ReagentWord]: List of ReagentWords nested inside reagent.
    """
    reagents = []
    if type(reagent) == SolutionWord:
        reagents.append(reagent)

    elif type(reagent) == ReagentGroupWord:
        for sub_reagent in reagent:
            reagents.extend(sanitize_reagent(sub_reagent))

    elif type(reagent) == ReagentWord:
        if reagent.minimum_volume and not reagent.volume and not reagent.mass:
            reagent.quantities.append(
                VolumeWord([
                    NumberWord(Word(f'{DEFAULT_MINIMUM_VOLUME}')),
                    VolumeUnitWord(Word('mL'))
                ])
            )
        reagents.append(reagent)

    elif type(reagent) == MixtureWord:
        reagents.append(reagent)
    return reagents

def sanitize_dissolve_action(dissolve_action: Action) -> Action:
    """Sanitize Action where DissolveWord is the action word.

    Args:
        dissolve_action (Action): Action to sanitize.

    Returns:
        Action: Sanitized action.
    """
    solvents = []
    temp = 25

    for modifier in dissolve_action.modifiers:
        # Get solvents
        if type(modifier) == ReagentModifier:
            for reagent in modifier.reagents:
                solvents.extend(sanitize_reagent(reagent))

            # Get temp from reagent
            reagent_temp = None
            for solvent in solvents:
                reagent_temp = get_reagent_temp(solvent)
                if reagent_temp != None:
                    break
            if reagent_temp != None:
                temp = reagent_temp

        # Get temp from temperature modifier
        elif type(modifier) == TemperatureModifier:
            temp = str(modifier.temp)

    dissolve_action.solvents = solvents
    dissolve_action.temp = temp
    dissolve_action.volumes = []

    # Get solvent volumes
    if dissolve_action.solvents:
        for solvent in dissolve_action.solvents:
            if solvent.volume:
                dissolve_action.volumes.append(str(solvent.volume))
            else:
                dissolve_action.volumes.append(0)

    dissolve_action.solutes = sanitize_reagent(dissolve_action.subject)
    return dissolve_action

def sanitize_mix_action(mix_action: Action) -> Action:
    """Sanitize Action where MixWord is the action word.

    Args:
        mix_action (Action): Action to sanitize.

    Returns:
        Action: Sanitized action.
    """
    return sanitize_add_action(mix_action)

def sanitize_dilute_action(dilute_action: Action) -> Action:
    """Sanitize Action where DiluteWord is the action word.

    Args:
        dilute_action (Action): Action to sanitize.

    Returns:
        Action: Sanitized action.
    """
    return sanitize_add_action(dilute_action)

def sanitize_neutralize_action(neutralize_action: Action) -> Action:
    """Sanitize Action where NeutralizeWord is the action word.

    Args:
        neutralize_action (Action): Action to sanitize.

    Returns:
        Action: Sanitized action.
    """
    reagents = []
    neutralize_action.temp = None
    neutralize_action.stir = False
    for modifier in neutralize_action.modifiers:
        if type(modifier) == ReagentModifier:
            reagents.extend(modifier.reagents)
        elif type(modifier) == StirringModifier:
            neutralize_action.stir = True
        elif type(modifier) == TemperatureModifier:
            neutralize_action.temp = modifier.temp
    neutralize_action.reagents = reagents
    return neutralize_action


#############################
### SEPARATION SANITIZERS ###
#############################

def sanitize_wash_action(wash_action: Action) -> Action:
    """Sanitize Action where WashWord is the action word.

    Args:
        wash_action (Action): Action to sanitize.

    Returns:
        Action: Sanitized action.
    """
    wash_action.addition_funnel = False
    wash_action.flask_wash = False
    if re.match(r'([aA]n|[tT]he) (same )?addition funnel', str(wash_action.subject)):
        wash_action.addition_funnel = True
        return sanitize_add_action(wash_action)

    elif isinstance(wash_action.subject, VesselWord):
        wash_action.flask_wash = True
        return sanitize_add_action(wash_action)
    return sanitize_separate_action(wash_action)

def sanitize_extract_action(extract_action: Action) -> Action:
    """Sanitize Action where ExtractWord is the action word.

    Args:
        extract_action (Action): Action to sanitize.

    Returns:
        Action: Sanitized action.
    """
    return sanitize_separate_action(extract_action)

def sanitize_separate_action(separate_action: Action) -> Action:
    """Sanitize Action where ExtractWord or WashWord is the action word.

    Args:
        separate_action (Action): Action to sanitize.

    Returns:
        Action: Sanitized action.
    """
    solvent = None
    separate_action.product_bottom = True
    separate_action.repeats = 1
    separate_action.solvent_volumes = []
    separate_action.solvent_names = []
    separate_action.separations = []
    separate_action.combined = False

    if 'combined' in str(separate_action.subject):
        separate_action.combined = True

    for modifier in separate_action.modifiers:
        if type(modifier) == RepeatModifier:
            separate_action.repeats = modifier.repeats

        elif type(modifier) == ReagentModifier and len(modifier.reagents) > 0:
            for solvent in modifier.reagents:
                if type(solvent) != ReagentPlaceholderWord:
                    separation = {
                        'solvent_name': '',
                        'repeats': 1,
                        'solvent_volume': 0,
                    }
                    if solvent.name:
                        separation['solvent_name'] = solvent.name
                    if modifier.n_portions > 1:
                        separation['repeats'] = modifier.n_portions

                    if type(solvent.volume) == RepeatedVolumeWord:
                        separation['repeats'] = solvent.volume.multiplier

                        if solvent.volume.volume:
                            separation['solvent_volume'] = str(
                                solvent.volume.volume)

                    elif solvent.volume:
                        separation['solvent_volume'] = str(solvent.volume)

                    else:
                        separation['solvent_volume'] = None
                    separate_action.separations.append(separation)
    return separate_action


#########################
### FILTER SANITIZERS ###
#########################

def sanitize_filter_action(filter_action: Action) -> Action:
    """Sanitize action where FilterWord is the action word.

    Args:
        filter_action (Action): Action to sanitize.

    Returns:
        Action: Sanitized action.
    """
    # Two distinct kinds of filtration. Plain Filter, and FilterThrough.
    # FilterThrough is used when 'filtered through a pad of celite' or similar
    # is encountered. If FilterThrough is being used 'eluting with ReagentWord'
    # is also taken into account.
    filter_action.through = None
    filter_action.eluting_solvent = None
    filter_action.eluting_volume = 1
    filter_action.eluting_repeats = 1

    def process_reagent_mod(reagent_mod):
        for word in reagent_mod.words:
            if isinstance(word, AbstractReagentWord):
                filter_action.eluting_solvent = word
                if type(filter_action.eluting_solvent.volume) == RepeatedVolumeWord:
                    filter_action.eluting_volume = str(word.volume.volume)
                    filter_action.eluting_repeats = word.volume.multiplier
                else:
                    filter_action.eluting_volume = str(word.volume)
                    filter_action.eluting_repeats = 1

    def process_method_mod(method_mod):
        if 'alumina' in str(method_mod).lower():
            filter_action.through = 'alumina'
        elif 'silica' in str(method_mod).lower():
            filter_action.through = 'silica'
        elif 'cotton wool' in str(method_mod).lower():
            filter_action.through = 'cotton wool'

    def process_technique_mod(technique_mod):
        if str(technique_mod).startswith('through '):
            if 'celite' in str(technique_mod).lower():
                filter_action.through = 'celite'
            elif 'silica' in str(technique_mod) and 'gel' in str(technique_mod):
                filter_action.through = 'silica-gel'
            elif 'filter paper' in str(technique_mod):
                filter_action.through = None
            else:
                filter_action.through = str(
                    technique_mod).replace('through ', '', 1)

    mod_processors = {
        TechniqueModifier: process_technique_mod,
        ReagentModifier: process_reagent_mod,
        MethodModifier: process_method_mod,
    }

    process_modifiers(filter_action, mod_processors)

    if str(filter_action.action).startswith('eluted'):
        if filter_action.eluting_solvent and filter_action.eluting_volume:
            if not filter_action.through:
                filter_action.through = 'prev_through'

    # Needs to be like this so 'flushed with nitrogen' doesn't cause FilterThrough
    elif str(filter_action.action).startswith('flushed'):
        if filter_action.eluting_solvent and filter_action.eluting_volume:
            if not filter_action.through:
                filter_action.through = 'prev_through'
        else:
            return None

    return filter_action

def sanitize_isolate_action(isolate_action: Action) -> Action:
    """Sanitize Action where IsolationWord is the action word.

    Args:
        isolation_action (Action): Action to sanitize.

    Returns:
        Action: Sanitized action.
    """
    isolate_action.filter = False
    for modifier in isolate_action.modifiers:
        # If TechniqueModifier i.e. 'isolate by vacuum filtration' set filter
        # bool to True
        if type(modifier) == TechniqueModifier:
            phrase = ' '.join([str(word) for word in modifier.words])
            if 'filtration' in phrase:
                isolate_action.filter = True
                isolate_action = sanitize_filter_action(isolate_action)
    return isolate_action

def sanitize_remove_action(remove_action: Action) -> Action:
    """Sanitize Action where RemoveWord is the action word.

    Args:
        remove_action (Action): Action to sanitize.

    Returns:
        Action: Sanitized action.
    """
    remove_action.filter = False
    remove_action.dry = False
    remove_action.evaporate = False
    remove_action.discontinue_heatchill = False

    # 'The oil bath was removed...'
    if 'bath' in str(remove_action.subject):
        remove_action.discontinue_heatchill = True

    else:
        for modifier in remove_action.modifiers:
            # If TechniqueModifier i.e. 'the solvent was removed by filtration'
            # set filter bool to True
            if type(modifier) == TechniqueModifier:
                phrase = ' '.join([str(word) for word in modifier.words])
                if 'filtration' in phrase:
                    remove_action.filter = True
                    return sanitize_filter_action(remove_action)

                elif str(phrase) in EVAPORATE_REMOVE_PHRASES:
                    remove_action.evaporate = True
                    return sanitize_evaporate_action(remove_action)

                elif 'evaporat' in str(modifier):
                    remove_action.evaporate = True
                    return sanitize_evaporate_action(remove_action)

            elif type(modifier) == MethodModifier:
                if 'evaporat' in str(modifier):
                    remove_action.evaporate = True
                    return sanitize_evaporate_action(remove_action)

                elif 'higher vacuum' in str(modifier) or 'vacuum line' in str(modifier):
                    remove_action.dry = True
                    return sanitize_dry_action(remove_action)
    return remove_action

def sanitize_washsolid_action(washsolid_action: Action) -> Action:
    """Sanitize Action where WashSolidWord is the action word.

    Args:
        washsolid_action (Action): Action to sanitize.

    Returns:
        Action: Sanitized action.
    """
    washsolid_action.solvents = []
    washsolid_action.repeats = 1
    washsolid_action.temp = None
    washsolid_action.anticlogging = False
    if str(washsolid_action.action) == 'used':
        washsolid_action.solvents.extend(
            sanitize_reagent(washsolid_action.subject))

    if 'gummy' in str(washsolid_action.subject):
        washsolid_action.anticlogging = True

    for modifier in washsolid_action.modifiers:
        if type(modifier) == ReagentModifier:
            for reagent in modifier.reagents:
                washsolid_action.solvents.extend(sanitize_reagent(reagent))

                reagent_temp = get_reagent_temp(reagent)
                if reagent_temp != None:
                    washsolid_action.temp = reagent_temp

            if modifier.n_portions > 1:
                washsolid_action.repeats = modifier.n_portions

        elif type(modifier) == RepeatModifier:
            washsolid_action.repeats = modifier.repeats

        elif type(modifier) == TemperatureModifier:
            washsolid_action.temp = str(modifier.temp)

    return washsolid_action

def sanitize_dry_action(dry_action: Action) -> Action:
    """Sanitize Action where DryWord is the action word.

    Args:
        dry_action (Action): Action to sanitize.

    Returns:
        Action: Sanitized action.
    """
    dry_action.temp = None
    dry_action.time = 'default'
    dry_action.pressure = 'default'
    dry_action.filter_through = None

    def process_time_mod(time_mod):
        dry_action.time = str(time_mod.time)
        phrase = ' '.join([str(word) for word in time_mod.words])
        if phrase == 'as long as possible':
            dry_action.time = DEFAULT_AS_DRY_AS_POSSIBLE_DRYING_TIME

    def process_temp_mod(temp_mod):
        dry_action.temp = str(temp_mod.temp)

    def process_reagent_mod(reagent_mod):
        dry_action.filter_through = reagent_mod.reagents

    def process_technique_mod(technique_mod):
        if 'standing over' in str(technique_mod):
            dry_action.filter_through = [
                word
                for word in technique_mod.words
                if isinstance(word, AbstractReagentWord)
            ]

    def process_pressure_mod(pressure_mod):
        dry_action.pressure = str(pressure_mod.pressure)

    def process_details_mod(details_mod):
        words_list = details_mod.words[0].words
        for word in words_list:
            if type(word) == QuantityGroupWord:
                words_list = word.words
                break

        for word in words_list:
            if type(word) == TempWord:
                dry_action.temp = word.quantity

            elif type(word) == PressureWord:
                dry_action.pressure = str(word)

            elif type(word) == PressureModifier:
                process_pressure_mod(word)

            elif type(word) == TemperatureModifier:
                process_temp_mod(word)

            elif type(word) == TimeModifier:
                process_time_mod(word)

            elif type(word) == TimeWord:
                dry_action.time = str(word)

            elif isinstance(word, AbstractReagentWord):
                dry_action.filter_through = [word]

    mod_processors = {
        TimeModifier: process_time_mod,
        TemperatureModifier: process_temp_mod,
        PressureModifier: process_pressure_mod,
        TechniqueModifier: process_technique_mod,
        ReagentModifier: process_reagent_mod,
        DetailsModifier: process_details_mod,
    }

    process_modifiers(dry_action, mod_processors)
    return dry_action

def sanitize_press_action(press_action: Action) -> Action:
    press_action = sanitize_dry_action(press_action)
    for modifier in press_action.modifiers:
        if type(modifier) == MethodModifier:
            if (' '.join([str(word) for word in modifier.words])
                    == 'as dry as possible'):
                press_action.time = DEFAULT_AS_DRY_AS_POSSIBLE_DRYING_TIME
    return press_action


###########################
### REACTION SANITIZERS ###
###########################

def sanitize_reflux_action(reflux_action: Action) -> Action:
    """Sanitize Action where RefluxWord is the action word.

    Args:
        reflux_action (Action): Action to sanitize.

    Returns:
        Action: Sanitized action.
    """
    reflux_action.temp = REFLUX_PLACEHOLDER_TEMP
    reflux_action.time = DEFAULT_STIRRING_TIME
    for modifier in reflux_action.modifiers:
        if type(modifier) == TemperatureModifier:
            reflux_action.temp = modifier.temp
        elif type(modifier) == TimeModifier:
            reflux_action.time = modifier.time
    return reflux_action

def sanitize_stir_action(stir_action: Action) -> Action:
    """Sanitize Action where StirWord is the action word.

    Args:
        stir_action (Action): Action to sanitize.

    Returns:
        Action: Sanitized action.
    """
    stir_action.temp = None
    stir_action.slow_temp = False
    stir_action.time = DEFAULT_STIRRING_TIME
    stir_action.reagents = []
    stir_action.speed = None
    stir_action.stir_speed = 'default'
    if stir_action.action_order_pos == 0:
        stir_action.reagents.extend(sanitize_reagent(stir_action.subject))

    for modifier in stir_action.modifiers:
        if type(modifier) == TemperatureModifier:
            if type(modifier.temp) == TempWord:
                stir_action.temp = modifier.temp.quantity

            elif type(modifier.temp) in [int, float]:
                stir_action.temp = modifier.temp

        elif type(modifier) == TimeModifier:
            stir_action.time = modifier.time

        elif type(modifier) == MethodModifier:
            if 'thoroughly' in ' '.join([str(word) for word in modifier.words]):
                stir_action.time = DEFAULT_THOROUGH_STIR_TIME

            elif 'vigorous' in str(modifier):
                stir_action.speed = 'fast'

            elif 'slow' in str(modifier):
                stir_action.speed = 'slow'

            if str(modifier) == 'with slow warming':
                stir_action.slow_temp = True

        elif type(modifier) == ReagentModifier:
            for reagent in modifier.reagents:
                stir_action.reagents.extend(sanitize_reagent(reagent))

        elif type(modifier) == StirringModifier:
            stir_action.stir_speed = modifier.stir_speed

    return stir_action

def sanitize_wait_action(wait_action: Action) -> Action:
    """Sanitize Action where WaitWord is the action word.

    Args:
        wait_action (Action): Action to sanitize.

    Returns:
        Action: Sanitized action.
    """
    if 'cool' in str(wait_action):
        wait_action.purpose = 'cool'
    else:
        wait_action.purpose = 'heat'
    return sanitize_heatchill_action(wait_action)

def sanitize_cool_action(cool_action: Action) -> Action:
    """Sanitize Action where CoolWord is the action word.

    Args:
        cool_action (Action): Action to sanitize.

    Returns:
        Action: Sanitized action.
    """
    cool_action.purpose = 'cool'
    return sanitize_heatchill_action(cool_action)

def sanitize_heat_action(heat_action: Action) -> Action:
    """Sanitize Action where HeatWord is the action word.

    Args:
        heat_action (Action): Action to sanitize.

    Returns:
        Action: Sanitized action.
    """
    heat_action.purpose = 'heat'
    return sanitize_heatchill_action(heat_action)

def sanitize_heatchill_action(heatchill_action: Action) -> Action:
    """Sanitize Action where HeatWord or CoolWord is the action word.

    Args:
        cool_action (Action): Action to sanitize.

    Returns:
        Action: Sanitized action.
    """
    heatchill_action.temp = 25
    heatchill_action.time = None
    heatchill_action.stir = 'default'
    heatchill_action.stir_speed = 'default'
    heatchill_action.active = None

    # Determine whether cooling is needed or simply, being allowed to cool.
    if ('allow' in ' '.join([str(word) for word in heatchill_action.action.words])):
        if heatchill_action.active == None:
            heatchill_action.active = False

    for modifier in heatchill_action.modifiers:

        if type(modifier) == TemperatureModifier and modifier.temp != None:
            if type(modifier.temp) == TempWord:
                heatchill_action.temp = modifier.temp.quantity

            elif type(modifier.temp) in [int, float]:
                heatchill_action.temp = modifier.temp

            else:
                raise TypeError(
                    f'Invalid type {type(modifier.temp)} used in temperature modifier {str(modifier)}')

        elif type(modifier) == TimeModifier:

            if 'briefly' in str(modifier):
                heatchill_action.time = DEFAULT_BRIEF_TIME

            # Ramping heatchill doesn't work yet so just ignore it to avoid
            # over heatchilling, e.g. 'heated to 85 C over 30 mins'.
            # Allow inactive cooling over a time.
            elif not 'over' in str(modifier):
                heatchill_action.time = modifier.time

        elif type(modifier) == StirringModifier:
            heatchill_action.stir = True
            heatchill_action.stir_speed = modifier.stir_speed

        elif type(modifier) == TechniqueModifier:
            if 'stirring' in str(modifier):
                heatchill_action.stir = True

        elif type(modifier) == MethodModifier:
            if ('room temperature' in str(modifier)
                    and 'water bath' in str(modifier)):
                heatchill_action.active = True

    if heatchill_action.active == None:
        heatchill_action.active = True

    return heatchill_action


#######################
### MISC SANITIZERS ###
#######################

def sanitize_discontinue_action(discontinue_action):
    discontinue_action.stop_actions = []
    for word in discontinue_action.action.words:
        if isinstance(word, ActionWord) and type(word) != DiscontinueWord:
            if type(word) in [HeatWord, CoolWord, RefluxWord]:
                discontinue_action.stop_actions.append('heatchill')
            elif type(word) in [StirWord]:
                discontinue_action.stop_actions.append('stir')
    return discontinue_action

def sanitize_continue_action(continue_action):
    # 'Stirring was continued at this temperature for 1 hr...'
    continue_action.continue_action = None
    if type(continue_action.subject) in [StirWord]:
        continue_action.continue_action = 'stir'
        continue_action = sanitize_stir_action(continue_action)

    elif type(continue_action.subject) in [HeatWord, CoolWord]:
        continue_action.continue_action = 'heatchill'
        continue_action.purpose = {
            HeatWord: 'heat',
            CoolWord: 'cool'
        }[type(continue_action.subject)]
        continue_action = sanitize_heatchill_action(continue_action)

    return continue_action

def sanitize_purify_action(purify_action):
    purify_action.column, purify_action.recrystallize = False, False
    purify_action.filtration = False
    for modifier in purify_action.modifiers:
        if type(modifier) == TechniqueModifier:
            if 'chromatography' in str(modifier):
                purify_action.column = True

            elif 'recrystalli' in str(modifier):
                purify_action.recrystallize = True
                return sanitize_recrystallize_action(purify_action)

            elif 'filtration' in str(modifier):
                purify_action.filtration = True
                return sanitize_filter_action(purify_action)

    return purify_action

def sanitize_time_modifier_action(time_modifier_action):
    time_modifier_action.time = str(time_modifier_action.action.time)
    # Set these to None for compatibility with wait action XDL converter
    time_modifier_action.temp, time_modifier_action.stir = None, None
    return time_modifier_action

def sanitize_achieve_action(achieve_action):
    achieve_action.purify = False

    if str(achieve_action.subject).lower() == 'purification':
        achieve_action.purify = True
        return sanitize_purify_action(achieve_action)

    return achieve_action

def sanitize_provide_action(provide_action):
    provide_action.column = False
    if 'chromatography' in str(provide_action.subject):
        provide_action.column = True
    return provide_action

def sanitize_subjected_action(subjected_action):
    subjected_action.distill, subjected_action.column = False, False
    for modifier in subjected_action.modifiers:
        if type(modifier) == TechniqueModifier:
            if 'distillation' in str(modifier):
                subjected_action.distill = True
                return sanitize_distill_action(subjected_action)

            elif 'chromatography' in str(modifier):
                subjected_action.column = True
                return sanitize_purify_action(subjected_action)

    return subjected_action

def sanitize_place_action(place_action):
    place_action.addition, place_action.heatchill = False, False
    if (any([type(modifier) == ReagentModifier for modifier in place_action.modifiers])
            or (type(place_action.subject) != ReagentPlaceholderWord
                and isinstance(place_action.subject, AbstractReagentWord))
        ):
        place_action.addition = True
        return sanitize_add_action(place_action)

    for modifier in place_action.modifiers:
        if type(modifier) == TemperatureModifier:
            place_action.heatchill = True
            if modifier.temp < 18:
                place_action.purpose = 'cool'
            else:
                place_action.purpose = 'heat'
            return sanitize_heatchill_action(place_action)

    return place_action

def sanitize_collect_action(collect_action):
    collect_action.filtration = False

    for modifier in collect_action.modifiers:
        if type(modifier) == TechniqueModifier and 'filtration' in str(modifier):
            collect_action.filtration = True
            return sanitize_filter_action(collect_action)

    return collect_action

def sanitize_afford_action(afford_action):
    afford_action.purify = False
    afford_action.column = False
    if 'purif' in str(afford_action.subject):
        afford_action.purify = True
        return sanitize_purify_action(afford_action)

    elif 'chromatography' in str(afford_action.subject):
        afford_action.column = True
        return afford_action
    return afford_action

def sanitize_evaporate_action(evaporate_action):
    evaporate_action.temp = None
    evaporate_action.pressure = None
    evaporate_action.time = None

    def process_quantity_group(quantity_group):
        for quantity in quantity_group:
            if type(quantity) == PressureWord:
                evaporate_action.pressure = str(quantity)
            elif type(quantity) == TempWord:
                evaporate_action.temp = str(quantity)
            elif type(quantity) == TimeWord:
                evaporate_action.time = str(quantity)

    def process_pressure_mod(pressure_mod):
        for subword in pressure_mod.words:
            if type(subword) == PressureWord:
                evaporate_action.pressure = str(subword)
            elif type(subword) == QuantityGroupWord:
                process_quantity_group(subword)

    def process_temp_mod(temp_mod):
        for subword in temp_mod.words:
            if type(subword) == TempWord:
                evaporate_action.temp = str(subword)

    def process_time_mod(time_mod):
        for subword in time_mod.words:
            if type(subword) == TimeWord:
                evaporate_action.time = str(subword)

    def process_details_mod(details_mod):
        # If contains QuantityGroupWord use that instead of modifier for words.
        words_list = details_mod.words[0].words
        for word in words_list:
            if type(word) == QuantityGroupWord:
                words_list = word.words
                break

        for word in words_list:
            if type(word) == TempWord:
                evaporate_action.temp = word.quantity

            elif type(word) == TimeWord:
                evaporate_action.time = str(word)

            elif type(word) == PressureWord:
                evaporate_action.pressure = str(word)

            elif type(word) == TemperatureModifier:
                process_temp_mod(word)

            elif type(word) == TimeModifier:
                process_time_mod(word)

            elif type(word) == PressureModifier:
                process_pressure_mod(word)

            elif type(word) == RangeWord:
                if word.unit in PRESSURE_UNITS:
                    evaporate_action.pressure = str(word)

            elif type(word) == QuantityGroupWord:
                process_quantity_group(word)

    # Map modifier processors
    mod_processors = {
        DetailsModifier: process_details_mod,
        TemperatureModifier: process_temp_mod,
        PressureModifier: process_pressure_mod,
        TimeModifier: process_time_mod,
    }

    # Process modifiers
    res = process_modifiers(evaporate_action, mod_processors)
    if res:
        return res
    return evaporate_action

def sanitize_evacuate_action(evacuate_action: Action) -> Action:
    return evacuate_action

def process_modifiers(action: Action, processors: Dict[type, Callable]) -> None:
    """Given action and modifier processor dict process modifiers updating
    action.

    Args:
        action (Action): Action to get and process modifiers from.
        processors (Dict[type, Callable]): Processor functions for different
            modifier types, e.g. { TimeModifier: process_time_mod }.
    """
    for modifier in action.modifiers:
        mod_type = type(modifier)
        if mod_type in processors:
            res = processors[mod_type](modifier)
            # Processor has assigned the action to a different sanitizer
            if res:
                return res
    return None

def sanitize_combined_action(combined_action):
    combined_action.phases = False
    for word in ['phase', 'layer', 'extracts', 'washings']:
        if word in str(combined_action.subject):
            combined_action.phases = True
    return combined_action

################################
### UNIMPLEMENTED SANITIZERS ###
################################

def sanitize_sonicate_action(sonicate_action):
    return sonicate_action

def sanitize_solution_word(solution_word):
    solution_word.action = None
    return solution_word

def sanitize_recrystallize_action(recrystallize_action):
    return recrystallize_action

def sanitize_require_action(require_action):
    return require_action

def sanitize_distill_action(distill_action):
    return distill_action


#: Dict of { specific_action_word_type: sanitizier_function }
SANITIZE_FN_DICT: Dict[Word, Callable] = {
    StirWord: sanitize_stir_action,
    AddWord: sanitize_add_action,
    RefluxWord: sanitize_reflux_action,
    DissolveWord: sanitize_dissolve_action,
    ExtractWord: sanitize_extract_action,
    EvaporateWord: sanitize_evaporate_action,
    NeutralizeWord: sanitize_neutralize_action,
    WaitWord: sanitize_wait_action,
    MixWord: sanitize_mix_action,
    CoolWord: sanitize_cool_action,
    HeatWord: sanitize_heat_action,
    DiluteWord: sanitize_dilute_action,
    FilterWord: sanitize_filter_action,
    WashWord: sanitize_wash_action,
    WashSolidWord: sanitize_washsolid_action,
    DryWord: sanitize_dry_action,
    PressWord: sanitize_press_action,
    PurifyWord: sanitize_purify_action,
    IsolateWord: sanitize_isolate_action,
    DiscontinueWord: sanitize_discontinue_action,
    RecrystallizeWord: sanitize_recrystallize_action,
    RemoveWord: sanitize_remove_action,
    ContinueWord: sanitize_continue_action,
    AchieveWord: sanitize_achieve_action,
    ProvideWord: sanitize_provide_action,
    SonicateWord: sanitize_sonicate_action,
    RequireWord: sanitize_require_action,
    DistillWord: sanitize_distill_action,
    SubjectedWord: sanitize_subjected_action,
    PlaceWord: sanitize_place_action,
    CollectWord: sanitize_collect_action,
    AffordWord: sanitize_afford_action,
    EvacuateWord: sanitize_evacuate_action,
    CombineWord: sanitize_combined_action,

    # Bit of a weird one. Action is TimeModifier. Used for stuff like
    # 'After 3 h, the solution...' where '3 h' is a TimeModifier.
    TimeModifier: sanitize_time_modifier_action,
}
