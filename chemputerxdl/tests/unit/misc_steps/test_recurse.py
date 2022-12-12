import os
import pytest
from xdl import XDL
from chemputerxdl.steps import (
    Recurse,
    Add,
    MWAddAndTurn,
    CleanBackbone,
    CWait)
from ...utils import generic_chempiler_test

HERE = os.path.abspath(os.path.dirname(__file__))
FOLDER = os.path.join(HERE, '..', 'files')

@pytest.mark.unit
def test_basic_recursion():
    """
    This test will make sure simple recursion is working correctly. It is
    assumed for the purposes of this test that reagent inputs will be the same
    for every cycle in the recursive experiment.
    """

    xdl_f = os.path.join(FOLDER, "recursion_simple.xdl")
    graph_f = os.path.join(FOLDER, "ALChem_2_v6_sample_wheel_v2.json")
    generic_chempiler_test(xdl_f, graph_f)

    x = XDL(xdl_f)
    x.prepare_for_execution(graph_f, interactive=False)

    for step in x.steps:
        if type(step) == Recurse:
            assert len(step.steps) == 36

            adds, mw_adds, cleans = [], [], []

            for j, substep in enumerate(step.steps):
                if j in [6, 13, 22, 29]:
                    assert type(substep) == CWait
                if j in [20, 21]:
                    assert type(substep) == CleanBackbone
                if type(substep) == Add:
                    adds.append(j)
                    if j > 6:
                        if substep.vessel == 'reactor1':
                            assert substep.volume == 10
                        if substep.vessel == 'reactor4':
                            if substep.reagent == 'ipa':
                                assert substep.volume == 2.5
                            if substep.reagent == 'water':
                                assert substep.volume == 7.5
                elif type(substep) == MWAddAndTurn:
                    mw_adds.append(j)
                    if j > 6:
                        assert substep.volume == step.sampling_volume
                    else:
                        assert substep.volume == 12
                elif type(substep) == CleanBackbone:
                    cleans.append(j)
            assert len(adds) == step.n_cycles * 3
            assert len(cleans) == 2
            assert len(mw_adds) == step.n_cycles
