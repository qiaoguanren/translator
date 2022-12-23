import re

# from chemdata.solvents import lower_phase, SOLVENT_BOILING_POINTS, DCM
# from chemdata.synonyms import SYNONYM_CAS_DICT

from xdl import XDL
from xdl.utils.copy import xdl_copy

from chemputerxdl.steps import (
    Separate,
    HeatChill,
    Add,
    HeatChillToTemp,
    StartHeatChill,
    WashSolid,
    RunColumn,
    FilterThrough,
    Dissolve,
)
from xdl.steps import Repeat
from chemputerxdl.executor.tracking import iter_vessel_contents

# from chemdata.solvents import rotavap_mbar_p_for_50C_water_bath

from .constants import (
    DEFAULT_SLOW_ADDITION_DISPENSE_SPEED,
    DEFAULT_DROPWISE_DISPENSE_SPEED
)
from ..constants import float_regex_pattern, REFLUX_PLACEHOLDER_TEMP
from ..logging import get_logger

def fill_in_blanks(xdl_obj: XDL) -> XDL:
    """Fill in unknown values in procedure using different methods.

    Args:
        xdl_obj (XDL): XDL object to fill in unknown values.

    Returns:
        XDL: XDL object with unknown values filled in when possible.
    """
    if not xdl_obj.steps:
        return xdl_obj

    fill_in_missing_through_properties(xdl_obj)

    # Generate mock graph based on XDL to pass to prepare_for_execution.
    # Not using copy.deepcopy as that only works on Python 3.7.
    xdl_obj_copy = get_prepared_xdl_copy(xdl_obj)
    #guess_separation_phases(xdl_obj, xdl_obj_copy)

    #do_not_heat_empty_vessels(xdl_obj, xdl_obj_copy)

    # Make new copy as this can change step order.
    xdl_obj_copy = get_prepared_xdl_copy(xdl_obj)

    #guess_reflux_temperatures(xdl_obj, xdl_obj_copy)

    guess_neutralization_volumes(xdl_obj, xdl_obj_copy)

    #get_rotavap_pressures(xdl_obj, xdl_obj_copy)

    do_not_add_reagents_dropwise_to_empty_vessels(xdl_obj, xdl_obj_copy)
    return xdl_obj

def fill_in_missing_through_properties(xdl_obj: XDL) -> XDL:
    """If there is an 'eluted' action need to figure out from previous actions
    what to elute through.

    Args:
        xdl_obj (XDL): XDL object to fill in missing FilterThrough through
            properties.

    Returns:
        XDL: XDL with missing through properties filled in.
    """
    last_through = None
    for step in xdl_obj.steps:
        if 'through' in step.properties:
            if step.through != 'prev_through':
                if step.through:
                    last_through = step.through
            else:
                step.through = last_through
    return xdl_obj


def get_prepared_xdl_copy(xdl_obj: XDL) -> XDL:
    xdl_obj_copy = xdl_copy(xdl_obj)
    # Make sure there is no complication in making the fake graph and calling
    # prepare_for_execution.

    xdl_obj_copy.prepare_for_execution(
        xdl_obj_copy.graph(),
        interactive=False,
        sanity_check=False,
        filter_dead_volume_method='inert_gas',
        organic_cleaning_solvent='ether',
        auto_clean=False,
    )
    return xdl_obj_copy

def guess_separation_phases(xdl_obj: XDL, xdl_obj_copy: XDL) -> XDL:
    """Use solvent density data to guess which phase the product will be in in
    wash and extract steps.

    Args:
        xdl_obj (XDL): xdl_obj to set product_bottom property for all Separate
            steps.
        xdl_obj_copy (XDL): XDL object copy with prepared_for_execution called
            so iter_vessel_contents can be used.

    Returns:
        XDL: xdl_obj with product_bottom property guessed for all Separate steps.
            If product_bottom cannot be guessed it will be set to None and won't
            be written when saving the XDL.
    """
    logger = get_logger()
    if not Separate in [type(step) for step in xdl_obj.steps]:
        return xdl_obj
    # List to store bools (True if product in bottom phase, False if product
    # in top phase).
    product_bottoms = []
    # Need to call prepare_for_execution to access iter_vessel_contents so make
    # a deepcopy so the original xdl_obj is unchanged.
    # Assign all vessels etc so that iter_vessel_contents can be used.
    prev_vessel_contents = {}
    # Go through vessel_contents at every step, and use vessel contents along
    # with known solvent densities to determine what will be the lower phase.
    for i, step, vessel_contents, _ in iter_vessel_contents(
            xdl_obj_copy.steps, xdl_obj_copy.executor._graph):
            #xdl_obj_copy.steps, xdl_obj_copy.executor._graph_hardware):
        if type(step) == Separate:
            if step.from_vessel in prev_vessel_contents:
                from_vessel_contents = prev_vessel_contents[step.from_vessel].reagents

                # Edge case.
                # If previous step was an extraction, don't use entire
                # from_vessel contents, just use the solvent that the product
                # was extracted into for calculating product phase.
                if i > 0 and type(xdl_obj_copy.steps[i - 1]) == Separate:
                    prev_step = xdl_obj_copy.steps[i - 1]
                    if (prev_step.purpose == 'extract'
                        and prev_step.to_vessel == step.separation_vessel
                            and prev_step.solvent):
                        from_vessel_contents = [prev_step.solvent]

                if step.purpose == 'extract':
                    # Stops crash if solvent is None
                    # Extract, product will be in solvent, so append True if lower
                    # phase is step solvent, otherwise False.
                    if not step.solvent:
                        for reagent in from_vessel_contents:
                            if reagent.lower() in SYNONYM_CAS_DICT and SYNONYM_CAS_DICT[reagent.lower()] == DCM:
                                product_bottom = True
                                break
                        else:
                            product_bottom = False
                    else:
                        product_bottom = lower_phase(
                            step.solvent, from_vessel_contents)

                    if product_bottom == None:
                        product_bottoms.append(False)
                    else:
                        product_bottoms.append(product_bottom)

                # Wash product will be in from_vessel contents, so append True if
                # lower phase if from_vessel contents, otherwise False.
                elif step.purpose == 'wash':
                    # Stops crash if solvent is None
                    if not step.solvent:
                        for reagent in from_vessel_contents:
                            if reagent in SYNONYM_CAS_DICT and SYNONYM_CAS_DICT[reagent] == DCM:
                                product_bottom = True
                                break
                        else:
                            product_bottom = False
                    else:
                        logger.debug('Separation Phases: Guessing phase',
                                     from_vessel_contents, step.solvent)
                        product_bottom = lower_phase(
                            from_vessel_contents, step.solvent)

                    if product_bottom == None:
                        product_bottoms.append(False)
                    else:
                        product_bottoms.append(product_bottom)

            else:
                # Guess at False, better than nothing
                product_bottoms.append(False)
        prev_vessel_contents = vessel_contents

    # Apply product phases to original xdl_obj and return it.
    for step in xdl_obj.steps:
        if type(step) == Separate:
            step.product_bottom = product_bottoms.pop(0)
    return xdl_obj

def guess_reflux_temperatures(xdl_obj: XDL, xdl_obj_copy: XDL) -> XDL:
    """Use solvent boiling point data to guess what temperature reflux steps
    should heat to.

    Args:
        xdl_obj (XDL): XDL object to modify with guessed reflux temperatures.
        xdl_obj_copy (XDL): XDL object copy with prepared_for_execution called
            so iter_vessel_contents can be used.

    Returns:
        XDL: xdl_obj with reflux temperatures added to HeatChill steps where
            possible.
    """
    reflux_step_types = [HeatChill, HeatChillToTemp, StartHeatChill]
    if not any(
            [type(step) in reflux_step_types for step in xdl_obj_copy.steps]):
        return xdl_obj
    # List to store temperatures for all steps where temperature is stated as
    reflux_temps = []
    # Go through vessel_contents at every step, and use vessel contents along
    # with known solvent boiling points to work out reflux temperatures.
    for i, step, vessel_contents, _ in iter_vessel_contents(
            xdl_obj_copy.steps, xdl_obj_copy.executor._graph_hardware):
        if (type(step) in reflux_step_types
                and step.temp == REFLUX_PLACEHOLDER_TEMP):
            reflux_temps.append(25)
            if step.vessel in vessel_contents:
                solvent_reflux_temps = []
                for reagent in vessel_contents[step.vessel].reagents:
                    reagent_cas = None

                    # Infer aqueous solution from certain keywords
                    if any([item in reagent.lower()
                            for item in [
                                ' acid', ' hydroxide', 'aqueous ']]):
                        reagent_cas = SYNONYM_CAS_DICT['water']

                    if not reagent_cas:
                        reagent = reagent.lower()
                        for synonym in SYNONYM_CAS_DICT:
                            search = re.search(
                                r'(^| )(' + synonym + r')($| )', reagent)
                            if search:
                                reagent_cas = SYNONYM_CAS_DICT[search[2]]
                                break

                    if reagent_cas and reagent_cas in SOLVENT_BOILING_POINTS:
                        solvent_reflux_temps.append(
                            SOLVENT_BOILING_POINTS[reagent_cas])
                if solvent_reflux_temps:
                    # reflux_temps[-1] = sum(solvent_reflux_temps) / len(solvent_reflux_temps)
                    # Reversed to favour recent additions
                    for temp in reversed(solvent_reflux_temps):
                        if temp != 100:
                            reflux_temps[-1] = temp
                            break
                    else:
                        reflux_temps[-1] = solvent_reflux_temps[-1]

            # If no reflux temp found, and temp in previous step use that.
            if reflux_temps[-1] == 25:
                j = i - 1
                while j > 0 and xdl_obj_copy.steps[j].name == 'Transfer':
                    j -= 1
                if 'temp' in xdl_obj_copy.steps[j].properties:
                    reflux_temps[-1] = xdl_obj_copy.steps[j].temp

    # Apply reflux temperatures to original XDL object and return it.
    for i, step in enumerate(xdl_obj.steps):
        if (type(step) in reflux_step_types
                and step.temp == REFLUX_PLACEHOLDER_TEMP):
            step.temp = reflux_temps.pop(0)
            step.vessel = None  # Need to reassign vessel cos of temp change
    return xdl_obj

def guess_neutralization_volumes(xdl_obj: XDL, xdl_obj_copy: XDL) -> XDL:
    """For steps that just say 'the mixture was neutralised with 3 M
    hydrochloric acid', work out what volume should be used based on other
    reagents added in the procedure.

    LIMITATIONS:
        1) Only works for one neutralisation in procedure.
        2) Doesn't account for different stoichiometry of different acids/bases.
           e.g. 10 mL 3 M H2SO4 would go to 10 mL of 3 M NaOH when it
           should go to 20 mL as H2SO4 has two protons.

    Args:
        xdl_obj (XDL): XDL object to modify with neutralisation volumes.
        xdl_obj_copy (XDL): XDL object copy with prepared_for_execution called
            so iter_vessel_contents can be used.

    Returns:
        XDL: xdl_obj with volumes of neutralisation Add steps added if possible.
    """
    neutralisations = False
    for step in xdl_obj.steps:
        if step.name == 'Add' and step.volume == 111111:
            neutralisations = True
            break
    if not neutralisations:
        return xdl_obj
    # Go through vessel contents and find opposing reagents to acid/base used in
    # neutralization step.
    opposing_reagents = []
    for i, step, vessel_contents, _ in iter_vessel_contents(
            xdl_obj_copy.steps, xdl_obj_copy.executor._graph_hardware):
        # -0.001 is a hack in action_xdl_converters to label step as
        # neutralization
        if step.name == 'Add' and step.volume == 111111:
            # Get concentration from reagent name e.g.
            # '3 M hydrochloric acid' -> 3
            conc = parse_concentration(step.reagent)
            if conc:
                if is_acid(step.reagent):
                    neutralisation_type = 'acid'
                else:
                    neutralisation_type = 'base'
                # Look for reagent which is being neutralised in previous
                # step vessel contents.
                if step.vessel in prev_vessel_contents:
                    for reagent in prev_vessel_contents[
                            step.vessel].reagents:
                        # Lists below are [step_i, reagent, conc, volume]
                        # Volume is added later,
                        if neutralisation_type == 'acid' and is_base(reagent):
                            opposing_reagents.append([i, reagent, conc, None])
                        elif neutralisation_type == 'base' and is_acid(reagent):
                            opposing_reagents.append([i, reagent, conc, None])
        prev_vessel_contents = vessel_contents

    # If reagents being neutralised have been found get their volumes and add it
    # to the items in opposing_reagents.
    if opposing_reagents:
        for i, step in enumerate(xdl_obj_copy.base_steps):
            if step.name == 'CMove':
                from_vessel = xdl_obj_copy.executor._graph_hardware[step.from_vessel]
                for j in range(len(opposing_reagents)):
                    reagent = opposing_reagents[j][1]
                    if ('chemical' in from_vessel.properties
                            and from_vessel.chemical == reagent):
                        opposing_reagents[j][3] = step.volume

        # Calculate how much neutralising agent to add based on volume and conc
        # of opposing reagent.
        neutralization_add_volume = None
        for _, reagent, conc, neutralising_volume in opposing_reagents:
            neutralising_conc = parse_concentration(reagent)
            if neutralising_volume and neutralising_conc:
                neutralization_add_volume = (
                    (neutralising_volume * neutralising_conc) / conc)

        # If neutralising volume has been found add it to steps.
        if neutralization_add_volume != None:
            for step in xdl_obj.steps:
                if step.name == 'Add' and step.volume == 111111:
                    step.volume = neutralization_add_volume

    return xdl_obj

def parse_concentration(reagent_name: str) -> float:
    """Parse concentration in mol L-1 from reagent_name, e.g. '3 M NaOH' -> 3.

    Args:
        reagent_name (str): Reagent name to parse concentration from.

    Returns:
        float: Concentration parsed from reagent_name in mol L-1. If no conc is
            found then None.
    """
    conc_match = re.match(
        float_regex_pattern + r'[ ]?[mM][ ](.*)', reagent_name)
    conc = None
    if conc_match:
        try:
            conc = float(conc_match[1])
        except IndexError:
            pass
    return conc

def is_acid(reagent_name: str) -> bool:
    """Return True if reagent_name is of an acid, otherwise False.

    Args:
        reagent_name (str): Name of reagent.

    Returns:
        bool: True if reagent_name is an acid, otherwise False.
    """
    return 'acid' in reagent_name

def is_base(reagent_name: str) -> bool:
    """Return True is reagent_name is of a base, otherwise False.

    Args:
        reagent_name (str): Name of reagent.

    Returns:
        bool: True if reagent_name is a base, otherwise False.
    """
    return 'hydroxide' in reagent_name

def get_rotavap_pressures(xdl_obj: XDL, xdl_obj_copy: XDL) -> XDL:
    """Get rotavap pressures for all Evaporate steps based on solvents used.

    Args:
        xdl_obj (XDL): XDL object to add rotavap pressures to.
        xdl_obj_copy (XDL): XDL object copy with prepared_to_execution called.

    Returns:
        XDL: xdl_obj with rotavap pressures added where possible.
    """
    logger = get_logger()
    pressures = []
    prev_vessel_contents = {}
    for _, step, vessel_contents, _ in iter_vessel_contents(
            xdl_obj_copy.steps, xdl_obj_copy.executor._graph_hardware):
        if step.name == 'Evaporate' and step.pressure == None:
            pressure = None
            if step.rotavap_name in prev_vessel_contents:
                # Get all reagents in rotavap
                reagents = list(set([
                    reagent
                    for reagent in prev_vessel_contents[step.rotavap_name].reagents
                ]))
                reagent_pressures = []
                reagents_to_check = []
                cas_to_check = []
                # Get list of known solvents in rotavap. Use CAS numbers to
                # ignore duplicates with different synonyms like 'CH2Cl2' and
                # 'dichloromethane'.
                for reagent in reagents:
                    sub_reagents = reagent.split()
                    for sub_reagent in sub_reagents:
                        sub_reagent = sub_reagent.lower()
                        if sub_reagent in SYNONYM_CAS_DICT:
                            cas = SYNONYM_CAS_DICT[sub_reagent]
                            if not cas in cas_to_check:
                                cas_to_check.append(cas)
                                reagents_to_check.append(sub_reagent)
                logger.debug(
                    f'\nRV Pressure: Checking reagents for pressure: {", ".join(reagents_to_check)}')
                # Get pressures for all known solvents
                for _, reagent in enumerate(reagents_to_check):
                    pressure = rotavap_mbar_p_for_50C_water_bath(
                        reagent.lower())
                    if pressure:
                        logger.debug(
                            f'RV Pressure: Found pressure: {reagent} {pressure} mbar')
                        reagent_pressures.append(pressure)
                reagent_pressures = [
                    pressure for pressure in reagent_pressures if pressure]
                # Take pressure as average of pressures associated with all
                # known solvents.
                if reagent_pressures:
                    pressure = sum(reagent_pressures) / len(reagent_pressures)
                    logger.debug(
                        f'RV Pressure: Average pressure: {pressure} mbar')
            if not pressure:
                pressures.append(None)
            else:
                pressures.append(pressure)
        prev_vessel_contents = vessel_contents

    for step in reversed(xdl_obj.steps):
        if step.name == 'Evaporate' and step.pressure == None:
            pressure = pressures.pop()
            if pressure:
                step.pressure = pressure
                if not step.temp:
                    step.temp = 50
    return xdl_obj

def do_not_heat_empty_vessels(xdl_obj, xdl_obj_copy):
    """If additions are performed to an empty flask at not room-temperature,
    heating should only be performed after first addition so the empty flask or
    flask with a very small amount of liquid in it is not heated. Risk of local
    overheating, excessive reflux, temperature fluctuations due to sudden change
    in total heat capacity creating extra load on chiller if this is not done.

    Args:
        xdl_obj (XDL): XDL object to alter step order for to avoid heating empty
            vessels.
        xdl_obj_copy (XDL): XDL object with prepare_for_execution called so that
            iter_vessel_contents can be used to find out if vessels are empty.

    Returns:
        XDL: XDL object with step order changed so that empty vessels are not
            heated.
    """
    # Get steps to alter ordering
    alterations = []
    for _, step, vessel_contents, _ in iter_vessel_contents(
            xdl_obj_copy.steps, xdl_obj_copy.executor._graph_hardware):
        if type(step) == HeatChillToTemp:
            if step.temp <= 25:
                alterations.append(0)  # Not heating, don't alter
            else:
                if step.vessel in vessel_contents:
                    if vessel_contents[step.vessel].volume > 0:
                        # Vessel is not empty, don't alter
                        alterations.append(0)
                    else:
                        alterations.append(1)  # Vessel is empty, alter
                else:
                    alterations.append(1),  # Vessel is empty, alter

    # Switch HeatChillToTemp, Add, Add... sequences to
    # Add, HeatChillToTemp, Add... where the vessel involved has been found to
    # be empty at start of sequence.
    steps = xdl_obj.steps
    for i in reversed(range(len(steps))):
        if type(steps[i]) == HeatChillToTemp and alterations.pop():
            j = i
            liquid_start = j
            while j + 1 < len(steps) and type(steps[j + 1]) == Add:
                # Don't start heating if just solid in vessel.
                if liquid_start == i and steps[j + 1].volume != None:
                    liquid_start = j + 1
                j += 1
            if j > i:
                heatchill_step = steps.pop(i)
                steps.insert(liquid_start, heatchill_step)
    return xdl_obj

def do_not_add_reagents_dropwise_to_empty_vessels(
        xdl_obj: XDL, xdl_obj_copy: XDL) -> XDL:
    """Do not add reagents dropwise to empty vessels.

    Args:
        xdl_obj (XDL): XDLto alter
        xdl_obj_copy (XDL): XDL to use to determine if vessels are empty.

    Returns:
        XDL: XDL file with Add steps to empty vessels dropwise addition removed.
    """
    vessels_used = []
    for step in xdl_obj.steps:
        # Vessel is empty, don't add dropwise
        if type(step) == Add and not step.vessel in vessels_used:
            if step.dispense_speed in [
                DEFAULT_SLOW_ADDITION_DISPENSE_SPEED,
                DEFAULT_DROPWISE_DISPENSE_SPEED
            ]:
                step.dispense_speed = 'default'

        if type(step) in [Add, WashSolid, Dissolve]:
            if not step.vessel in vessels_used:
                vessels_used.append(step.vessel)

        elif type(step) in [Separate, FilterThrough, RunColumn]:
            if not step.to_vessel in vessels_used:
                vessels_used.append(step.to_vessel)

    return xdl_obj

def assign_stirring_to_add_steps(xdl_obj: XDL, xdl_obj_copy: XDL) -> XDL:
    """Use XDL vessel contents tracking to make sure Add steps only stir if
    there is already liquid in the vessel.

    Args:
        xdl_obj (XDL): XDL object to alter Add step stirring.
        xdl_obj_copy (XDL): XDL object with prepare_for_execution called so that
            iter_vessel_contents can be used to find out if vessels are empty.

    Returns:
        XDL: XDL object with Add step stirring altered so that Add steps only
            stir if there is already liquid in the vessel.
    """
    alterations = []
    prev_vessel_contents = {}
    for _, step, vessel_contents, _ in iter_vessel_contents(
            xdl_obj_copy.steps, xdl_obj_copy.executor._graph_hardware):

        stir = False
        # Only apply to False stirs as if stirring stated explicitly this
        # shouldn't affect it.
        if type(step) == Add and step.stir == False:
            if step.vessel in prev_vessel_contents:
                prev_contents = prev_vessel_contents[step.vessel]
                if prev_contents.reagents and prev_contents.volume > 0:
                    stir = True
            alterations.append(stir)

        elif type(step) == Repeat:
            for child in step.children:
                if type(child) == Add and child.stir is False:
                    if child.vessel in prev_vessel_contents:
                        prev_contents = prev_vessel_contents[child.vessel]
                        if prev_contents.reagents and prev_contents.volume > 0:
                            stir = True
                    alterations.append(stir)
        prev_vessel_contents = vessel_contents

    for step in xdl_obj.steps:
        if type(step) == Add and step.stir == False:
            step.stir = alterations.pop(0)
        elif type(step) == Repeat:
            for child in step.children:
                if type(child) == Add and child.stir is False:
                    child.stir = alterations.pop(0)

    return xdl_obj
