from typing import List, Tuple, Dict
import copy

from chemputerxdl.steps import Step, Transfer, Add, Separate, Filter, Evaporate
from xdl.steps.special_steps import Repeat
from xdl.hardware import Component

from .constants import (
    STEP_VESSEL_CHAINS,
    COMPONENT_CLASS_NAME_DICT,
    DEFINITE_VESSELS,
    MAX_FILTER_TEMP,
    TRANSFER_BEFORE_STEPS,
    FINAL_TRY_STEP_VESSEL_CHAINS
)

# Bug catcher
for step, vessels in STEP_VESSEL_CHAINS.items():
    try:
        assert all([type(vessel) == list for vessel in vessels])
    except AssertionError:
        raise TypeError(
            f'All vessels in vessel chain must be lists. Problem: {step.__name__}')

class VesselChainLink(object):
    """Convenience class to store each link in vessel chain.

    Attributes:
        vessel_keyword (str): Vessel keyword as used as key in step properties
            dict.
        resolution_rule (Union[str, List[str]]): Rules by which to resolve
            what this vessel should be. Described fully in constants.py.
        step (Step): Step that this vessel belongs to.
        assigned_vessel (str): Definite vessel name assigned to this link in
            vessel chain.
    """

    def __init__(self, vessel_keyword, resolution_rule, step, assigned_vessel):
        self.vessel_keyword = vessel_keyword
        self.resolution_rule = resolution_rule
        self.step = step
        self.assigned_vessel = assigned_vessel

    def __str__(self):
        return f'VesselChainLink: keyword={self.vessel_keyword}, rule={self.resolution_rule}, step={type(self.step).__name__}, assigned={self.assigned_vessel}'

def get_vessel_chain_links(step, forced_vessels):
    step_vessel_chain = copy.deepcopy(STEP_VESSEL_CHAINS[type(step)])
    # if type(step) == Separate:
    #     separate_before = i-1 >= 0 and type(steps[i-1]) == Separate
    #     separate_after = i+1 < len(steps) and type(steps[i+1]) == Separate
    #     if separate_before:
    #         step_vessel_chain.pop(0)
    #     if separate_after:
    #         step_vessel_chain.pop(-1)
    links = []
    for item in step_vessel_chain:
        resolution_rule = item[1]

        assigned_vessel = None
        for forced_step, forced_keyword, forced_vessel in forced_vessels:
            if forced_step is step and forced_keyword == item[0]:
                assigned_vessel = forced_vessel
                if assigned_vessel in ['group_to', 'other']:
                    resolution_rule = assigned_vessel
                    assigned_vessel = None

                # Split vessel chain into two and put splitting step in at beginning of second vessel chain.
                elif assigned_vessel == 'split_with_next':
                    resolution_rule = 'next'
                    assigned_vessel = None

                # Split vessel chain into two and put splitting step at end of first vessel chain
                elif assigned_vessel == 'split_with_prev':
                    resolution_rule = 'prev'
                    assigned_vessel = None

        link = VesselChainLink(vessel_keyword=item[0],
                               resolution_rule=resolution_rule,
                               step=step,
                               assigned_vessel=assigned_vessel)
        links.append(link)
    return links

def get_vessel_chains(
    steps: List[Step],
    forced_vessels: List[Tuple[Step, str]]
) -> List[List[VesselChainLink]]:
    """Get vessel chains from list of steps. Each vessel in chain is represented
    as VesselChainLink object with vessel_keyword, resolution_rules, step and
    assigned_vessel attributes.

    Multiple vessel chains will only be included if a splitter is in forced_vessels

    Args:
        steps (List[Step]): List of steps to get vessel chain from.
        forced_vessels (List[Tuple[Step, str]]): List of steps with
            corresponding forced vessels.

    Returns:
        List[List[VesselChainLink]]:
            List of list of objects representing vessels in vessel chain.
    """
    vessel_chains, vessel_chain = [], []
    step_groups, step_group = [], []
    i = 0
    while i < len(steps):
        step = steps[i]
        should_continue = False
        for forced_vessel_step, _, forced_vessel in forced_vessels:
            if forced_vessel_step is step:
                if forced_vessel == 'split_with_next':
                    vessel_chains.append(vessel_chain)
                    step_groups.append(step_group)
                    vessel_chain = get_vessel_chain_links(step, forced_vessels)
                    step_group = [step]
                    should_continue = True

                elif forced_vessel == 'split_with_prev':
                    vessel_chain.extend(
                        get_vessel_chain_links(step, forced_vessels))
                    vessel_chains.append(vessel_chain)
                    vessel_chain = []
                    step_group.append(step)
                    step_groups.append(step_group)
                    step_group = []
                    should_continue = True

        if should_continue:
            i += 1
            continue

        if type(step) == Repeat:
            for child in step.children:
                vessel_chain.extend(
                    get_vessel_chain_links(child, forced_vessels))
        else:
            vessel_chain.extend(get_vessel_chain_links(step, forced_vessels))
        step_group.append(step)
        i += 1

    if vessel_chain:
        vessel_chains.append(vessel_chain)
    if step_group:
        step_groups.append(step_group)
    return vessel_chains, step_groups

def search_definite_temperature(vessel_chain, i, direction='forward'):
    while ((direction == 'forward' and i < len(vessel_chain))
           or (direction == 'back' and i >= 0)):
        upcoming_link = vessel_chain[i]
        if 'heatcool' in upcoming_link.resolution_rule:
            reqs = upcoming_link.step.requirements[upcoming_link.vessel_keyword]
            max_temp = max(reqs['temp'])
            min_temp = min(reqs['temp'])
            if min_temp < 18:
                return 'filter'

        elif ('separator' in upcoming_link.resolution_rule
              or 'rotavap' in upcoming_link.resolution_rule):
            return None

        elif 'filter' in upcoming_link.resolution_rule:
            return 'filter'
        if direction == 'forward':
            i += 1
        else:
            i -= 1
    return None

def resolve_definite_vessels(
        vessel_chain: List[VesselChainLink]) -> List[VesselChainLink]:
    """Set assigned_vessel on all links in chain with definite resolution rules,
    i.e. 'separator', 'filter', 'heatcool', or 'rotavap'.

    Args:
        vessel_chain (List[VesselChainLink]): Vessel chain to resolve definite
            vessels for.

    Returns:
        List[VesselChainLink]: Vessel chain with all links with definite
            resolution rules given an assigned_vessel.
    """
    for i, link in enumerate(vessel_chain):
        if type(link.resolution_rule) == str:
            resolution_rules = [link.resolution_rule]
        else:
            resolution_rules = link.resolution_rule
        for rule in resolution_rules:
            if link.assigned_vessel:
                break

            if rule in DEFINITE_VESSELS:
                link.assigned_vessel = rule

            elif rule.startswith('cartridge'):
                link.assigned_vessel = rule

            elif rule == 'heatcool':
                if ('prev' in resolution_rules
                    and i > 0
                    and vessel_chain[i - 1].assigned_vessel in [
                        'filter', 'reactor']
                        and type(vessel_chain[i - 1].step) == Add):
                    link.assigned_vessel = vessel_chain[i - 1].assigned_vessel

                else:
                    # If there is a filter step coming up and the temperatures
                    # are compatible, use filter. Otherwise use reactor.
                    link.assigned_vessel = 'reactor'
                    use_filter = False
                    for link2 in vessel_chain[i:]:
                        if link2.resolution_rule in ['separator', 'rotavap']:
                            break
                        elif link2.resolution_rule == 'filter':
                            use_filter = True
                            break
                        elif link2.resolution_rule == 'heatcool':
                            reqs = link2.step.requirements[link2.vessel_keyword]
                            max_temp = max(reqs['temp'])
                            if max_temp > MAX_FILTER_TEMP:
                                use_filter = False
                                break

                    if not use_filter:
                        for link2 in reversed(vessel_chain[:i]):
                            if link2.resolution_rule in ['separator', 'rotavap']:
                                break
                            elif link2.resolution_rule == 'filter':
                                use_filter = True
                                break
                            elif link2.resolution_rule == 'heatcool':
                                reqs = link2.step.requirements[link2.vessel_keyword]
                                max_temp = max(reqs['temp'])
                                if max_temp > MAX_FILTER_TEMP:
                                    use_filter = False
                                    break

                    if use_filter:
                        link.assigned_vessel = 'filter'

    return vessel_chain

def biggest_chain_length_unresolved_vessels(
        vessel_chain: List[VesselChainLink]) -> int:
    """Return length of longest sequence of consecutive links with
    assigned_vessel attribute == None.

    Args:
        vessel_chain (Link[VesselChainLink]): Vessel chain to find longest
            undefined sequence in.

    Returns:
        int: Length of longest sequence in vessel chain of links with no
            defined assigned_vessel.
    """
    biggest_chain_length = 0
    chain_length = 0
    for link in vessel_chain:
        if link.assigned_vessel not in DEFINITE_VESSELS:
            chain_length += 1
            if chain_length > biggest_chain_length:
                biggest_chain_length = chain_length
        else:
            chain_length = 0
    return biggest_chain_length

def resolve_vessel(
        vessel_chain: List[VesselChainLink], rule: str, i: int) -> bool:
    """Try and resolve undefined vessel.

    Args:
        vessel_chain (List[VesselChainLink]): Vessel chain.
        rule (str): Rule to use for resolution, 'next' or 'prev'.
        i (int): Index of link in chain to try and resolve.

    Returns:
        bool: True if resolution was successful, otherwise False.
    """
    resolved = False
    if rule == 'group_to':
        j = i
        while j < len(vessel_chain) and type(vessel_chain[j].step) in [Separate, Transfer]:
            j += 1
        if j < len(vessel_chain) and vessel_chain[j].assigned_vessel:
            vessel_chain[i].assigned_vessel = vessel_chain[j].assigned_vessel

    elif rule == 'prev':
        if (i - 1 >= 0
                and vessel_chain[i - 1].assigned_vessel in DEFINITE_VESSELS):
            resolved = True
            vessel_chain[i].assigned_vessel = vessel_chain[i
                                                           - 1].assigned_vessel

    elif rule == 'next':
        if (i + 1 < len(vessel_chain)
                and vessel_chain[i + 1].assigned_vessel in DEFINITE_VESSELS):
            resolved = True
            vessel_chain[i].assigned_vessel = vessel_chain[i
                                                           + 1].assigned_vessel

    return resolved

def try_resolve_vessels(
        vessel_chain: List[VesselChainLink]) -> List[VesselChainLink]:
    """Try and resolve all unassigned vessels in vessel chain.

    Args:
        vessel_chain (List[VesselChainLink]): Vessel chain.

    Returns:
        List[VesselChainLink]: Vessel chain with all possible assignments made.
    """
    for i in reversed(range(len(vessel_chain))):
        link = vessel_chain[i]
        if not link.assigned_vessel:
            if type(link.resolution_rule) == str:
                resolve_vessel(vessel_chain, link.resolution_rule, i)
            elif type(link.resolution_rule) == list:
                for rule in link.resolution_rule:
                    if resolve_vessel(vessel_chain, rule, i):
                        break
    return vessel_chain

def final_try_resolve_vessels(
        vessel_chain: List[VesselChainLink]) -> List[VesselChainLink]:
    """Try and resolve all unassigned vessels in vessel chain.

    Args:
        vessel_chain (List[VesselChainLink]): Vessel chain.

    Returns:
        List[VesselChainLink]: Vessel chain with all possible assignments made.
    """
    for i in reversed(range(len(vessel_chain))):
        link = vessel_chain[i]
        if type(link.step) in FINAL_TRY_STEP_VESSEL_CHAINS:
            if not link.assigned_vessel:
                rule = FINAL_TRY_STEP_VESSEL_CHAINS[type(
                    link.step)][link.vessel_keyword]
                if type(rule) == str:
                    resolve_vessel(vessel_chain, link.resolution_rule, i)
                elif type(rule) == list:
                    for subrule in rule:
                        if resolve_vessel(vessel_chain, subrule, i):
                            break
    return vessel_chain

def add_fake_vessels_at_beginning_end(
        vessel_chain: List[VesselChainLink]) -> List[VesselChainLink]:
    """Add definite filter vessels at beginning and end as a fallback, in case
    there are no definite vessels around beginning and end for vessel links to
    use for resolution.

    Args:
        vessel_chain (List[VesselChainLink]): Vessel chain to add fake vessels
            to.

    Returns:
        List[VesselChainLink]: Vessel chain witih fake filter vessels added at
            beginning and end.
    """
    fake_vessel = VesselChainLink(
        vessel_keyword='vessel',
        resolution_rule='reactor',
        step=None,
        assigned_vessel=None
    )
    fake_vessel.assigned_vessel = 'reactor'
    vessel_chain.insert(0, fake_vessel)
    vessel_chain.append(copy.deepcopy(fake_vessel))
    return vessel_chain

def resolve_circular_dependencies(
        vessel_chain: List[VesselChainLink]) -> List[VesselChainLink]:
    """Circular dependencies arise when one link in chain has 'next' as its
    resolution_rule and the next link has 'prev' as its resolution rule.
    As an imperfect resolution to this situation, go through vessel chain in
    reverse order, storing each encountered definite vessel as you go, and
    assign the last encountered definite vessel to any unassigned vessels.

    Args:
        vessel_chain (List[VesselChainLink]): Vessel chain to resolve circular
            dependencies for.

    Returns:
        List[VesselChainLink]: Vessel chain with all vessels assigned.
    """
    for i in reversed(range(len(vessel_chain))):
        link = vessel_chain[i]
        if link.assigned_vessel in DEFINITE_VESSELS:
            current_vessel = link.assigned_vessel
        elif not link.assigned_vessel and not link.resolution_rule in ['group_to', 'other']:
            link.assigned_vessel = current_vessel
    return vessel_chain

def apply_vessel_chain_to_steps(vessel_chain: List[VesselChainLink]) -> None:
    """Update all Step object properties dicts with assigned_vessels in vessel
    chain.

    Args:
        vessel_chain (List[VesselChainLink]): Vessel chain to use for applying
            assigned vessels to steps.
    """
    vessel_chain = vessel_chain[1:-1]
    for link in vessel_chain:
        link.step.properties[link.vessel_keyword] = link.assigned_vessel
        link.step.update()

def add_missing_transfer_steps(steps: List[Step], forced_vessels) -> List[Step]:
    """
    Add missing transfer steps after vessels have been assigned to procedure.

    Args:
        steps (List[Step]): List of steps to add missing transfer steps to.

    Returns:
        List[Step]: Step list with transfer steps added in during vessel changes.
    """
    insertions = []
    for i, step in enumerate(steps):
        if type(step) == Repeat:
            continue
        if len(STEP_VESSEL_CHAINS[type(step)]) == 1:
            j = i + 1
            if j < len(steps):
                next_step = steps[j]
                if type(next_step) == Repeat:
                    continue
            else:
                continue
            while (j < len(steps) - 1
                   and len(STEP_VESSEL_CHAINS[type(next_step)]) == 0):
                j += 1
                next_step = steps[j]

            if len(STEP_VESSEL_CHAINS[type(next_step)]) == 1:

                step_vessel = step.properties[
                    STEP_VESSEL_CHAINS[type(step)][0][0]]

                next_step_vessel = next_step.properties[
                    STEP_VESSEL_CHAINS[type(next_step)][0][0]]

                if step_vessel != next_step_vessel:
                    apply = True
                    for forced_step, forced_keyword, forced_vessel in forced_vessels:
                        if forced_step in [next_step, step] and forced_vessel == 'other':
                            apply = False
                    if apply:
                        insert_pos = j
                        insertions.append((
                            insert_pos,
                            Transfer(from_vessel=step_vessel,
                                     to_vessel=next_step_vessel,
                                     volume='all')))
    # Insert transfer steps at correct places.
    for pos, step in reversed(
            sorted(insertions, key=lambda insertion: insertion[0])):
        steps.insert(pos, step)
    return steps

def assign_vessels(
    steps: List[Step],
    forced_vessels: List[Tuple[Step, str]]
) -> Tuple[List[Step], List[Component]]:
    """Algorithm:

    1) Get vessel chains.

    2) Resolve definite vessels, i.e. Filter step needs 'filter', Separate step
       separation_vessel must be separate.

    3) Go through vessel chain and resolve undefined vessels based on their rules
       ('next', 'prev' or both in a specific order), using definite vessels
       immediately before or after them in the vessel chain. Repeat this for the
       length of the longest chain of undefined vessels at the start of step 2,
       as vessels become defined they can be used in the next iteration.

    4) Add default defined filter vessels at beginning and end of procedure to
       give undefined vessels at start and end something to fall back on.

    5) Repeat step 2

    6) Fill in any remaining undefined vessels (caused by circular dependencies
       of rules in the vessel chain) by going from end -> start of vessel chain
       and filling in last definite vessel for undefined vessels.

    7) Apply this vessel chain to the steps and add Transfer steps for added
       vessel changes.

    Args:
        steps (List[Step]): List of steps to assign vessels to.
        forced_vessels (List[Tuple[Step, str]]): List of steps with
            corresponding forced vessels.

    Returns:
        Tuple[List[Step], List[Component]]: List of Steps with vessels assigned
            and list of Components representing all vessels assign in steps.
    """
    # 0. Remove Transfer steps from steps (needs to be done if assign_vessels
    # has previously been called).
    for i in reversed(range(len(steps))):
        if type(steps[i]) == Transfer:
            pop = True
            for forced_step, _, _ in forced_vessels:
                if forced_step is steps[i]:
                    pop = False
            if pop:
                steps.pop(i)

    hardware = []

    vessel_chains, step_groups = get_vessel_chains(steps, forced_vessels)

    assigned_steps = []
    i = 0
    prev_finishing_vessel, current_starting_vessel = None, None

    for vessel_chain, step_group in zip(vessel_chains, step_groups):

        # Resolve vessel chain
        vessel_chain_steps = convert_vessel_chain(
            step_group, vessel_chain, forced_vessels)

        # Has to be 1 as fake reactor will be added at beginning.
        current_starting_vessel = vessel_chain[1].assigned_vessel

        if i > 0:
            vessel_chain_steps.insert(1, Transfer(
                from_vessel=prev_finishing_vessel,
                to_vessel=current_starting_vessel,
                volume='all'
            ))

        # Has to be -2 as fake reactor will be added at end.
        prev_finishing_vessel = vessel_chain[-2].assigned_vessel

        # Extend assigned steps and hardware
        assigned_steps.extend(vessel_chain_steps)
        i += 1
    return assigned_steps

def convert_vessel_chain(
    steps: List[Step],
    vessel_chain: List[VesselChainLink],
    forced_vessels: List[Tuple[Step, str]],
) -> Tuple[List[Step], List[Component]]:
    """Convert vessel chain to steps and components."""
    # 1. Resolve definite vessels
    vessel_chain = resolve_definite_vessels(vessel_chain)

    # 2. Multiple passes trying to resolve undefined vessels.
    for _ in range(biggest_chain_length_unresolved_vessels(vessel_chain)):
        vessel_chain = try_resolve_vessels(vessel_chain)

    # 3. Add fake vessels at beginning and end.
    vessel_chain = add_fake_vessels_at_beginning_end(vessel_chain)

    # 4. Multiple passes trying to resolve undefined vessels.
    for _ in range(biggest_chain_length_unresolved_vessels(vessel_chain)):
        vessel_chain = try_resolve_vessels(vessel_chain)

    # 5. Last resort to resolve circular dependencies, apply definite vessels
    #    through onto undefined vessels in reverse step order. Don't apply to
    # separation group 'group_to' vessels.
    vessel_chain = resolve_circular_dependencies(vessel_chain)

    # 6. Try and resolve any remaining 'group_to' separation group vessels
    for _ in range(biggest_chain_length_unresolved_vessels(vessel_chain)):
        vessel_chain = try_resolve_vessels(vessel_chain)

    for i in range(len(vessel_chain)):
        if vessel_chain[i].resolution_rule == 'other':
            j = i
            while j >= 0 and vessel_chain[j].resolution_rule == 'other':
                j -= 1
            if j >= 0 and vessel_chain[j].resolution_rule != 'other':
                if vessel_chain[j].assigned_vessel == 'reactor':
                    vessel_chain[i].assigned_vessel = 'filter'
                else:
                    vessel_chain[i].assigned_vessel = 'reactor'

    # 7. Apply all vessels to step properties.
    apply_vessel_chain_to_steps(vessel_chain)

    # 8. Add missing transfer steps for newly introduced vessel changes.
    steps = add_missing_transfer_steps(steps, forced_vessels)

    steps = postprocess_step_vessels(steps)

    return steps


def vessel_is_compatible(vessel, step):
    """Used by postprocess_step_vessels. Determine if step could use given vessel."""
    if type(step) in [Evaporate, Separate]:
        return False
    if vessel == 'reactor':
        if 'temp' in step.properties and step.temp != None:
            if 18 <= step.temp:
                return True
            else:
                return False
        if type(step) == Filter:
            return False
        return True

    elif vessel == 'filter':
        if 'temp' in step.properties and step.temp != None:
            if step.temp <= MAX_FILTER_TEMP:
                return True
            else:
                return False
        return True
    return False

def remove_pointless_transfers(steps):
    """Remove any pointless Transfer steps at start of procedure, but only at start.
    For example, starting in Reactor then going to Filter when everything could be
    performed in Filter.
    """
    for i in range(len(steps)):
        if type(steps[i]) == Transfer:
            j = i - 1
            should_change_vessel = True
            vessel = steps[i].to_vessel
            while j >= 0:
                if vessel_is_compatible(vessel, steps[j]):
                    j -= 1
                    continue
                else:
                    should_change_vessel = False
                    break
            if should_change_vessel:
                for step in steps[:i]:
                    if 'vessel' in step.properties:
                        step.vessel = vessel
                steps.pop(i)
                break
    for i in reversed(range(len(steps))):
        if type(steps[i]) == Transfer and steps[i].from_vessel == steps[i].to_vessel:
            steps.pop(i)
    return steps

def sort_out_no_solvent_separations(steps):
    """Correct issues with separations that just separate without adding solvent.
    """
    for i in range(len(steps)):
        step = steps[i]
        if type(step) == Separate:
            if not step.solvent:

                # If next step is Separate
                if i + 1 < len(steps) and type(steps[i + 1]) == Separate:

                    # If next step is extraction
                    if steps[i + 1].purpose == 'extract':
                        # Current step waste -> extraction
                        # Current step waste_phase_to_vessel = separator = next step from_vessel
                        steps[i + 1].from_vessel = 'separator'
                        steps[i].waste_phase_to_vessel = 'separator'

                    # If next step is wash
                    elif steps[i + 1].purpose == 'wash':
                        # Current step waste -> extraction
                        # Current step waste_phase_to_vessel = separator = next step from_vessel
                        steps[i + 1].from_vessel = steps[i].to_vessel
                        steps[i].waste_phase_to_vessel = None

                    # No point separating to vessel then from same vessel, just stay in separator
                    # If next step from_vessel == current step to_vessel != current step separation_vessel
                    if steps[i + 1].from_vessel == steps[i].to_vessel != steps[i].separation_vessel:
                        # Next step from_vessel -> separator
                        steps[i + 1].from_vessel = steps[i].separation_vessel
                        steps[i + 1].from_port = None
                        # Current step to_vessel -> separator
                        steps[i].to_vessel = steps[i].separation_vessel
                        steps[i].to_port = None

            # No point sending layer to to_vessel if it is just going to be
            # transferred back.
            # If next step is transfer and step after that is Separate
            elif (i + 1 < len(steps) and type(steps[i + 1]) == Transfer
                  and i + 2 < len(steps) and type(steps[i + 2]) == Separate):
                if steps[i].to_vessel == steps[i + 1].from_vessel:
                    # if steps[i+1].from_vessel != 'buffer_flask1':
                    steps[i].to_vessel = steps[i + 1].to_vessel
                    # steps[i].to_port = 'top'

                    # Add
                    if steps[i].to_vessel != 'buffer_flask1' and steps[i].purpose == 'wash':
                        j = i + 3
                        while j < len(steps) and type(steps[j]) == Separate:
                            j += 1
                        steps[i].to_vessel = steps[j - 1].to_vessel
                        steps[i].to_port == steps[j - 1].to_port
    return steps

def sort_pointless_separation_buffer_flasks(steps):
    """Sort problem where buffer flask is used instead of group to vessel
    in the case of two isolated consecutive extraction steps.
    """
    sep_is = [
        i for i in range(len(steps))
        if type(steps[i]) == Separate
    ]
    for i, step in enumerate(steps):
        if type(step) == Separate:
            # Two extractions together
            if (i + 1 in sep_is and not i - 2 in sep_is
                and not i - 1 in sep_is and not i + 2 in sep_is
                    and not i + 3 in sep_is):
                # Should just go to group_to, not to buffer flask.
                if step.purpose == 'extract' and steps[i + 1].purpose == 'extract':
                    if step.to_vessel == 'buffer_flask1':
                        step.to_vessel = steps[i + 1].to_vessel


def postprocess_step_vessels(steps):
    remove_pointless_transfers(steps)
    sort_out_no_solvent_separations(steps)
    sort_pointless_separation_buffer_flasks(steps)
    return steps
