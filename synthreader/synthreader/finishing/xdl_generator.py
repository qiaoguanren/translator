from typing import Dict, List, Union, Tuple, Callable
import copy
import logging

from xdl import XDL
from xdl.reagents import Reagent
from xdl.hardware import Hardware, Component
from chemputerxdl.steps import Step, Transfer
#from chemputerxdl.executor.tracking import iter_vessel_contents

from .action_sanitizer import sanitize_actions
from .action_xdl_converters import *
from .vessels import assign_vessels
from .blank_filling import (
    fill_in_blanks, assign_stirring_to_add_steps, get_prepared_xdl_copy)
from .tidyup import tidyup
from ..words.action_words import *
from ..words import VesselWord, AuxiliaryVerbWord
from ..words.modifiers import TimeModifier

#: Dict of { word_type: word_to_xdl_converter_function }
RENDER_XDL_DICT: Dict[Word, Callable] = {
    StirWord: stir_action_to_xdl,
    AddWord: add_action_to_xdl,
    RefluxWord: reflux_action_to_xdl,
    DissolveWord: dissolve_action_to_xdl,
    ExtractWord: extract_action_to_xdl,
    EvaporateWord: evaporate_action_to_xdl,
    NeutralizeWord: neutralize_action_to_xdl,
    WaitWord: wait_action_to_xdl,
    MixWord: mix_action_to_xdl,
    CoolWord: heatchill_action_to_xdl,
    HeatWord: heatchill_action_to_xdl,
    DiluteWord: dilute_action_to_xdl,
    FilterWord: filter_action_to_xdl,
    WashWord: wash_action_to_xdl,
    WashSolidWord: washsolid_action_to_xdl,
    DryWord: dry_action_to_xdl,
    PressWord: press_action_to_xdl,
    PurifyWord: purify_action_to_xdl,
    IsolateWord: isolate_action_to_xdl,
    DiscontinueWord: discontinue_action_to_xdl,
    RecrystallizeWord: recrystallize_action_to_xdl,
    RemoveWord: remove_action_to_xdl,
    TimeModifier: wait_action_to_xdl,
    ContinueWord: continue_action_to_xdl,
    AchieveWord: achieve_action_to_xdl,
    ProvideWord: provide_action_to_xdl,
    SonicateWord: sonicate_action_to_xdl,
    DistillWord: distill_action_to_xdl,
    SubjectedWord: subjected_action_to_xdl,
    PlaceWord: place_action_to_xdl,
    CollectWord: collect_action_to_xdl,
    AffordWord: afford_action_to_xdl,
    EvacuateWord: evacuate_action_to_xdl,
    CombineWord: combine_action_to_xdl,
}

def action_to_xdl(
    action: Union[Action, SolutionWord]
) -> Tuple[List[Step], List[str]]:
    """Convert Action or Solution word to XDL. Specifically return list of Steps
    and list of reagent names.

    Args:
        action (Union[Action, SolutionWord]): Action to convert to XDL, can be
            Action or SolutionWord, as solutions represent an action.

    Returns:
        Tuple[List[Step], List[str]]: (steps, reagents) tuple. Steps are Step
            objects and reagents are just str of reagent names i.e. 'propanol'.
    """
    if type(action) == SolutionWord:
        return solution_word_to_xdl(action)
    else:
        return RENDER_XDL_DICT[type(action.action)](action)

def combine_require_actions(action_list: List[Action]):
    for i in reversed(range(len(action_list))):
        action = action_list[i]
        if type(action.action) == RequireWord:
            if i - 1 >= 0:
                action_list[i - 1].modifiers.extend(action.modifiers)
            action_list.pop(i)
    return action_list

def postprocess_xdl_steps(
    xdl_steps: List[Step],
    step_action_map: Dict[int, Action]
) -> List[Step]:
    """Postprocessing to be performed immediately after creating XDL step list."""
    convert_wash_solid_to_elution(xdl_steps)
    # Go through twice in case there are multiple consecutive empty additions
    transform_empty_additions(xdl_steps)
    transform_empty_additions(xdl_steps)
    remove_no_solvent_separation_steps_at_end(xdl_steps)
    add_filter_anticlogging(xdl_steps)

def add_filter_anticlogging(xdl_steps: List[Step]):
    """If WashSolid action is anticlogging also apply anticlogging to preceding
    Filter step.
    """
    for i, step in enumerate(xdl_steps):
        if i > 0 and type(step) == WashSolid:
            if type(xdl_steps[i - 1]) == Filter and step.anticlogging:
                xdl_steps[i - 1].anticlogging = True
    return xdl_steps

def convert_wash_flask_steps(steps, step_action_map):
    """'The flask from which 2 is transferred is washed with CH2Cl2 (10 mL) to
    ensure that no product is left.' Should be Transfer, Add, Transfer instead
    of Separate.
    """
    i = 0
    while i < len(steps):
        step = steps[i]
        if type(step) == Separate:
            action = step_action_map[(id(step))]
            if str(action.action) in [
                'rinsed', 'washed'] and isinstance(
                    action.subject, (AddWord, AuxiliaryVerbWord, VesselWord)):

                new_add_step = Add(
                    reagent=step.solvent,
                    volume=step.solvent_volume,
                    vessel=steps[i].from_vessel
                )
                new_transfer_step = Transfer(
                    from_vessel=steps[i].from_vessel,
                    to_vessel=steps[i].to_vessel,
                    volume='all'
                )
                new_transfer_step2 = Transfer(
                    from_vessel=steps[i].from_vessel,
                    to_vessel=steps[i].to_vessel,
                    volume=step.solvent_volume,
                )
                step_action_map[id(new_transfer_step)] = action
                step_action_map[id(new_transfer_step2)] = action
                step_action_map[id(new_add_step)] = action
                del steps[i]
                for item in [
                        new_transfer_step2, new_add_step, new_transfer_step]:
                    steps.insert(i, item)
                i += 2

        elif (type(step) == Add
              or (type(step) == Repeat
                  and len(step.children) == 1
                  and type(step.children[0]) == Add)):
            action = step_action_map[(id(step))]

            # Repeat containing just Add
            if type(step) == Repeat:
                repeats = step.repeats
                add_step = step.children[0]
            # Add step
            else:
                repeats = 1
                add_step = step

            if (str(action.action) in ['rinsed', 'washed']
                and isinstance(
                    action.subject, (AuxiliaryVerbWord, VesselWord))):

                j = i - 1
                while j >= 0 and type(steps[j]) in [Repeat, Transfer]:
                    j -= 1
                if j + 1 < i:
                    prev_step = steps[j + 1]
                    add_step.vessel = prev_step.from_vessel
                    new_transfer_step = Transfer(
                        from_vessel=prev_step.from_vessel,
                        to_vessel=prev_step.to_vessel,
                        volume='all'
                    )
                    step_action_map[id(new_transfer_step)] = action
                    if repeats > 1:
                        repeat_step = Repeat(repeats=repeats, children=[
                            add_step,
                            new_transfer_step
                        ])
                        del steps[i]
                        steps.insert(i, repeat_step)
                    else:
                        steps.insert(i + 1, new_transfer_step)
                        i += 1

            elif type(action.action) == AddWord and action.flask_rinse:
                j = i - 1
                while j >= 0 and type(steps[j]) in [Add]:
                    j -= 1

                if j >= 0 and type(steps[j]) == Transfer:
                    initial_transfer = steps.pop(j)
                    steps.insert(i - 1, initial_transfer)
                    step.vessel = initial_transfer.from_vessel
                    new_transfer_step = Transfer(
                        from_vessel=initial_transfer.from_vessel,
                        from_port=initial_transfer.from_port,
                        to_vessel=initial_transfer.to_vessel,
                        to_port=initial_transfer.to_port,
                        volume=step.volume,
                    )
                    step_action_map[id(new_transfer_step)] = action
                    steps.insert(i + 1, new_transfer_step)
                    i += 1

        i += 1
    return steps


def remove_no_solvent_separation_steps_at_end(xdl_steps):
    for i in reversed(range(len(xdl_steps))):
        step = xdl_steps[i]
        if type(step) == Separate and not step.solvent:
            if (i - 1 >= 0 and type(xdl_steps[i - 1]) == Separate
                    and i + 1 < len(xdl_steps) and type(xdl_steps[i + 1]) != Separate):
                xdl_steps.pop(i)
    return xdl_steps

def transform_empty_additions(xdl_steps):
    pops = []
    for i, step in enumerate(xdl_steps):
        if i - 1 >= 0:
            prev_step = xdl_steps[i - 1]
            if type(step) == type(prev_step) == Add:
                if not step.volume and prev_step.volume and step.reagent.lower()[:3] == 'the':
                    if not prev_step.time and step.time:
                        prev_step.time = step.time
                    pops.append(i)
    for i in reversed(pops):
        xdl_steps.pop(i)
    return xdl_steps

def convert_wash_solid_to_elution(xdl_steps):
    """Convert WashSolid step to elution properties in FilterThrough step, if it
    comes immediately after a FilterThrough step.
    """
    pops = []
    for i, step in enumerate(xdl_steps):

        if i > 0 and type(step) == WashSolid and type(xdl_steps[i - 1]) == FilterThrough:
            xdl_steps[i - 1].eluting_solvent = step.solvent
            xdl_steps[i - 1].eluting_volume = step.volume
            xdl_steps[i - 1].eluting_repeats = step.repeat
            pops.append(i)

    for i in reversed(pops):
        xdl_steps.pop(i)
    return xdl_steps

def get_forced_vessels(xdl_steps):
    # Get forced vessels
    forced_vessels = []
    in_sep_block = False

    for i, step in enumerate(xdl_steps):
        # No point applying 'other' vessels at start of procedure hence [2:].
        if type(step) == Add and step.vessel and i > 2:
            forced_vessels.append((step, 'vessel', step.vessel))
            in_sep_block = False

        elif type(step) == Separate:
            if not (i + 1 < len(xdl_steps) and type(xdl_steps[i + 1]) != Separate) and step.to_vessel:
                forced_vessels.append((step, 'to_vessel', step.to_vessel))

            if step.waste_phase_to_vessel:
                forced_vessels.append(
                    (step, 'waste_phase_to_vessel', step.waste_phase_to_vessel))

            if not in_sep_block:
                in_sep_block = True
            else:
                if step.from_vessel:
                    forced_vessels.append(
                        (step, 'from_vessel', step.from_vessel))

        elif type(step) == Dissolve and step.vessel:
            # Dissolve at start of procedure shouldn't use other vessel.
            if i > 2:
                forced_vessels.append((step, 'vessel', step.vessel))
            else:
                step.vessel = None

        elif type(step) == Transfer:
            if step.to_vessel:
                forced_vessels.append((step, 'to_vessel', step.to_vessel))
            if step.from_vessel:
                forced_vessels.append((step, 'from_vessel', step.from_vessel))

        else:
            in_sep_block = False
    return forced_vessels


def action_list_to_xdl(action_list: List[Action]) -> XDL:
    """Convert action list tot XDL object.

    Args:
        action_list (List[Union[Action, SolutionWord]]): List of actions to
            convert to XDL. Actions can be Action or SolutionWord, as solutions
            represent an action.

    Returns:
        XDL: XDL object containing steps, hardware and reagents involved in
            procedure.
    """
    # Get XDL steps and reagents
    action_list = combine_require_actions(action_list)
    action_list = sanitize_actions(action_list)
    print(action_list)
    xdl_steps = []
    xdl_hardware = []
    xdl_reagents = []
    step_action_map = {}
    for action in action_list:
        steps, reagents = action_to_xdl(action)
        xdl_steps.extend(steps)
        xdl_reagents.extend(reagents)

        # Create map so what sentences different steps came from can be tracked
        for step in steps:
            step_action_map[id(step)] = action
    print(xdl_steps,xdl_reagents)

    postprocess_xdl_steps(xdl_steps, step_action_map)

    forced_vessels = get_forced_vessels(xdl_steps)

    # Get initial vessel assignment to work with
    xdl_steps = assign_vessels(xdl_steps, forced_vessels)

    # Remove duplicates and empty reagents
    xdl_reagents = list(set(xdl_reagents))
    xdl_reagents = [Reagent(id=reagent)
                    for reagent in xdl_reagents
                    if reagent]

    # Get initial XDL object
    x = XDL(
        steps=xdl_steps,
        hardware=get_hardware(xdl_steps),
        reagents=xdl_reagents,
        logging_level=logging.CRITICAL
    )

    # for step in x.steps:
    #     for k, v in step.properties.items():
    #         if v == 'buffer_flask1':
    #             print(step.name, step.properties)
    #             break

    # Fill in missing properties using XDL object
    x = fill_in_blanks(x)

    # Reassign vessels
    xdl_steps = assign_vessels(xdl_steps, forced_vessels)

    # Sort to avoid diffs in tests when nothing has really changed.
    xdl_reagents = sorted(xdl_reagents, key=lambda reagent: reagent.id)

    # Create new XDL object with reassigned vessels
    x = XDL(
        steps=xdl_steps,
        hardware=get_hardware(xdl_steps),
        reagents=xdl_reagents,
        logging_level=logging.CRITICAL
    )

    # Assign stirring to Add steps. This comes after fill_in_blanks as it is
    # affected by volumes added during fill_in_blanks
    x_copy = get_prepared_xdl_copy(x)

    #assign_stirring_to_add_steps(x, x_copy)

    # Tidy up XDL and return
    x = tidyup(x)
    xdl_steps = assign_vessels(x.steps, forced_vessels)
    convert_solution_add_to_transfer(xdl_steps)
    x = XDL(
        steps=xdl_steps,
        hardware=get_hardware(xdl_steps),
        reagents=xdl_reagents,
        logging_level=logging.CRITICAL
    )
    convert_wash_flask_steps(xdl_steps, step_action_map)
    add_dry_after_filter_wash(x)

    for step in x.steps:
        print(step.name, step.properties, '\n')

    #remove_unwanted_transfers(x)
    return x

def remove_unwanted_transfers(xdl_obj):
    """If transfers are added explicitly, remove transfer added by vessel assignment
    and make sure explicit transfers are using the right vessels.

    Specifically, if a transfer is transferring from a vessel with nothing in it,
    use the last vessel that was transferred from that had something in it,
    and delete the original transfer.

    Example of why is is needed is second paragraph of Org. Synth. v95p0251
    """
    last_transfer_from = None
    last_transfer_i = -1
    deletions = []
    alterations = []

    xdl_obj_copy = get_prepared_xdl_copy(xdl_obj)

    transfer_i = 0
    prev_vessel_contents = {}
    prev_step, prev_step2 = None, None
    for i, step, vessel_contents, _ in iter_vessel_contents(
            xdl_obj_copy.steps, xdl_obj_copy.executor._graph_hardware):
        if type(step) == Transfer:
            # Buffer flasks never need messed with
            if step.from_vessel == 'buffer_flask1':
                transfer_i += 1
                continue

            # Transferring from empty vessel and transfer is invalid as prev two steps
            # don't reference from_vessel
            if ((not step.from_vessel in prev_vessel_contents
                 or prev_vessel_contents[step.from_vessel].volume <= 0)
                and not step.from_vessel in list(prev_step.properties.values())
                    and (not step.from_vessel in list(prev_step2.properties.values()) or type(prev_step2) == Transfer)):
                if last_transfer_from:
                    alterations.append((transfer_i, last_transfer_from))
                    deletions.append(last_transfer_i)
            else:
                last_transfer_from = step.from_vessel
                last_transfer_i = transfer_i

            transfer_i += 1
        prev_vessel_contents = vessel_contents
        prev_step2 = prev_step
        prev_step = step

    deletions = list(set(deletions))
    transfer_i = 0
    deletion_is = []
    # Get indexes of transfers to delete and alter from_vessels
    for i, step in enumerate(xdl_obj.steps):
        if type(step) == Transfer:
            if transfer_i in deletions:
                deletion_is.append(i)
            for alter_transfer_i, vessel in alterations:
                if alter_transfer_i == transfer_i:
                    step.from_vessel = vessel
            transfer_i += 1

    # Delete unneeded transfers
    for i in reversed(deletion_is):
        xdl_obj.steps.pop(i)

def add_dry_after_filter_wash(xdl_obj: XDL) -> XDL:
    """If there is a sequence Filter, WashSolid, WashSolid... without a Dry step
    at the end, assume there should be a Dry step there and add one. There can
    be any number of WashSolid steps in the sequence.

    Args:
        xdl_obj (XDL): XDL object to add Dry steps to in case described above.

    Returns:
        XDL: xdl_obj with Dry steps added in case described above.
    """
    steps = xdl_obj.steps
    for i in reversed(range(len(steps))):
        if type(steps[i]) == WashSolid:
            # Check to see if there is a Dry step after WashSolid step(s)
            has_dry = False
            j = i + 1
            while j < len(steps):
                if type(steps[j]) == Dry:
                    has_dry = True
                    break
                elif type(steps[j]) == WashSolid:
                    j += 1
                else:
                    has_dry = False
                    break
            # If there is no Dry step, check to see if there is a Filter step
            # preceding the WashSolid step(s)
            if not has_dry:
                has_filter = False
                j = i - 1
                while j >= 0:
                    if type(steps[j]) == Filter:
                        has_filter = True
                        break
                    elif type(steps[j]) == WashSolid:
                        j -= 1
                    else:
                        has_filter = False
                        break
                # If there is a Filter step before the WashSolid step(s) and no
                # Dry step after, add a Dry step with default properties.
                if has_filter:
                    steps.insert(i + 1, Dry(vessel=steps[i].vessel))
    return xdl_obj

def add_dry_after_filter_wash(xdl_obj: XDL) -> XDL:
    """If there is a sequence Filter, WashSolid, WashSolid... without a Dry step
    at the end, assume there should be a Dry step there and add one. There can
    be any number of WashSolid steps in the sequence.

    Args:
        xdl_obj (XDL): XDL object to add Dry steps to in case described above.

    Returns:
        XDL: xdl_obj with Dry steps added in case described above.
    """
    steps = xdl_obj.steps
    for i in reversed(range(len(steps))):
        if type(steps[i]) == WashSolid:
            # Check to see if there is a Dry step after WashSolid step(s)
            has_dry = False
            j = i + 1
            while j < len(steps):
                if type(steps[j]) == Dry:
                    has_dry = True
                    break
                elif type(steps[j]) == WashSolid:
                    j += 1
                else:
                    has_dry = False
                    break
            # If there is no Dry step, check to see if there is a Filter step
            # preceding the WashSolid step(s)
            if not has_dry:
                has_filter = False
                j = i - 1
                while j >= 0:
                    if type(steps[j]) == Filter:
                        has_filter = True
                        break
                    elif type(steps[j]) == WashSolid:
                        j -= 1
                    else:
                        has_filter = False
                        break
                # If there is a Filter step before the WashSolid step(s) and no
                # Dry step after, add a Dry step with default properties.
                if has_filter:
                    steps.insert(i + 1, Dry(vessel=steps[i].vessel))
    return xdl_obj

def convert_solution_add_to_transfer(steps):
    """If something is dissolved then added to the main reaction mixture, the
    Add step should be replaced with a Transfer step.

    Args:
        steps (List[Step]): Steps to replace Add steps immediately after Dissolve
            steps with Transfer steps.
    """
    insertions = []
    for i, step in enumerate(steps):
        if type(step) == Dissolve:
            if (i + 1 < len(steps)
                and type(steps[i + 1]) == Add
                    and step.vessel != steps[i + 1].vessel):
                steps[i + 1] = Transfer(from_vessel=step.vessel,
                                        to_vessel=steps[i + 1].vessel,
                                        volume='all',
                                        time=steps[i + 1].time,
                                        move_speed=steps[i + 1].move_speed,
                                        dispense_speed=steps[i
                                                             + 1].dispense_speed,
                                        aspiration_speed=steps[i + 1].aspiration_speed)
                if i + 2 < len(steps) and type(steps[i + 2]) == Add:
                    steps[i + 2].vessel = step.vessel
                    insertions.append((i + 3, Transfer(from_vessel=step.vessel,
                                                       to_vessel=steps[i
                                                                       + 1].to_vessel,
                                                       volume='all')))
    for i, step in reversed(insertions):
        steps.insert(i, step)

def get_hardware(steps):
    """Get hardware necessary for given steps."""
    components = []
    cartridges = []
    hardware = []
    for step in steps:
        if 'through' in step.properties and step.through:
            cartridges.append(step.through)
        for prop, val in step.properties.items():
            if ('vessel' in prop or 'rotavap_name' in prop or 'column' in prop) and val and type(val) == str:
                components.append(val)
    for component in list(set(components)):
        # name usually == type except for buffer flask
        # reactor -> reactor, filter -> filter etc
        # buffer_flask -> flask
        component_type = component
        if component == 'buffer_flask1':
            component_type = 'flask'
        hardware.append(Component(id=component, component_type=component_type))
    for cartridge in list(set(cartridges)):
        hardware.append(Component(
            id=f'cartridge_{cartridge}',
            component_type='cartridge',
            chemical=cartridge))
    return Hardware(sorted(hardware, key=lambda x: x.id))
