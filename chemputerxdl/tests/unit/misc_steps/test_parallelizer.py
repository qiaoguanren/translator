import os
import pytest
import logging
from xdl import XDL

from chemputerxdl.parallelizer import Parallelizer

HERE = os.path.abspath(os.path.dirname(__file__))
FOLDER = os.path.join(HERE, '..', 'files')

logging.getLogger('xdl').setLevel(logging.INFO)

@pytest.mark.unit
def test_parallelizer():
    """Test parallel processing of XDL files. Both reactors should be
    used in execution.
    """

    # load a minimal graph with 2 reactors
    graph_f = os.path.join(FOLDER, 'graph_minimal_2reactor.json')

    # instantiate 2 xdl objects tp be passed to parallelizer
    xdl1 = XDL(os.path.join(FOLDER, 'parallel_1.xdl'))
    xdl2 = XDL(os.path.join(FOLDER, 'parallel_2.xdl'))

    p = Parallelizer(graph_f, [xdl1, xdl2], time_step=300)

    p.optimize_resource_allocation()
    p.compile_execution_stream()

    # log the optimised lock matrix
    p.print_lock_matrix()
    p.print_schedule()
    # go through execution stream and execute each time step
    # p.execute()
