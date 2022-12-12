import numpy as np
import itertools
import math
import time
import copy
import datetime
from functools import partial
from tabulate import tabulate

from xdl.constants import VESSEL_PROP_TYPE, REAGENT_PROP_TYPE
from xdl.utils.logging import get_logger
from xdl.steps.special_steps import Async
from xdl.utils.graph import get_graph

from ..utils.execution import get_chempiler
from ..executor.graph import hardware_from_graph

# np.set_printoptions(linewidth=1000, threshold=1000000000)

class Parallelizer(object):
    """ Module for Parallel processing of XDL scripts.

    By specifying a list of XDL scripts and available hardware, the
    parallelizer automatically determines:

        i)  the optimal allocation of XDL steps to hardware resources.
        ii) the appropriate execution sequence for those steps.

    Resource Allocation
    -------------------

    1. For each XDL block supplied, all of the ways in which this block
        can be executed on the available harware are determined, and a
        corresponding XDL object is initialized for each of these.
        E.g. if two reactors are available but the XDL block calls for one,
        two XDL objects are generated - one for the use of each reactor.

    2. All possible combinations of these XDL objects are generated,
        selecting one XDL object per XDL block supplied. For each
        combination, the best possible resource allocation is derermined.

    3. The XDL object combination that produces the shortest execution
        time is chosen and passed on for execution.

    Execution
    ---------

    With the optimal XDL object combinaton, an execution stream is
    compiled, which consists of a list of steps that are to be
    executed at each time interval. At each time interval, all steps
    present are executed asynchronously, with hardware locked by the
    Chempiler before execution, and unlocked after.

    If a given step requests a hardware component that is locked by
    a step from a previous time interval, the step is delayed until
    the hardware component becomes available.

    """
    opt_block_positions = None
    opt_block_sequence = None

    def __init__(self, graph_file, xdl_objs, time_step=20):
        """Init method of the Parallelizer class.

        Args:
            graph_file (str): path to graph .json file that describes
                hardware availability and connectivity.
            xdl_objs (List[XDL]): list of initialised XDL objects that are
                to be run in parallel.
            time_step (int): interval (in seconds) used to discritize time into
                chunks. Once an execution order has been established, XDL steps
                will be executed asynchronously at the approproate time step.

        """
        self.graph_file = graph_file
        self.xdl_objs = xdl_objs
        self.time_step = time_step

        # initialize the graph from the graph file
        self.graph = get_graph(graph_file)

        # retrieve the graph hardware object from the graph
        self.graph_hardware = hardware_from_graph(self.graph)

        # initialize the chempiler object, used for locking and unlocking
        self.chempiler = get_chempiler(graph_file)

        # store a list of nodes in the hardware graph for convenience
        self.nodes = sorted([node for node in self.chempiler.graph.nodes()])

        # create empty execution stream
        # (list of steps to be executed at each time step)
        self.exstream = [[]]

        self.logger = get_logger()

    #######################
    # RESOURCE ALLOCATION #
    #######################

    def optimize_resource_allocation(self):
        """ Get possible mappings of XDL steps to graph hardware, generate
        possible combinations of these mappings for each XDL block and
        determine which combination gives the fastest execution time.

        """
        # determine possible xdl objects with correspnding harware mappings.
        # described by a dict {'block_name': [valid_xdl1, valid_xdl2, ...]}
        xdls_to_optimise = self.get_possible_xdl_objects()

        # initialize minimum timesteps
        self.required_timesteps = 10 ** 10

        # iterate through all possible XDL block combinations to determine
        # the combination with the shortest execution time
        for xdl_combo in itertools.product(*list(xdls_to_optimise.values())):
            blocks = [
                XDLBlock(
                    self.chempiler, xdl.steps, self.time_step, f'block{ix}'
                )
                for ix, xdl in enumerate(xdl_combo)
            ]
            self.optimize_xdlblock_compatibility(blocks)

        for block in self.opt_block_sequence:
            block.print_lock_matrix()

        # print('TIME SAVED:', self.max_timesteps - self.required_timesteps)
        # self.print_lock_matrix()

    def get_possible_xdl_objects(self):
        """By finding all valid mappings of XDL steps to hardware, determine
        all valid XDL objects that can execute a given block of steps.

        Returns:
            Dict[str, List[XDL]]: Each block ID and associated XDL objects.

        """
        valid_xdl_objs = {}

        # go through each xdl block, get possible hardware maps and create
        # new xld objects for each hardware map
        for i in range(len(self.xdl_objs)):

            block_id = f'block_{i}'
            hardware_maps = self.get_possible_hardware_maps(self.xdl_objs[i])

            # make a xdl object with each hardware map and prepare for execution
            valid_xdls = []
            for m in hardware_maps:
                xdl_obj = copy.deepcopy(self.xdl_objs[i])
                xdl_obj.prepare_for_execution(
                    self.graph_file,
                    hardware_map=m,
                    interactive=False,
                    full_procedure=False
                )
                valid_xdls.append(xdl_obj)

            # store possible xdl objects for each xdl block ID
            valid_xdl_objs[block_id] = valid_xdls

        return valid_xdl_objs

    def get_possible_hardware_maps(self, xdl_obj):
        """Get all possible maps of XDL step components to graph hardware

        Args:
            xdl_obj (XDL): xdl object to find mappings for

        Returns:
            List[Dict[str, str]]: For each valid hardware map, the
                corresponding XDL and graph hardware IDs to be passed to
                prepare_for_execution.

        """

        # determine valid maps for reactors
        map_reactors = self.get_component_class_map(
            xdl_obj.hardware.reactors, self.graph_hardware.reactors
        )

        # determine valid maps for filters
        map_filters = self.get_component_class_map(
            xdl_obj.hardware.filters, self.graph_hardware.filters
        )

        # determine valid maps for separators
        map_separators = self.get_component_class_map(
            xdl_obj.hardware.separators, self.graph_hardware.separators
        )

        # determine valid maps for rotavaps
        map_rotavaps = self.get_component_class_map(
            xdl_obj.hardware.rotavaps, self.graph_hardware.rotavaps
        )

        # compile all maps for hardware reqired by XDL
        map_all = [
            m
            for m in [map_reactors, map_filters, map_separators, map_rotavaps]
            if len(m) > 0
        ]

        # convert maps to dictionaries to be passed to prepare_for_execution
        hardware_map_dicts = []
        for m in itertools.product(*map_all):
            map_dict = {}
            for c_xdl, c_graph in m:
                map_dict[c_xdl] = c_graph
            hardware_map_dicts.append(map_dict)

        return hardware_map_dicts

    def get_component_class_map(self, xdl_components, graph_components):
        """ Retrieve possible XDL to Graph hardware maps for a given
        component class (reactor, separator, filter or rotavap).

        Args:
            xdl_components (List[Component]): xdl components of given class
            graph_components (List[Component]): graph components of given class

        Returns:
            List[List[str, str]]: Corresponding xdl and graph component IDs
                for each hardware map.

        """
        # iterate through all graph component permutations and map to
        # list of xdl components.
        component_map = []
        for p in itertools.permutations(graph_components):
            for i in range(len(xdl_components)):
                component_map.append(
                    [xdl_components[i].id, p[i].id]
                )
        return component_map

    def optimize_xdlblock_compatibility(self, blocks):
        """ Find the shortest execution time possible for the given XDL blocks.

        Args:
            blocks (List[XDLBlock]): list of XDLBlock objects

        """
        # get compatible block positions for all block sequence permutations
        for block_sequence in itertools.permutations(blocks):
            block_positions, lock_matrix = \
                self.get_valid_lock_matrix(block_sequence)

            required_timesteps = lock_matrix.shape[1]

            # store the shortest block sequence
            if required_timesteps < self.required_timesteps:
                self.required_timesteps = required_timesteps
                self.opt_block_sequence = block_sequence
                self.opt_block_positions = block_positions
                self.lock_matrix = lock_matrix

    def get_valid_lock_matrix(self, block_sequence):
        """Produce a lock matrix and relative block starting positions
        for a given block sequence. A lock matrix is considered valid when
        there is no overlap between locks of a set of XDLBlock lock matrices.

        Args:
            block_sequence (List[XDLBlock]): List of XDLBlock objects

        Returns:
            List[int]: Starting positions (time step) where XDLBlock can
                begin execution.
            Array: Hardware resource allocation across time steps expressed
                as a lock matrix - a matrix of integers describing the lock
                state of a given node on the hardware graph.

        """
        self.max_timesteps = 0
        for block in block_sequence:
            self.max_timesteps += block.n_timesteps

        # create an empty master lock matrix
        lock_matrix = np.full(
            (block_sequence[0].n_nodes, self.max_timesteps),
            0
        )
        # add blocks in non-overlapping positions to the master lock matrix
        block_positions = []
        for block in block_sequence:
            block.lock_matrix = block.generate_lock_matrix()

            block.lock_matrix = np.pad(
                block.lock_matrix,
                [(0, 0), (0, self.max_timesteps - block.lock_matrix.shape[1])]
            )

            # find compatible block position and add block to lock matrix
            shift = 0
            while np.sum(np.multiply(lock_matrix, block.lock_matrix)) > 0:
                block.lock_matrix = np.roll(block.lock_matrix, 1)
                shift += 1

            # update the master lock matrix
            lock_matrix = lock_matrix + block.lock_matrix
            block_positions.append(shift)

        # trim inactive time steps
        while sum(lock_matrix[:, -1]) == 0:
            lock_matrix = np.delete(lock_matrix, -1, axis=1)

        return block_positions, lock_matrix

    def print_lock_matrix(self):
        """Print lock matrix, for use in debugging

        """
        msg = f'\nNSTEPS: {self.lock_matrix.shape[1]}\n'
        for ix, locks in enumerate(self.lock_matrix):
            msg += f'{self.nodes[ix]:<30} {locks}\n'
        msg += '\n'
        self.logger.info(msg)

    #############
    # EXECUTION #
    #############

    def compile_execution_stream(self):
        """ Use optimised block sequence to determine steps to execute at
        each time step interval.

        """
        # compile the stream of steps to be executed at each time step
        for pos, block in zip(
            self.opt_block_positions,
            self.opt_block_sequence
        ):
            for i in range(len(block.exstream)):
                if (pos + i) >= len(self.exstream):
                    self.exstream.extend([[]])
                self.exstream[pos + i] += block.exstream[i]

    def execute(self):
        """ Go through each time step in the execution stream and execute the
        steps at each time interval asynchronously.

        """

        def execute_time_step():
            """ Execute every step at a given time interval

            """
            time_step = self.exstream.pop(0)
            if not time_step:
                self.logger.info('No action to take in this time step...')

            while time_step:
                # Execute all steps scheduled for current time step.
                for i in reversed(range(len(time_step))):
                    step = time_step[i]
                    if step.request_lock(self.chempiler, step.locking_pid):
                        execute_step(step)
                        time_step.pop(i)

                # If some steps could not be executed due to unreleased lock,
                # wait then try again.
                if time_step:
                    self.logger.info(
                        f'Waiting to execute {len(time_step)} more steps in \
current time step...')
                    self.logger.info([
                        node
                        for node in self.chempiler.graph.nodes()
                        if self.chempiler.graph[node]['lock'] is not None
                    ])
                    time.sleep(0.1)

        def execute_step(step):
            """ Execute a step

            Args:
                self (Step): XDL step to execute

            """
            # lock node on graph before execution
            step.acquire_lock(self.chempiler, step.locking_pid)

            # set up step as child of Async step, release lock on finish
            async_step = Async(
                step,
                on_finish=partial(
                    step.release_lock, self.chempiler, step.locking_pid)
            )
            async_step.execute(self.chempiler)

        # Execute time steps until execution stream is empty
        while self.exstream:
            self.print_exstream()

            # Execute time step
            start_t = time.time()
            execute_time_step()
            time_elapsed = time.time() - start_t

            # Wait time step duration to execute next time step.
            while time_elapsed < self.time_step - 19.8:
                time.sleep(0.1)
                time_elapsed = time.time() - start_t

    def print_exstream(self):
        """Print the execution stream

        """
        msg = '\n-----Execution stream------\n'
        for block in self.exstream:
            for step in block:
                msg += step.name
            msg += ''
        self.logger.info(msg)

    def get_schedule(self):
        """Get schedule which is list of timesteps and steps at those timesteps
        with their associated blocks.
        """
        schedule = []
        for pos, block in zip(
            self.opt_block_positions,
            self.opt_block_sequence
        ):
            for i in range(len(block.exstream)):
                if (pos + i) >= len(schedule):
                    schedule.append({
                        block.block_id: [] for block in self.opt_block_sequence
                    })
                schedule[pos + i][block.block_id].extend(
                    block.exstream[i]
                )
        return schedule

    def format_properties(self, step):
        s = ''
        for prop, val in step.properties.items():
            if prop not in step.INTERNAL_PROPS and prop != 'children' and val:
                if step.PROP_TYPES[prop] in [
                    VESSEL_PROP_TYPE, REAGENT_PROP_TYPE
                ]:
                    s += f'{prop}: {val}\n'
        return s

    def print_schedule(self):
        """Pretty print table showing the parallelised schedule"""
        schedule = self.get_schedule()
        table = [
            [str(datetime.timedelta(seconds=i * self.time_step))]
            for i in range(len(schedule))
        ]
        ongoing = {
            block_id: 0 for block_id in schedule[0]
        }
        durations = {
            block_id: 0 for block_id in schedule[0]
        }
        for i, timestep in enumerate(schedule):
            for block_id, steps in timestep.items():
                # Print step
                if len(steps) > 0:
                    step = steps[0]

                    table[i].append(
                        f'{step.name}\n{self.format_properties(step)}\n'
                    )
                    ongoing[block_id] = step.cached_duration - 1
                    durations[block_id] += step.cached_duration * self.time_step

                # Display '-' to show that the previous step is ongoing
                elif ongoing[block_id]:
                    table[i].append('-')
                    ongoing[block_id] -= 1

                # Nothing happening, blank cell
                else:
                    table[i].append('')

        self.logger.info(
            '\n'
            + tabulate(
                table,
                headers=['Time'] + list(schedule[0]),
                tablefmt='pretty'
            )
        )
        parallelised_time = self.time_step * len(table)
        linear_time = sum(list(durations.values()))
        time_saved = linear_time - parallelised_time

        duration_table = [
            ['Linear', str(datetime.timedelta(seconds=linear_time))],
            ['Parallel', str(datetime.timedelta(seconds=parallelised_time))],
            ['Time Saved', str(datetime.timedelta(seconds=time_saved))],
        ]
        self.logger.info(
            '\n'
            + tabulate(
                duration_table,
                headers=['Schedule', 'Duration'],
                tablefmt='pretty'
            )
        )


class XDLBlock(object):
    def __init__(self, chempiler, steps, time_step, block_id):
        """ Class to process and store locking and execution attributes
        of a given XDL object.

        Args:
            chempiler (Chempiler): Chempiler object used to determine lock
                states of nodes on graph
            steps (List[Step]): List of steps in XDL object
            time_step (int): time interval used by Parallelizer
            block_id (str): ID of block to be used as locking PID

        """
        self.chempiler = chempiler
        self.steps = steps
        self.time_step = time_step
        self.block_id = block_id

        # retrieve graph nodes
        self.nodes = [node for node in chempiler.graph.nodes()]
        self.n_nodes = len(self.nodes)

        # assign locking process IDs to steps in block
        for step in self.steps:
            step.locking_pid = self.block_id

        # calculate step and base step durations and total requires time steps
        self.step_durations, self.base_step_durations = self.get_durations()
        self.n_timesteps = sum(self.step_durations)

        # calculate hardware availability throughout execution time
        # expressed as lock matrix
        self.lock_matrix = self.generate_lock_matrix()

        # compile step execution stream for this block
        self.exstream = self.get_exstream()

        self.logger = get_logger()

    def generate_lock_matrix(self):
        """ Generate the lock matrix for this set of XDL steps.

        Returns:
            Array: Hardware resource allocation across time steps expressed
                as a lock matrix - a matrix of integers describing the lock
                state of a given node on the hardware graph.

        Possible locks:
            0 = No lock : hardware available
            1 = Lock : hardware in use
            2 = Ongoing Lock : hardware unavailable after previous use
            3 = Unlock : hardware again available

        """
        # for convenience, locks are initialized as a dict of numpy arrays
        # describing the locks for each node (key).
        self.lock_dict = {
            node: np.full(self.n_timesteps, 0)
            for node in self.nodes
        }

        i = 0
        t_start = 0

        # iterate through steps and assign lock states for each time interval
        for step in self.steps:
            for base_step in step.base_steps:

                # get lock states from chempiler
                locks, ongoing_locks, unlocks = base_step.locks(self.chempiler)

                # caclculate step duration
                t_end = t_start + self.base_step_durations[i]

                for node in locks:
                    self.lock_dict[node][t_start:t_end] = 1
                for node in ongoing_locks:
                    self.lock_dict[node][t_start:t_end] = 2
                for node in unlocks:
                    self.lock_dict[node][t_start:t_end] = 3

                t_start = t_end
                i += 1

        # fill in ongoing locks where neccessary
        self.apply_ongoing_locks()

        # make the lock matrix array from the lock dict
        lock_matrix = np.full((self.n_nodes, self.n_timesteps), 0)
        i = 0
        for node in sorted(self.lock_dict.keys()):
            lock_matrix[i, :] = self.lock_dict[node]
            i += 1

        return np.array(lock_matrix)

    def apply_ongoing_locks(self):
        """ Applies ongoing locks between locking and unlocking of
        appropriate vessels.

        """
        for node, locks in self.lock_dict.items():
            ongoing_lock = False
            for i in range(len(locks)):
                if locks[i] == 2:
                    ongoing_lock = True
                    continue
                elif locks[i] == 3:
                    ongoing_lock = False
                    continue
                if ongoing_lock:
                    locks[i] = 2
            self.lock_dict[node] = locks

    def get_exstream(self):
        """ Get the execution stream for this XDL block.

        Returns:
            List[List[Step]]: List of steps to be executed at each time step.

        """
        exstream = []
        t = 0
        for ix, step in enumerate(self.steps):
            step.cached_duration = self.step_durations[ix]
            step_end = t + self.step_durations[ix]
            exstream.append([step])
            while t < step_end - 1:
                exstream.append([])
                t += 1
        return exstream

    def get_durations(self):
        """ Calculate the durations - in terms of time intervals - for
        both Steps and Base Steps. The latter is required to account for the
        duration of steps that would not be considered in normal calculation
        of step durations.

        Returns:
            List[int]: duration (in time steps) of Steps
            List[int]: duration (in time steps) of Base Steps

        """
        step_durations, base_step_durations = [], []
        for step in self.steps:
            total_step_duration = 0
            for base_step in step.base_steps:
                base_step_duration = self.get_n_timesteps(base_step)
                base_step_durations.append(base_step_duration)
                total_step_duration += base_step_duration
            step_durations.append(total_step_duration)
        return step_durations, base_step_durations

    def get_n_timesteps(self, step):
        """ Get the number of time steps required to execute a XDL Step.
        This is always rounded up to the nearest time step integer.

        Args:
            step (Step): Step for which the duration will be calculated

        Returns:
            int: Number of time steps required to execute XDL Step

        """
        # use duration_accurate for CMove
        if step.name == 'CMove':
            return int(
                math.ceil(
                    step.duration_accurate(self.chempiler) / self.time_step
                )
            )
        # use regular duration method for all other steps
        else:
            return int(
                math.ceil(
                    step.duration(self.chempiler) / self.time_step
                )
            )

    def print_lock_matrix(self):
        """Print the lock matrix for this XDLBlock (used in debugging)

        """
        msg = f'\nNSTEPS {len(list(self.lock_dict.values())[0])}'
        for node, locks in sorted(self.lock_dict.items()):
            msg += f'\n{node:<30} {locks}'
        msg += '\n'
        self.logger.info(msg)
