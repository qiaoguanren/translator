from typing import Tuple, List, Union, Optional
from xdl.chemputerxdl.steps import (
    Step,
    Stir,
    StartStir,
    StopStir,
    Add,
    Separate,
    StartHeatChill,
    HeatChill,
    HeatChillToTemp,
    StopHeatChill,
    Filter,
    FilterThrough,
    WashSolid,
    Dry,
    Confirm,
    Evaporate,
    Dissolve,
    RunColumn,
    Recrystallize,
    Sonicate,
    Distill,
    Evacuate,
    Transfer,
)
from xdl.steps.special_steps import Repeat, Wait
from .utils import get_reagent_temp
from .constants import (
    DEFAULT_SLOW_ADDITION_DISPENSE_SPEED,
    DEFAULT_DROPWISE_DISPENSE_SPEED,
    DEFAULT_VISCOUS_ASPIRATION_SPEED,
    DEFAULT_COLD_REAGENT_TEMP,
    DEFAULT_ICECOLD_REAGENT_TEMP,
    DEFAULT_AUTO_EVAPORATION_TIME_LIMIT,
    REAGENT_NAME_COLD_WORDS,
    REAGENT_NAME_ICECOLD_WORDS,
    DEFAULT_SEPARATION_VOLUME,
    DEFAULT_ANTICLOGGING_FILTER_ASPIRATION_SPEED,
)
from ..constants import (
    DEFAULT_FAST_STIR_SPEED,
    DEFAULT_SLOW_STIR_SPEED,
)
from ..words import (
    Action,
    SolutionWord,
    ReagentWord,
    RepeatedVolumeWord,
    ReagentPlaceholderWord
)

#################
### SOLUTIONS ###
#################

def solution_word_to_xdl(
    solution_word: SolutionWord
) -> Tuple[List[Step], List[str]]:
    """Convert solution word to XDL, specifically list of Steps and list of
    reagent names.

    Args:
        solutionWord (SolutionWord): Action to convert to XDL, after sanitization.

    Returns:
        Tuple[List[Step], List[str]]: (steps, reagent_names) tuple.
    """
    reagents = [solution_word.solvent.name]
    reagents.extend([solute.name for solute in solution_word.solutes])
    steps = [Confirm(get_confirm_solutes_in_flask_msg(solution_word.solutes))]
    steps.append(Add(vessel=None,
                     reagent=solution_word.solvent.name,
                     volume=str(solution_word.volume)))
    return steps, reagents

def get_confirm_solutes_in_flask_msg(solutes):
    confirm_msg = 'Is '
    for solute in solutes:
        confirm_msg += f'{str(solute)}, '
    confirm_msg = confirm_msg[:-2] + ' in the correct vessel?'
    return confirm_msg


def check_subject_for_solution(
    action: Union[Action, SolutionWord]
) -> Tuple[List[Step], List[str]]:
    """Check action to see if it is SolutionWord and if so return solution
    steps and reagents as stub, otherwise return empty lists.
    Used by multiple action_to_xdl functions to make solution before adding
    other steps.

    Args:
        action (Union[Action, SolutionWord]): Object to check if it is a
            SolutionWord and respond accoridngly.

    Returns:
        Tuple[List[Step], List[str]]: (steps, reagents) tuple, blank if action
            is an Action, contains steps, reagents for making solution if action
            is a SolutionWord.
    """
    if type(action.subject) == SolutionWord:
        return solution_word_to_xdl(action.subject)
    else:
        return [], []


######################
### ADDITION STEPS ###
######################

def add_reaction_mixture_action_to_xdl(add_action):
    dispense_speed, time = None, None
    if add_action.time:
        time = str(add_action.time)
    elif add_action.dropwise:
        dispense_speed = DEFAULT_DROPWISE_DISPENSE_SPEED
    elif add_action.slow_addition:
        dispense_speed = DEFAULT_SLOW_ADDITION_DISPENSE_SPEED
    return [
        Transfer(
            from_vessel='other',
            to_vessel=None,
            volume=add_action.subject.volume,
            dispense_speed=dispense_speed,
            time=time,
        )
    ], []

def add_action_to_xdl(add_action: Action) -> Tuple[List[Step], List[str]]:
    """Convert add action to XDL, specifically list of Steps and list of
    reagent names.

    Args:
        add_action (Action): Action to convert to XDL, after sanitization.

    Returns:
        Tuple[List[Step], List[str]]: (steps, reagent_names) tuple.
    """
    # Transferring reaction mixture gradually back somewhere, see Org. Synth v90p0251 paragraph 2
    if type(add_action.subject) == ReagentPlaceholderWord and add_action.subject.volume:
        return add_reaction_mixture_action_to_xdl(add_action)

    if add_action.column:
        return purify_action_to_xdl(add_action)
    elif add_action.evaporate:
        return evaporate_action_to_xdl(add_action)
    elif add_action.filter:
        return filter_action_to_xdl(add_action)
    elif add_action.wash_solid:
        return washsolid_action_to_xdl(add_action)
    elif add_action.transfer_to_separator:
        reagents = []
        steps = [Transfer(from_vessel=None,
                          to_vessel='separator',
                          volume='all')]
        for reagent in add_action.reagents:
            new_steps, new_reagents = add_reagent_to_xdl(reagent)
            steps.extend(new_steps)
            reagents.extend(new_reagents)
        return steps, reagents

    steps, reagents = [], []
    stir = False
    stir_speed = 'default'
    if add_action.temp != None:
        steps.append(HeatChillToTemp(vessel=None, temp=str(add_action.temp)))
    liquid_additions = 0

    # Force round bottomed flask to be used with heterogeneous mixtures as there
    # is a problem using the filter with the solid staying in the top and liquid
    # reactant moving to the bottom.
    force_vessel = None
    if str(add_action.action).startswith('suspended'):
        force_vessel = 'reactor'

    # 'NaOH (5 g) was added in 10 portions (500 mg every 5 mins)'
    if add_action.mass_at_interval:
        reagent = add_action.reagents[0]
        n_portions = add_action.n_portions
        mass = add_action.mass_at_interval['mass']
        interval = add_action.mass_at_interval['interval']
        steps.append(Repeat(children=[
            Add(vessel=None, reagent=reagent.name, mass=mass),
            Wait(time=interval)
        ], repeats=n_portions))
        reagents.append(reagent.name)
        return steps, reagents

    # Normal addition
    for i, reagent in enumerate(add_action.reagents):
        if add_action.explicit_stirring:
            stir = True
            if add_action.fast_stirring:
                stir_speed = DEFAULT_FAST_STIR_SPEED
            elif add_action.slow_stirring:
                stir_speed = DEFAULT_SLOW_STIR_SPEED
        reagent_forced_vessel = force_vessel
        if reagent.name in add_action.forced_vessels:
            reagent_forced_vessel = add_action.forced_vessels[reagent.name]

        reagent_steps, reagent_reagents = add_reagent_to_xdl(
            reagent,
            slow_addition=add_action.slow_addition,
            dropwise=add_action.dropwise,
            time=add_action.time,
            stir=stir,
            stir_speed=stir_speed,
            force_vessel=reagent_forced_vessel,
            through=add_action.through,
            viscous=add_action.viscous,
        )
        if reagent.volume != None:
            liquid_additions += 1
        steps.extend(reagent_steps)
        reagents.extend(reagent_reagents)
    if add_action.temp != None:
        steps.append(StopHeatChill(vessel=None))
    return steps, reagents

def add_reagent_to_xdl(
    reagent: Union[ReagentWord, SolutionWord],
    slow_addition: Optional[bool] = False,
    dropwise: Optional[bool] = False,
    time: Optional[float] = None,
    stir: bool = True,
    stir_speed: float = 'default',
    force_vessel: str = None,
    through: str = None,
    viscous: bool = False,
) -> Tuple[List[Step], List[str]]:
    """Convert addition of reagent to XDL, specifically list of Steps and list
    of reagent names.

    Args:
        reagent (Union[ReagentWord, SolutionWord]): Reagent to add in XDL.
        slow_addition (bool): If True reagent will be added very slowly.
        time (float): Time over which reagent should be added.
        stir (bool): True if vessel should be stirred during addition, otherwise
            False.

    Returns:
        Tuple[List[Step], List[str]]: (steps, reagent_names) tuple.
    """
    steps, reagents = [], []
    reagents = [reagent.name]
    addition_temp = get_reagent_temp(reagent)
    if addition_temp != None:
        steps = [
            HeatChillToTemp(vessel=force_vessel, temp=addition_temp),
        ]

    if reagent.volume:
        if type(reagent.volume) == RepeatedVolumeWord:
            repeat = reagent.volume.multiplier
            volume = str(reagent.volume.volume)
            add_step = Add(
                reagent=reagent.name,
                vessel=force_vessel,
                volume=volume,
                stir=stir,
                stir_speed=stir_speed,
                through=through,
            )
            if repeat > 1:
                steps.append(Repeat(children=[add_step], repeats=repeat))
            else:
                steps.append(add_step)
        else:
            volume = str(reagent.volume)
            steps.append(
                Add(reagent=reagent.name,
                    vessel=force_vessel,
                    volume=volume,
                    stir=stir,
                    through=through,
                    stir_speed=stir_speed)
            )

    elif hasattr(reagent, 'mass') and reagent.mass:
        steps.append(
            Add(reagent=reagent.name,
                vessel=force_vessel,
                mass=str(reagent.mass),
                stir=stir,
                through=through,
                stir_speed=stir_speed))

    else:
        steps.append(
            Add(reagent=reagent.name,
                vessel=force_vessel,
                volume=0,
                stir=stir,
                through=through,
                stir_speed=stir_speed))
    if time:
        steps[-1].time = str(time)
        steps[-1].update()

    elif dropwise:
        steps[-1].dispense_speed = DEFAULT_DROPWISE_DISPENSE_SPEED
        steps[-1].update()

    elif slow_addition:
        steps[-1].dispense_speed = DEFAULT_SLOW_ADDITION_DISPENSE_SPEED
        steps[-1].update()

    if viscous:
        steps[-1].viscous = True
        steps[-1].update()

    if type(steps[0]) == HeatChillToTemp:
        steps.append(StopHeatChill(vessel=None))

    return steps, reagents

def dissolve_action_to_xdl(
    dissolve_action: Action
) -> Tuple[List[Step], List[str]]:
    """Convert dissolve action to XDL, specifically list of Steps and list of
    reagent names.

    Args:
        dissolve_action (Action): Action to convert to XDL, after sanitization.

    Returns:
        Tuple[List[Step], List[str]]: (steps, reagent_names) tuple.
    """
    solvents = dissolve_action.solvents
    solutes = dissolve_action.solutes
    volumes = dissolve_action.volumes
    steps, reagents = [], []
    vessel = None
    if solutes:
        vessel = 'other'
    # Add solutes
    if solutes:
        for solute in solutes:
            reagents.append(solute.name)
            # Solid solute
            if not solute.volume:
                steps.append(Confirm(get_confirm_solutes_in_flask_msg(
                    [solute])))

            # Liquid solute
            else:
                steps.append(
                    Add(reagent=solute.name,
                        volume=str(solute.volume),
                        vessel=vessel))

    volume_solvents = [i for i, solvent in enumerate(
        solvents) if volumes[i] != 0]
    if volume_solvents:
        solvents = [solvents[i] for i in volume_solvents]
        volumes = [volumes[i] for i in volume_solvents]
    # Add solvents
    if solvents:
        # Add all solvents before performing Dissolve on last solvent
        if len(solvents) > 1:
            for solvent, volume in zip(
                    solvents[:-1], volumes[:-1]):

                reagents.append(solvent.name)
                steps.append(
                    Add(reagent=solvent.name, volume=volume, vessel=vessel))

        # Dissolve last (or only) solvent
        reagents.append(solvents[-1].name)
        steps.append(Dissolve(
            solvent=solvents[-1].name,
            vessel=vessel,
            temp=dissolve_action.temp,
            volume=volumes[-1]))
    return steps, reagents

def neutralize_action_to_xdl(
    neutralize_action: Action
) -> Tuple[List[Step], List[str]]:
    """Convert neutralize action to XDL, specifically list of Steps and list of
    reagent names.

    Args:
        neutralize_action (Action): Action to convert to XDL, after sanitization.

    Returns:
        Tuple[List[Step], List[str]]: (steps, reagent_names) tuple.
    """
    steps, reagents = [], []
    if neutralize_action.temp != None:
        steps = [HeatChillToTemp(
            vessel=None, temp=str(neutralize_action.temp))]
    for reagent in neutralize_action.reagents:
        add_steps, add_reagents = add_reagent_to_xdl(reagent)
        for step in add_steps:
            if step.name == 'Add':
                # Hack to tell blank_filling that step is neutralization
                step.volume = 111111
                step.dispense_speed = 10
                steps.extend(add_steps)
        reagents.extend(add_reagents)
    if neutralize_action.stir:
        for step in steps:
            if type(step) == Add:
                step.stir = True
    if neutralize_action.temp != None:
        # In case solution has warmed during addition, make sure vessel is at
        # correct temp before turning off heater/chiller.
        steps.append(HeatChillToTemp(
            vessel=None, temp=str(neutralize_action.temp)))
        steps.append(StopHeatChill(vessel=None))
    return steps, reagents

def mix_action_to_xdl(mix_action: Action) -> Tuple[List[Step], List[str]]:
    """Convert mix action to XDL, specifically list of Steps and list of
    reagent names.

    Args:
        mix_action (Action): Action to convert to XDL, after sanitization.

    Returns:
        Tuple[List[Step], List[str]]: (steps, reagent_names) tuple.
    """
    return add_action_to_xdl(mix_action)


######################
### REACTION STEPS ###
######################

def stir_action_to_xdl(stir_action: Action) -> Tuple[List[Step], List[str]]:
    """Convert stir action to XDL, specifically list of Steps and list of
    reagent names.

    Args:
        stir_action (Action): Action to convert to XDL, after sanitization.

    Returns:
        Tuple[List[Step], List[str]]: (steps, reagent_names) tuple.
    """
    steps, reagents = [], []
    stir_speed = 'default'
    stir_reagent_addition = False
    if stir_action.stir_speed != 'default':
        stir_speed = stir_action.stir_speed
    elif stir_action.speed == 'fast':
        stir_speed = DEFAULT_FAST_STIR_SPEED
    elif stir_action.speed == 'slow':
        stir_speed = DEFAULT_SLOW_STIR_SPEED
    for reagent in stir_action.reagents:
        # If reagent name starts with 'cold', e.g. 'cold water', the temperature
        # used to chill the reagent should be applied to the stirring as well.
        if not stir_action.temp:
            reagent_temp = get_reagent_temp(reagent)
            if reagent_temp != None:
                stir_action.temp = reagent_temp
        stir_reagent_addition = True
        add_steps, add_reagents = add_reagent_to_xdl(reagent)
        steps.extend(add_steps)
        reagents.extend(add_reagents)

    if stir_action.temp != None:
        if stir_reagent_addition:
            steps.insert(
                0, HeatChillToTemp(vessel=None,
                                   temp=str(stir_action.temp),
                                   stir="True",
                                   stir_speed=stir_speed))
            steps.extend([
                Stir(vessel=None,
                     time=str(stir_action.time),
                     stir_speed=stir_speed),
                StopHeatChill(vessel=None),
            ])
        # Solution was stirred with slow warming to...
        elif stir_action.slow_temp:
            steps.extend([
                StartHeatChill(
                    vessel=None,
                    temp=str(stir_action.temp),
                ),
                Stir(
                    vessel=None,
                    time=str(stir_action.time),
                    stir_speed=stir_speed
                )
            ])
        else:
            steps.append(HeatChill(
                vessel=None,
                time=str(stir_action.time),
                temp=str(stir_action.temp),
                stir="True",
                stir_speed=stir_speed))
    else:
        steps.append(Stir(
            vessel=None,
            time=str(stir_action.time),
            stir_speed=stir_speed))
    return steps, reagents

def reflux_action_to_xdl(reflux_action: Action) -> Tuple[List[Step], List[str]]:
    """Convert reflux action to XDL, specifically list of Steps and list of
    reagent names.

    Args:
        reflux_action (Action): Action to convert to XDL, after sanitization.

    Returns:
        Tuple[List[Step], List[str]]: (steps, reagent_names) tuple.
    """
    steps, reagents = check_subject_for_solution(reflux_action)
    steps.extend([
        HeatChill(
            vessel=None,
            temp=str(reflux_action.temp),
            time=str(reflux_action.time))
    ])
    return steps, reagents

def wait_action_to_xdl(wait_action: Action) -> Tuple[List[Step], List[str]]:
    """Convert wait action to XDL, specifically list of Steps and list of
    reagent names.

    Args:
        wait_action (Action): Action to convert to XDL, after sanitization.

    Returns:
        Tuple[List[Step], List[str]]: (steps, reagent_names) tuple.
    """
    steps = []
    if wait_action.temp not in [None, 25]:
        return heatchill_action_to_xdl(wait_action)
    elif wait_action.time:
        if wait_action.stir == True:
            steps = [Stir(time=str(wait_action.time),
                          vessel=None,
                          stir_speed=wait_action.stir_speed)]
        else:
            steps = [Wait(time=str(wait_action.time))]
    return steps, []

def heatchill_action_to_xdl(
        heatchill_action: Action) -> Tuple[List[Step], List[str]]:
    """Convert heatchill action to XDL, specifically list of Steps and list of
    reagent names.

    Args:
        heat_action (Action): Action to convert to XDL, after sanitization.

    Returns:
        Tuple[List[Step], List[str]]: (steps, reagent_names) tuple.
    """
    steps = []
    if not heatchill_action.active:
        if heatchill_action.temp != None:
            temp = heatchill_action.temp
            if heatchill_action.temp < 18 or heatchill_action.temp > 25:
                continue_heatchill = True
            else:
                continue_heatchill = False
        else:
            temp = 25
            continue_heatchill = False

        # If heating, should wait for 18, as there is no guarantee what upper
        # temperature can be reached in a given room.
        # Likewise for cooling, just go to 25 as you cannot guarantee to go any
        # lower.
        if 18 <= temp <= 25:
            if heatchill_action.purpose == 'heat':
                temp = 18
            else:
                temp = 25

        # Explicit time given, just wait
        if heatchill_action.time:
            steps.extend([
                StopHeatChill(vessel=None),
                Wait(time=str(heatchill_action.time))
            ])

        # No explicit time given, wait for temp.
        else:
            steps.append(HeatChillToTemp(
                vessel=None,
                active=False,
                continue_heatchill=continue_heatchill,
                temp=temp,
                stir=heatchill_action.stir,
                stir_speed=heatchill_action.stir_speed))

    else:
        if heatchill_action.time:
            steps.append(
                HeatChill(
                    vessel=None,
                    temp=heatchill_action.temp,
                    time=str(heatchill_action.time),
                    stir=heatchill_action.stir,
                    stir_speed=heatchill_action.stir_speed))
        else:
            steps.append(HeatChillToTemp(
                vessel=None,
                temp=heatchill_action.temp,
                continue_heatchill=True,
                stir=heatchill_action.stir,
                stir_speed=heatchill_action.stir_speed))
    return steps, []


####################
### FILTER STEPS ###
####################

def isolate_action_to_xdl(
        isolate_action: Action) -> Tuple[List[Step], List[str]]:
    """Convert isolate action to XDL, specifically list of Steps and list of
    reagent names.

    Args:
        filter_action (Action): Action to convert to XDL, after sanitization.

    Returns:
        Tuple[List[Step], List[str]]: (steps, reagent_names) tuple.
    """
    if isolate_action.filter:
        return filter_action_to_xdl(isolate_action)
    return [], []

def remove_action_to_xdl(
        remove_action: Action) -> Tuple[List[Step], List[str]]:
    """Convert remove action to XDL, specifically list of Steps and list of
    reagent names.

    Args:
        filter_action (Action): Action to convert to XDL, after sanitization.

    Returns:
        Tuple[List[Step], List[str]]: (steps, reagent_names) tuple.
    """
    if remove_action.filter:
        return filter_action_to_xdl(remove_action)
    elif remove_action.evaporate:
        return evaporate_action_to_xdl(remove_action)
    elif remove_action.discontinue_heatchill:
        return [StopHeatChill(vessel=None)], []
    elif remove_action.dry:
        return dry_action_to_xdl(remove_action)
    return [], []

def filter_action_to_xdl(filter_action: Action) -> Tuple[List[Step], List[str]]:
    """Convert filter action to XDL, specifically list of Steps and list of
    reagent names.

    Args:
        filter_action (Action): Action to convert to XDL, after sanitization.

    Returns:
        Tuple[List[Step], List[str]]: (steps, reagent_names) tuple.
    """
    # Filter through something (e.g. celite)
    steps, reagents = [], []
    if filter_action.through:
        eluting_solvent, eluting_volume, eluting_repeats = None, None, 1
        if filter_action.eluting_solvent:
            eluting_solvent = filter_action.eluting_solvent.name

            if type(filter_action.eluting_solvent.volume) == RepeatedVolumeWord:
                eluting_volume = str(
                    filter_action.eluting_solvent.volume.volume)
                eluting_repeats = filter_action.eluting_solvent.volume.multiplier

            else:
                eluting_volume = str(filter_action.eluting_solvent.volume)
                eluting_repeats = filter_action.eluting_solvent.repeats

            reagents.append(eluting_solvent)

        if filter_action.through:
            steps = [FilterThrough(
                from_vessel=None,
                to_vessel=None,
                through=filter_action.through,
                eluting_solvent=eluting_solvent,
                eluting_volume=eluting_volume,
                eluting_repeats=eluting_repeats)]

    # Plain filter step.
    else:
        steps = [Filter(filter_vessel=None)]
        if filter_action.eluting_solvent:
            steps.append(
                WashSolid(
                    vessel=None,
                    solvent=filter_action.eluting_solvent.name,
                    volume=str(filter_action.eluting_volume),
                    repeat=filter_action.eluting_repeats
            ))
    return steps, reagents

def washsolid_action_to_xdl(
        washsolid_action: Action) -> Tuple[List[Step], List[str]]:
    """Convert wash filter cake action to XDL, specifically list of Steps and
    list of reagent names.

    Args:
        washsolid_action (Action): Action to convert to XDL, after
            sanitization.

    Returns:
        Tuple[List[Step], List[str]]: (steps, reagent_names) tuple.
    """
    steps, reagents = [], []

    for solvent in washsolid_action.solvents:
        reagents.append(solvent.name)
        volume = solvent.volume
        repeats = washsolid_action.repeats

        if type(solvent.volume) == RepeatedVolumeWord:
            repeats = solvent.volume.multiplier
            volume = solvent.volume.volume

        if not volume:
            volume = 'default'

        steps.append(WashSolid(
            vessel=None,
            solvent=solvent.name,
            volume=str(volume),
            repeat=repeats,
            temp=washsolid_action.temp,
            anticlogging=washsolid_action.anticlogging))
    return steps, reagents

def dry_action_to_xdl(dry_action: Action) -> Tuple[List[Step], List[str]]:
    """Convert dry action to XDL, specifically list of Steps and
    list of reagent names.

    Args:
        dry_action (Action): Action to convert to XDL, after sanitization.

    Returns:
        Tuple[List[Step], List[str]]: (steps, reagent_names) tuple.
    """
    steps = []
    if dry_action.filter_through:
        for reagent in dry_action.filter_through:
            steps.append(
                FilterThrough(from_vessel=None,
                              to_vessel=None,
                              through=reagent.name))
    else:
        steps.append(Dry(vessel=None,
                         temp=dry_action.temp,
                         time=dry_action.time,
                         vacuum_pressure=dry_action.pressure))
    return steps, []

def press_action_to_xdl(press_action: Action) -> Tuple[List[Step], List[str]]:
    """Convert press action to XDL, specifically list of Steps and
    list of reagent names. At the moment press action just becomes Dry step.

    Args:
        press_action (Action): Action to convert to XDL, after sanitization.

    Returns:
        Tuple[List[Step], List[str]]: (steps, reagent_names) tuple.
    """
    return dry_action_to_xdl(press_action)


########################
### SEPARATION STEPS ###
########################

def separate_action_to_xdl(separate_action, purpose):
    """Convert extract/wash action to XDL, specifically list of Steps and
    list of reagent names.

    Args:
        separate_action (Action): Extract/wash Action to convert to XDL, after
            sanitization.
        purpose (str): 'extract' or 'wash'

    Returns:
        Tuple[List[Step], List[str]]: (steps, reagent_names) tuple.
    """
    steps, reagents = [], []
    if separate_action.combined:
        from_vessel = 'buffer_flask1'
        if purpose == 'extract':
            from_vessel = 'buffer_flask1'
        steps.append(Transfer(from_vessel=from_vessel,
                              to_vessel='separator', volume='all'))
    if separate_action.separations:
        for separation in separate_action.separations:
            solvent_volume = separation['solvent_volume']
            if not solvent_volume:
                solvent_volume = DEFAULT_SEPARATION_VOLUME
            repeats = separation['repeats']
            if separate_action.repeats > separation['repeats']:
                repeats = separate_action.repeats

            steps.append(
                Separate(
                    purpose=purpose,
                    from_vessel=separation['from_vessel'],
                    to_vessel=separation['to_vessel'],
                    waste_phase_to_vessel=separation['waste_phase_to_vessel'],
                    separation_vessel=None,
                    solvent=separation['solvent_name'],
                    solvent_volume=solvent_volume,
                    product_bottom=separate_action.product_bottom,
                    n_separations=repeats,
                ))
            reagents.append(separation['solvent_name'])
    elif str(separate_action.action) in [
            'separated', 'retained', 'separated and retained', 'partitioned']:
        steps.append(
            Separate(
                purpose='extract',
                from_vessel=None,
                to_vessel='buffer_flask1',
                separation_vessel=None,
                waste_phase_to_vessel=None,
                solvent='',
                solvent_volume=None,
                product_bottom=None,
                n_separations=1,
            )
        )

    return steps, reagents

def extract_action_to_xdl(
    extract_action: Action
) -> Tuple[List[Step], List[str]]:
    """Convert extract action to XDL, specifically list of Steps and
    list of reagent names.

    Args:
        extract_action (Action): Action to convert to XDL, after sanitization.

    Returns:
        Tuple[List[Step], List[str]]: (steps, reagent_names) tuple.
    """
    return separate_action_to_xdl(extract_action, 'extract')

def wash_action_to_xdl(wash_action: Action) -> Tuple[List[Step], List[str]]:
    """Convert wash action to XDL, specifically list of Steps and
    list of reagent names.

    Args:
        wash_action (Action): Action to convert to XDL, after sanitization.

    Returns:
        Tuple[List[Step], List[str]]: (steps, reagent_names) tuple.
    """
    if wash_action.addition_funnel:
        return add_action_to_xdl(wash_action)
    elif wash_action.flask_wash:
        return add_action_to_xdl(wash_action)
    return separate_action_to_xdl(wash_action, 'wash')


###################
### OTHER STEPS ###
###################

def evacuate_action_to_xdl(
    evacuate_action: Action
) -> Tuple[List[Step], List[str]]:
    """Convert evacuate action to XDL, specifically list of Steps and list of
    reagent names.

    Args:
        evaporate_action (Action): Action to convert to XDL, after sanitization.

    Returns:
        Tuple[List[Step], List[str]]: (steps, reagent_names) tuple.
    """
    steps, reagents = [], []
    steps.append(Evacuate(vessel=None))
    return steps, reagents

def evaporate_action_to_xdl(
    evaporate_action: Action
) -> Tuple[List[Step], List[str]]:
    """Convert evaporate action to XDL, specifically list of Steps and list of
    reagent names.

    Args:
        evaporate_action (Action): Action to convert to XDL, after sanitization.

    Returns:
        Tuple[List[Step], List[str]]: (steps, reagent_names) tuple.
    """
    steps, reagents = [], []
    temp, pressure, time = None, None, DEFAULT_AUTO_EVAPORATION_TIME_LIMIT
    if evaporate_action.temp:
        temp = evaporate_action.temp
    if evaporate_action.pressure:
        pressure = evaporate_action.pressure
    if evaporate_action.time:
        time = evaporate_action.time
    steps.append(
        Evaporate(
            rotavap_name=None,
            mode='auto',
            temp=temp,
            pressure=pressure,
            time=time))
    return steps, reagents

def dilute_action_to_xdl(dilute_action: Action) -> Tuple[List[Step], List[str]]:
    """Convert dilute action to XDL, specifically list of Steps and list of
    reagent names.

    Args:
        dilute_action (Action): Action to convert to XDL, after sanitization.

    Returns:
        Tuple[List[Step], List[str]]: (steps, reagent_names) tuple.
    """
    return add_action_to_xdl(dilute_action)

def purify_action_to_xdl(purify_action: Action) -> Tuple[List[Step], List[str]]:
    """Convert purify action to XDL, specifically list of Steps and
    list of reagent names.

    Args:
        purify_action (Action): Action to convert to XDL, after sanitization.

    Returns:
        Tuple[List[Step], List[str]]: (steps, reagent_names) tuple.
    """
    reagents, steps = [], []
    if purify_action.column:
        steps = [RunColumn(from_vessel=None, to_vessel=None, column='column')]

    elif purify_action.recrystallize:
        steps = [Recrystallize(vessel=None)]

    elif purify_action.filtration:
        return filter_action_to_xdl(purify_action)
    return steps, []

def discontinue_action_to_xdl(
        discontinue_action: Action) -> Tuple[List[Step], List[str]]:
    steps = []
    for action in discontinue_action.stop_actions:
        if action == 'heatchill':
            steps.append(StopHeatChill(vessel=None))
        elif action == 'stir':
            steps.append(StopStir(vessel=None))
    return steps, []

def continue_action_to_xdl(
        continue_action: Action) -> Tuple[List[Step], List[str]]:
    if continue_action.continue_action == 'stir':
        return stir_action_to_xdl(continue_action)

    elif continue_action.continue_action == 'heatchill':
        return heatchill_action_to_xdl(continue_action)

    else:
        return [], []

def combine_action_to_xdl(combine_action: Action):
    steps, reagents = [], []
    if combine_action.phases:
        steps.append(Transfer(
            from_vessel='buffer_flask1', to_vessel='separator', volume='all'))
    return steps, reagents

def place_action_to_xdl(place_action: Action) -> Tuple[List[Step], List[str]]:
    if place_action.heatchill:
        return heatchill_action_to_xdl(place_action)

    elif place_action.addition:
        return add_action_to_xdl(place_action)

    else:
        return [], []

def afford_action_to_xdl(afford_action):
    if afford_action.purify:
        return purify_action_to_xdl(afford_action)
    elif afford_action.column:
        return [
            RunColumn(from_vessel=None, to_vessel=None, column=None),
        ], []
    return [], []

def collect_action_to_xdl(collect_action: Action) -> Tuple[List[Step], List[str]]:
    if collect_action.filtration:
        return filter_action_to_xdl(collect_action)

    return [], []

def subjected_action_to_xdl(
        subjected_action: Action) -> Tuple[List[Step], List[str]]:
    if subjected_action.distill:
        return distill_action_to_xdl(subjected_action)
    elif subjected_action.column:
        return purify_action_to_xdl(subjected_action)
    return [], []

def achieve_action_to_xdl(
        achieve_action: Action) -> Tuple[List[Step], List[str]]:
    if achieve_action.purify:
        return purify_action_to_xdl(achieve_action)
    return [], []

def provide_action_to_xdl(
        provide_action: Action) -> Tuple[List[Step], List[str]]:
    if provide_action.column:
        return [RunColumn(from_vessel=None, to_vessel=None, column=None)], []
    return [], []

def recrystallize_action_to_xdl(
        recrystallize_action: Action) -> Tuple[List[Step], List[str]]:
    return [Recrystallize(vessel=None)], []

def sonicate_action_to_xdl(
        sonicate_action: Action) -> Tuple[List[Step], List[str]]:
    return [Sonicate()], []

def distill_action_to_xdl(
        distill_action: Action) -> Tuple[List[Step], List[str]]:
    return [Distill()], []
