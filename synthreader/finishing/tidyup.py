from typing import List
import re

#from chemdata.synonyms import SYNONYM_CAS_DICT
from xdl import XDL
from xdl.steps.special_steps import Repeat
from xdl.steps import Step
from chemputerxdl.steps import (
    StopStir,
    StartStir,
    StopHeatChill,
    HeatChillToTemp,
    HeatChill,
    Filter,
    Stir,
    Add,
    Separate,
    Transfer,
    FilterThrough,
)
from xdl.steps.special_steps import Wait

SYNONYM_CAS_DICT=dict()
SYNONYM_CAS_DICT['Acetic acid']=64-19-7

def tidyup(xdl_obj: XDL) -> XDL:
    """Tidy up any little bits in step list that don't make sense, e.g.
    duplicate StopStir steps.
    """
    xdl_obj.steps = remove_duplicate_stop_steps(xdl_obj.steps)
    xdl_obj.steps = remove_pointless_heatchill_steps(xdl_obj.steps)
    xdl_obj = merge_duplicate_reagents(xdl_obj)
    xdl_obj.steps = correct_separation_then_filter_sequences(xdl_obj.steps)
    return xdl_obj

def correct_separation_then_filter_sequences(steps):
    i = 0
    while i < len(steps):
        step = steps[i]
        if type(step) == Separate:
            original_to_vessel = step.to_vessel
            if i + 1 < len(steps):
                if type(steps[i + 1]) == FilterThrough:
                    step.through = steps[i + 1].through
                    if i + 3 < len(steps) and type(steps[i + 2]) == Filter and type(steps[i + 3]) == Transfer:
                        step.to_vessel = steps[i + 3].to_vessel
                        step.to_port = steps[i + 3].to_port
                        del steps[i + 1:i + 4]

                    elif i + 2 < len(steps) and type(steps[i + 2]) == Filter:
                        step.to_vessel = steps[i + 2].filter_vessel
                        del steps[i + 1:i + 3]

                    else:
                        step.to_vessel = steps[i + 1].to_vessel
                        del steps[i + 1:i + 2]

                    # If combined phases need to be filtered through because some
                    # has already been transferred to to_vessel, use explicit
                    # FilterThrough step. Otherwise just using Separate through
                    # is fine.
                    j = i - 1
                    combined = False
                    while j >= 0 and type(steps[j]) == Separate:
                        if steps[j].to_vessel == original_to_vessel:
                            steps[j].through = step.through
                        j -= 1

                    # if combined:
                    #     steps.insert(i+1, FilterThrough(
                    #         from_vessel=step.to_vessel,
                    #         to_vessel=step.to_vessel,
                    #         through=step.through
                    #     ))
                    #     step.through = None
        i += 1
    return steps


def remove_duplicate_stop_steps(steps: List[Step]) -> List[Step]:
    """Remove any StopStir or StopHeatChill steps that come after
    another identical step without any stirring/heating in between.
    e.g. HeatChillToTemp(stir=True), StopHeatChill, StopStir, StopHeatChill, one
    of the StopHeatChills is pointless.

    Args:
        steps (List[Step]): Steps to remove pointless stop steps from.

    Returns:
        List[Step]: Steps with pointless stop steps removed.
    """
    stopped_stirring = []
    stopped_heatchill = []
    for i in reversed(range(len(steps))):
        step = steps[i]
        # Stir
        if type(step) == StopStir:
            # If StopStir and StopStir already encountered for that vessel
            # remove it from steps.
            if step.vessel in stopped_stirring:
                steps.pop(i)
            # If this is first StopStir encountered for this vessel add it to
            # list.
            else:
                stopped_stirring.append(step.vessel)
        # If StartStir is encountered in any form, remove vessel from list as
        # StopStirs after this will relate to another StartStir.
        elif type(step) == StartStir and step.vessel in stopped_stirring:
            stopped_stirring.remove(step.vessel)
        elif ('vessel' in step.properties
              and step.vessel in stopped_stirring
              and 'stir' in step.properties
              and step.stir):
            stopped_stirring.remove(step.vessel)

        # HeatChill (same process as stir, different variables)
        if type(step) == StopHeatChill:
            if step.vessel in stopped_heatchill:
                steps.pop(i)
            else:
                stopped_heatchill.append(step.vessel)
        elif type(step) in [HeatChillToTemp, HeatChill] and step.vessel in stopped_stirring:
            stopped_heatchill.remove(step.vessel)
        elif ('vessel' in step.properties
              and step.vessel in stopped_heatchill
              and 'temp' in step.properties
              and step.temp != None):
            stopped_heatchill.remove(step.vessel)
    return steps

def remove_pointless_heatchill_steps(steps: List[Step]) -> List[Step]:
    """Remove pointless heatchill steps where the vessel is already at that
    temperature, or heating has already been stopped.

    Args:
        steps (List[Step]): List of steps to remove pointless heatchill
            steps from.

    Returns:
        List[Step]: Steps with pointless heatchill steps removed.
    """
    # Remove StopHeatChill steps if next step is HeatChill / HeatChillToTemp on
    # same vessel.
    remove = []
    for i in range(len(steps)):
        if type(steps[i]) == StopHeatChill:
            if (i + 1 < len(steps)
                and type(steps[i + 1]) in [HeatChill, HeatChillToTemp]
                    and steps[i + 1].vessel == steps[i].vessel):
                remove.append(i)

            # StopHeatChill, Wait, HeatChill sequence where wait is less than
            # 10 minutes, there is no point stopping heating/chilling.
            elif (i + 2 < len(steps)
                  and type(steps[i + 2]) in [HeatChill, HeatChillToTemp]
                  and steps[i + 2].vessel == steps[i].vessel):

                # Don't bother to stop heating if just a wait step in between
                if (type(steps[i + 1]) == Wait
                        and steps[i + 1].time < 60 * 10):
                    remove.append(i)

                # Don't bother to stop heating if just an add step in between
                elif (type(steps[i + 1]) == Add
                      and steps[i + 1].vessel == steps[i + 2].vessel):
                    remove.append(i)

    for i in reversed(remove):
        steps.pop(i)

    # Remove HeatChillToTemp steps if vessel is already at that temp.
    # Convert HeatChill steps to Stir steps if vessel is already at that temp.
    active_temps = {}
    residual_temps = {}
    remove, downgrade_to_stir = [], []

    def set_temps_heatchill_to_temp(heatchill_to_temp_step):
        if heatchill_to_temp_step.continue_heatchill:
            active_temps[heatchill_to_temp_step.vessel] = heatchill_to_temp_step.temp
        else:
            residual_temps[heatchill_to_temp_step.vessel] = heatchill_to_temp_step.temp

    for i in range(len(steps)):
        if type(steps[i]) == HeatChillToTemp:
            # Vessel is already heatchilled to temp of this step
            if steps[i].vessel in active_temps and active_temps[steps[i].vessel] == steps[i].temp:
                remove.append(i)

            # Vessel is already heatchilled to a different temp
            else:
                set_temps_heatchill_to_temp(steps[i])

        elif type(steps[i]) == HeatChill:
            # Vessel is already heatchilled to temp of this step
            if steps[i].vessel in active_temps:
                if active_temps[steps[i].vessel] == steps[i].temp:
                    downgrade_to_stir.append(i)
                else:
                    del active_temps[steps[i].vessel]
            # Vessel has not been heatchilled
            if not steps[i].vessel in residual_temps:
                residual_temps[steps[i].vessel] = steps[i].temp

            # Vessel has been heatchilled to different temperature
            else:
                residual_temps[steps[i].vessel] = steps[i].temp

        elif type(steps[i]) == StopHeatChill:
            # Vessel has not been heatchilled
            if not steps[i].vessel in active_temps:
                active_temps[steps[i].vessel] = None
                remove.append(i)

            # Vessel heatchill has stopped
            elif active_temps[steps[i].vessel] == None:
                remove.append(i)

            elif (i > 0
                  and type(steps[i - 1]) == HeatChill
                  and not i - 1 in downgrade_to_stir):
                active_temps[steps[i].vessel] = None
                remove.append(i)

            # Vessel is already heatchilled
            else:
                active_temps[steps[i].vessel] = None

    # Downgrade HeatChill steps to Stir steps when vessel is already at the
    # HeatChill step temp
    for i in downgrade_to_stir:
        steps[i] = Stir(vessel=steps[i].vessel,
                        time=steps[i].time,
                        stir_speed=steps[i].stir_speed)

    # Remove pointless steps
    for i in reversed(remove):
        steps.pop(i)

    return steps

def merge_duplicate_reagents(xdl_obj: XDL) -> XDL:
    """If there is 'dry acetonitrile' and 'acetonitrile' in the procedure, just
    use 'dry acetonitrile for everything.

    Args:
        xdl_obj (XDL): XDL object to merge any duplicate reagents

    Returns:
        XDL: xdl_obj with duplicate reagents merged.
    """
    dry_reagents = [reagent.id
                    for reagent in xdl_obj.reagents
                    if reagent.id.startswith(('dry ', 'anhydrous '))]
    changed_reagents = {re.sub(r'(?:dry |anhydrous )', '', reagent): reagent
                        for reagent in dry_reagents}

    # diethyl ether and ether should be the same
    cas_reagent_name_map = {}
    for reagent in xdl_obj.reagents:
        if reagent.id in SYNONYM_CAS_DICT:
            cas = SYNONYM_CAS_DICT[reagent.id]
            if cas in cas_reagent_name_map:
                cas_reagent_name_map[cas].append(reagent.id)
            else:
                cas_reagent_name_map[cas] = [reagent.id]
    for cas, reagents in cas_reagent_name_map.items():
        if len(reagents) > 1:
            for reagent in reagents[1:]:
                changed_reagents[reagent] = reagents[0]

    # If 'dry ether' and 'ether' are used, just keep 'dry ether'.
    for i in reversed(range(len(xdl_obj.reagents))):
        reagent = xdl_obj.reagents[i]
        if reagent.id in changed_reagents:
            xdl_obj.reagents.pop(i)
    # Using ether example above, replace all instances of 'ether' in steps with
    # 'dry ether'.
    for step in xdl_obj.steps:
        if type(step) == Repeat:
            for child in step.children:
                for k, v in child.properties.items():
                    if type(v) == str and v in changed_reagents:
                        child.properties[k] = changed_reagents[v]
        else:
            for k, v in step.properties.items():
                if type(v) == str and v in changed_reagents:
                    step.properties[k] = changed_reagents[v]
    return xdl_obj
