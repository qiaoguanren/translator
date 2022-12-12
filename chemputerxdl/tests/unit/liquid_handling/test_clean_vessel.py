import os
import pytest
from ...utils import generic_chempiler_test

from xdl import XDL
from chemputerxdl.steps import (
    CleanBackbone,
    Dissolve,
    CleanVessel,
    Separate,
    HeatChillToTemp,
    HeatChillReturnToRT
)
from chemputerxdl.executor.constants import CLEAN_VESSEL_BOILING_POINT_FACTOR

HERE = os.path.abspath(os.path.dirname(__file__))
FOLDER = os.path.join(HERE, '..', 'files')

@pytest.mark.unit
def test_clean_vessel():
    """Test that dissolving a solid in the rotavap works."""
    xdl_f = os.path.join(FOLDER, 'clean_reactor_rotavap.xdl')
    graph_f = os.path.join(FOLDER, 'bigrig.json')
    generic_chempiler_test(xdl_f, graph_f)

@pytest.mark.unit
def test_clean_vessel_no_vacuum():
    xdl_f = os.path.join(FOLDER, 'clean_vessel_no_vacuum.xdl')
    graph_f = os.path.join(FOLDER, 'orgsyn_v81p0262.json')
    generic_chempiler_test(xdl_f, graph_f)


CLEAN_VESSEL_TESTS = [
    (os.path.join(FOLDER, 'alkyl_fluor_step4.xdl'),
     os.path.join(FOLDER, 'alkyl_fluor_step4.graphml'),
     None,
     2,
     ['acetonitrile', 'dcm'],
     [81.65 * CLEAN_VESSEL_BOILING_POINT_FACTOR,
      39.8 * CLEAN_VESSEL_BOILING_POINT_FACTOR]),

    (os.path.join(FOLDER, 'lidocaine.xdl'),
     os.path.join(FOLDER, 'lidocaine_graph.json'),
     'ether',
     1,
     ['ether'],
     [34.5 * CLEAN_VESSEL_BOILING_POINT_FACTOR]),
]

@pytest.mark.unit
def test_clean_vessel_scheduling():
    """Test that all CleanVessel steps are added at correct places, i.e.
    ...Dissolve, emptying_step, CleanVessel,..."""
    for (xdl_f, graph_f, organic_cleaning_solvent, n_clean_vessels,
         clean_vessel_solvents, clean_vessel_temps) in CLEAN_VESSEL_TESTS:
        print(xdl_f, graph_f)
        x = XDL(xdl_f)
        x.prepare_for_execution(
            graph_f,
            interactive=False,
            organic_cleaning_solvent=organic_cleaning_solvent
        )

        # Check right number of steps with right vessel/solvent have been added.
        clean_vessel_steps = [
            step for step in x.steps if type(step) == CleanVessel]
        assert len(clean_vessel_steps) == n_clean_vessels
        for i in reversed(range(len(clean_vessel_steps))):
            print(clean_vessel_steps[i].temp)
            assert(clean_vessel_steps[i].solvent.lower()
                   == clean_vessel_solvents.pop().lower())
            correct_temp = clean_vessel_temps.pop()
            assert clean_vessel_steps[i].temp == correct_temp
            assert type(clean_vessel_steps[i].steps[1]) == HeatChillToTemp
            assert clean_vessel_steps[i].steps[1].temp == correct_temp
            assert type(clean_vessel_steps[i].steps[-1]) == HeatChillReturnToRT

        # Check all CleanVessel steps come after Dissolve + filter_emptying step
        # or after Separate step.
        for i in range(len(x.steps)):
            emptying_step_passed = False
            legit = True
            if type(x.steps[i]) == CleanVessel:
                # Check default double clean is being done.
                assert (len([step
                             for step in x.steps[i].steps
                             if step.name == 'CMove']) == 4)
                legit = False
                j = i
                while j > 0:
                    j -= 1
                    #  Ignore CleanBackbone steps
                    if type(x.steps[j]) == CleanBackbone:
                        continue
                    # Dissolve steps encountered after emptying step.
                    elif type(x.steps[j]) == Dissolve and emptying_step_passed:
                        legit = True
                        break
                    elif type(x.steps[j]) == Separate:
                        legit = True
                        break
                    # Found emptying step.
                    elif not emptying_step_passed:
                        emptying_step_passed = True
                    # Emptying step already found but next step backwards is
                    # not a Dissolve step. Therefore CleanVessel is incorrectly
                    # placed.
                    else:
                        legit = False
                        break
                assert legit

@pytest.mark.unit
def test_clean_vessel_move_to_end():
    xdl_f = os.path.join(FOLDER, 'clean_vessel_at_end.xdl')
    graph_f = os.path.join(FOLDER, 'bigrig.json')
    x = XDL(xdl_f)
    x.prepare_for_execution(graph_f, interactive=False)

    # Ignore the Shutdown at the end
    check_steps = x.steps[:-1]
    assert len(
        [step for step in check_steps if step.name == 'CleanVessel']) == 1
    assert check_steps[-2].name == 'CleanVessel'
    generic_chempiler_test(xdl_f, graph_f)
