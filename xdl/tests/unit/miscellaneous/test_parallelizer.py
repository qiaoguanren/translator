import os
import json
import pytest

from chemputerxdl.steps import HeatChill, Transfer
# from xdl.execution import XDLExecutor
from chemputerxdl.executor import ChemputerExecutor
from xdl.steps.special_steps import Parallelizer
from networkx.readwrite.json_graph import node_link_graph

import ChemputerAPI
from chempiler import Chempiler

HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, '..', 'files', 'bigrig.json')) as fd:
    graph_dict = json.load(fd)
    graph = node_link_graph(graph_dict)

chempiler = Chempiler(
    experiment_code='test',
    output_dir=os.path.join(HERE, 'chempiler_output'),
    simulation=True,
    graph_file=graph_dict,
    device_modules=[ChemputerAPI])

executor = ChemputerExecutor(None)
block1 = [
    Transfer(from_vessel='flask_water', to_vessel='reactor', volume=1),
    Transfer(from_vessel='flask_ether', to_vessel='reactor', volume=1),
    HeatChill(vessel='reactor', temp=60, time='1 s'),
    # Transfer(from_vessel='reactor', to_vessel='filter', volume=1),
]

block2 = [
    Transfer(
        from_vessel='flask_chloroacetyl_chloride',
        to_vessel='filter',
        volume=1
    ),
    # Transfer(from_vessel='flask_ether', to_vessel='reactor', volume=5),
    # HeatChill(vessel='reactor', temp=60, time='30 s'),
    # Transfer(from_vessel='reactor', to_vessel='filter', volume=10),
]

executor.prepare_block_for_execution(graph_dict, block1)
executor.prepare_block_for_execution(graph_dict, block2)

p = None

@pytest.mark.skip(reason="Alpha WIP")
def test_block_scheduling():
    pytest.skip("Skipping Parallelizer WIP")
    p = Parallelizer(chempiler, [block1, block2], time_step=1)
    print('\n')
    print(len(p.exstream))
    for step, exs in enumerate(p.exstream):
        print(exs)
        # if len(exs) > 0:
        #    print(step, exs)

    # ex_list = [e[0] for e in p.exstream if len(e) > 0]
    assert block1[0] in p.exstream[0]
    assert block2[0] in p.exstream[0]

    p.print_lockmatrix()

@pytest.mark.skip(reason="Alpha WIP")
def test_exstream():
    pytest.skip("Skipping Parallelizer WIP")
    p = Parallelizer(chempiler, [block1, block2], time_step=1)
    p.execute()
