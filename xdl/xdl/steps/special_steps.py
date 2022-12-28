from typing import Union, List, Callable, Dict, Any
import logging
import time
import math
from functools import partial
from ..utils.logging import get_logger
from ..utils.prop_limits import TIME_PROP_LIMIT
from .base_steps import (
    Step,
    AbstractAsyncStep,
    AbstractStep,
    AbstractBaseStep,
    AbstractDynamicStep
)

if False:
    from chempiler import Chempiler

class Async(AbstractAsyncStep):
    """Wrapper to execute a step or sequence of steps asynchronously.

    Use like this:

    async_stir_step = Async(Stir(vessel=filter, time=3600))

    Can be stopped in between steps by calling async_stir_step.kill()

    Args:
        children (Union[Step, List[Step]]): Step object or list of Step objects
            to execute asynchronously.
        pid (str): Process ID. Optional, but must be given if using Await later
            in procedure.
        on_finish (Callable): Callback function to call after execution of steps
            has finished.
    """

    PROP_TYPES = {
        'children': Union[Step, List[Step]],
        'pid': str,
        'on_finish': Callable,
    }

    def __init__(
        self,
        children: Union[Step, List[Step]],
        pid: str = None,
        on_finish: Callable = None,
    ):
        super().__init__(locals())

        if type(children) != list:
            self.children = [children]

        self.steps = self.children

        self._should_end = False
        self.finished = False

    def async_execute(
        self, chempiler: 'Chempiler', logger: logging.Logger = None
    ) -> None:
        for step in self.children:
            keep_going = step.execute(chempiler, logger)
            if not keep_going or self._should_end:
                self.finished = True
                return

        self.finished = True
        if self.on_finish:
            self.on_finish()
        return True

    def human_readable(self, language='en'):
        human_readable = 'Asynchronous:\n'
        for step in self.children:
            human_readable += f'    {step.human_readable()}\n'
        return human_readable

class Await(AbstractBaseStep):
    """Wait for Async step with given pid to finish executing.

    Args:
        pid (str): pid of Async step to wait for.
    """

    PROP_TYPES = {
        'pid': str,
    }

    def __init__(self, pid: str, **kwargs):
        super().__init__(locals())
        self.steps = []

    def execute(
        self,
        async_steps: List[Async],
        logger: logging.Logger = None
    ) -> None:

        for async_step in async_steps:
            if async_step.pid == self.pid:
                while not async_step.finished:
                    time.sleep(1)
        return True

    def locks(self, chempiler):
        return [], [], []

class Repeat(AbstractStep):
    """Repeat children of this step self.repeats times.

    Args:
        repeats (int): Number of times to repeat children.
        children (List[Step]): Child steps to repeat.
    """

    PROP_TYPES = {
        'repeats': int,
        'children': Union[Step, List[Step]]
    }

    def __init__(
        self, repeats: int, children: Union[Step, List[Step]]
    ) -> None:
        super().__init__(locals())

        if type(children) != list:
            self.children = [children]

    def get_steps(self):
        steps = []
        for _ in range(self.repeats):
            steps.extend(self.children)
        return steps

    def human_readable(self, language='en'):
        human_readable = f'Repeat {self.repeats} times:\n'
        for step in self.children:
            human_readable += f'    {step.human_readable()}\n'
        return human_readable

class Loop(AbstractDynamicStep):
    """Repeat children of this step indefinitely.

    Args:
        children (List[Step]): Child steps to repeat.

    """

    PROP_TYPES = {
        'children': Union[Step, List[Step]]
    }

    def __init__(
        self, children: Union[Step, List[Step]]
    ) -> None:
        super().__init__(locals())

        if type(children) != list:
            self.children = [children]

    def on_start(self):
        """Nothing to be done."""
        return []

    def on_continue(self):
        """Perform child steps"""
        return self.children

    def on_finish(self):
        """Nothing to be done."""
        return []

class Wait(AbstractBaseStep):
    """Wait for given time.

    Args:
        time (int): Time in seconds
    """

    PROP_TYPES = {
        'time': float,
    }

    PROP_LIMITS = {
        'time': TIME_PROP_LIMIT,
    }

    def __init__(self, time: float, **kwargs) -> None:
        super().__init__(locals())

    def execute(
        self,
        platform_controller: Any,
        logger: logging.Logger = None,
        level: int = 0
    ) -> bool:
        # Don't wait if platform_controller is in simulation mode.
        if (hasattr(platform_controller, 'simulation')
                and platform_controller.simulation is True):
            return True

        time.sleep(self.time)
        return True

class Parallelizer(object):
    """Parallelize given blocks of steps and offer stream of steps to execute at
    given timesteps.
    """
    def __init__(
        self,
        chempiler: 'Chempiler',
        blocks: List[List[Step]],
        time_step: int = 1,
    ) -> None:
        """Initialise parallelizer, creating lock matrix and execution stream.

        Args:
            chempiler (Chempiler): Chempiler object to use for getting step
                durations and lock nodes, and eventually executing steps.
            blocks (List[List[Step]]): List of blocks to parallelize. More
                blocks can be added later.
            time_step (int): Time step in seconds of lock matrix. Defaults to 1.
        """
        self.block_id = 0
        self.chempiler = chempiler
        self.block_queue = blocks
        self.exstream = []  # Execution stream
        self.lockmatrix = []  # Matrix showing vessel locking over time
        self.nodes = [node for node in self.chempiler.graph.nodes()]
        self.time_step = time_step

        self.locks = []

        self.logger = get_logger()

        # Initialise lockmatrix and exstream
        self.process_first_block()

        # Add all remaining blocks to lockmatrix and exstream
        self.process_blocks()

    def get_step_end(self, step: Step, start_t: int) -> int:
        """Get the time step in the lockmatrix at which the given step ends
        using the given start time.

        Args:
            step (Step): Step object to use duration to determine end time step.
            start_t (int): Start time step in lockmatrix of the step.

        Returns:
            int: End time step in lockmatrix of the step.
        """
        return int(
            start_t + math.ceil(step.duration(self.chempiler)) / self.time_step)

    def get_lockmatrix(self, block: List[Step]) -> List[List[int]]:
        """Get lockmatrix for given block.

        Args:
            block (List[Step]): List of steps to get lockmatrix for.

        Returns:
            List[List[int]]: Lockmatrix for given block.
        """
        lockmatrix = []
        t = 0
        for step in block:
            for base_step in step.base_steps:
                # Get start and end time steps of step.
                step_start = t
                step_end = self.get_step_end(base_step, step_start)
                locks, ongoing_locks, unlocks = base_step.locks(self.chempiler)
                # Create lockmatrix
                for _ in range(step_end - step_start):
                    lockmatrix.append([])
                    for node in self.nodes:
                        if node in locks:
                            lockmatrix[-1].append(1)
                        elif node in ongoing_locks:
                            lockmatrix[-1].append(2)
                        elif node in unlocks:
                            lockmatrix[-1].append(3)
                        else:
                            lockmatrix[-1].append(0)
                t = step_end
        return self.apply_ongoing_locks(lockmatrix)

    def apply_ongoing_locks(
        self, lockmatrix: List[List[int]]
    ) -> List[List[int]]:
        """Fill in ongoing_locks in lockmatrix. Should be called whenever lock
        matrix is extended.

        Args:
            lockmatrix (List[List[int]]): Lock matrix to fill in ongoing locks.

        Returns:
            List[List[int]]: Updated lock matrix.
        """
        for i in range(len(lockmatrix[0])):
            ongoing_lock = False
            for j in range(len(lockmatrix)):
                if lockmatrix[j][i] == 2:
                    ongoing_lock = True
                    continue
                elif lockmatrix[j][i] == 3:
                    ongoing_lock = False
                    continue
                if ongoing_lock:
                    lockmatrix[j][i] = 2
        return lockmatrix

    def get_exstream(self, block: List[List[Step]]) -> List[List[Step]]:
        """Get execution stream for given block.

        Args:
            block (List[List[Step]]): Block to get execution stream for.

        Returns:
            List[List[Step]]: Execution stream for given block.
        """
        exstream = []
        t = 0
        for step in block:
            step_start = t
            step_end = self.get_step_end(step, step_start)
            exstream.append([step])
            while t < step_end:
                exstream.append([])
                t += 1
        return exstream

    def process_first_block(self) -> None:
        """Initialise lockmatrix and execution stream."""
        if not self.block_queue:
            return
        block = self.block_queue.pop(0)
        block_id = self.get_block_id()
        for step in block:
            step.locking_pid = block_id
        self.lockmatrix = self.get_lockmatrix(block)
        self.exstream = self.get_exstream(block)

    def get_block_id(self) -> str:
        """Return unique block ID and increment block_id counter.

        Returns:
            str: Unique block ID
        """
        block_id = f'block{self.block_id}'
        self.block_id += 1
        return block_id

    def process_blocks(self) -> None:
        """Add all blocks in queue to lockmatrix/execution stream."""
        while self.block_queue:
            block = self.block_queue.pop(0)
            block_id = self.get_block_id()
            for step in block:
                step.locking_pid = block_id
            block_lockmatrix = self.get_lockmatrix(block)
            block_exstream = self.get_exstream(block)
            for block_start_t in range(len(self.lockmatrix)):
                if self.check_block_compat(block_lockmatrix, block_start_t):
                    self.add_block_to_lockmatrix(
                        block_lockmatrix, block_start_t)
                    self.add_block_to_exstream(block_exstream, block_start_t)
                    break

    def check_block_compat(
        self, block_lockmatrix: List[List[int]], block_start_t: int
    ) -> bool:
        """Check if given block lockmatrix is compatible with the global
        lockmatrix at the given block start time step.

        Args:
            block_lockmatrix (List[List[int]]): Lock matrix for block being
                added.
            block_start_t (int): Time step to check block compatibility with
                global lock matrix, if the block starts at this time step.

        Returns:
            bool: True if the block can start at block_start_t, otherwise False.
        """
        for i in range(len(block_lockmatrix)):
            # Past end of lockmatrix, no conflicts
            if i + block_start_t >= len(block_lockmatrix):
                return True

            # Check for lock conflicts
            for j in range(len(block_lockmatrix[i])):
                if (block_lockmatrix[i][j] > 0
                        and self.lockmatrix[i + block_start_t][j] > 0):
                    return False

        # Gone through entire block and found no lock conflicts
        return True

    def add_block_to_exstream(
        self, block_exstream: List[List[Step]], block_start_t: int
    ) -> None:
        """Add block execution stream to the global execution stream starting
        at the given time step.

        Args:
            block_exstream (List[List[Step]]): Execution stream for block being
                added.
            block_start_t (int): Time step of global execution stream to add
                block execution stream at.
        """
        for i in range(len(block_exstream)):
            if block_start_t + i >= len(self.exstream):
                self.exstream.append([])
            self.exstream[block_start_t + i].extend(block_exstream[i])

    def add_block_to_lockmatrix(
        self, block_lockmatrix: List[List[int]], block_start_t: int
    ) -> None:
        """Add block lockmatrix to the global lockmatrix starting at the given
        time step.

        Args:
            block_lockmatrix (List[List[int]]): Lock matrix of block being
                added.
            block_start_t (int): Time step of global lock matrix to add block
                lock matrix to.
        """
        for i in range(len(block_lockmatrix)):
            # If past the end of lockmatrix append new row.
            if i + block_start_t >= len(self.lockmatrix):
                self.lockmatrix.append([])

            # Add block locks to lockmatrix
            for j in range(len(block_lockmatrix[i])):
                self.lockmatrix[i + block_start_t][j] += block_lockmatrix[i][j]

        self.apply_ongoing_locks(self.lockmatrix)

    def add_block(self, block: List[List[Step]]) -> None:
        """Add block to global lockmatrix/execution stream.

        Args:
            block (List[List[Step]]): Block to add to global lock matrix and
                execution stream.
        """
        self.block_queue.append(block)
        self.process_blocks()

    def execute(self) -> None:
        """Execute every step in execution stream."""
        while self.exstream:
            self.print_exstream()
            # Execute time step
            start_t = time.time()
            self.execute_time_step()
            time_elapsed = time.time() - start_t

            # Wait until time step duration has passed to execute next time
            # step.
            while time_elapsed < self.time_step:
                time.sleep(1)
                time_elapsed = time.time() - start_t

    def print_exstream(self) -> None:
        """Print entire contents of execution stream."""
        self.logger.info('Execution stream\n----------------\n')
        for block in self.exstream:
            for step in block:
                self.logger.info(step.human_readable())
            self.logger.info('')

    def execute_time_step(self) -> None:
        """Execute current time step."""
        time_step = self.exstream.pop(0)
        if not time_step:
            self.logger.info('Popping empty time step...')

        while time_step:
            # Execute all steps scheduled for current time step.
            for i in reversed(range(len(time_step))):
                step = time_step[i]
                if step.request_lock(self.chempiler, step.locking_pid):
                    self.execute_step(step)
                    time_step.pop(i)

            # If some steps could not be executed due to unreleased lock, wait
            # then try again.
            if time_step:
                self.logger.info(
                    f'Waiting to execute {len(time_step)} more steps in current\
 time step...')
                self.logger.info([
                    node
                    for node in self.chempiler.graph.nodes()
                    if self.chempiler.graph[node]['lock'] is not None
                ])
                time.sleep(1)

    def execute_step(self, step) -> None:
        """Asynchronously execute step, acquiring and releasing lock before and
        after execution.
        """
        step.acquire_lock(self.chempiler, step.locking_pid)
        async_step = Async(
            step,
            on_finish=partial(
                step.release_lock, self.chempiler, step.locking_pid)
        )
        async_step.execute(self.chempiler)

    def print_lockmatrix(self):
        """Print lock matrix with values color coded by lock type."""
        s = []
        for node in self.nodes:
            s.append(f'{str(node):>30} ')
        for row in self.lockmatrix:
            for i, item in enumerate(row):
                # Normal lock
                if item == 1:
                    s[i] += f'\033[1;33;49m{str(item):2}\033[0;37;49m'
                # Ongoing lock
                elif item == 2:
                    s[i] += f'\033[1;31;49m{str(item):2}\033[0;37;49m'
                # Unlock
                elif item == 3:
                    s[i] += f'\033[1;32;49m{str(item):2}\033[0;37;49m'
                # No lock
                else:
                    s[i] += f'{str(item):2}'
        self.logger.info('\n'.join(s))
        self.logger.info(
            f"    n_timesteps = {len(s[0].strip().split(' '))-1}")

class Callback(AbstractBaseStep):

    PROP_TYPES = {
        'fn': Callable,
        'args': List[Any],
        'keyword_args': Dict[str, Any]
    }

    def __init__(
        self,
        fn: Callable,
        args: List[Any] = [],
        keyword_args: Dict[str, Any] = {}
    ):
        super().__init__(locals())

    def execute(self, chempiler, logger, level=0):
        self.fn(*self.args, **self.keyword_args)

    def locks(self, chempiler):
        return [], [], []
