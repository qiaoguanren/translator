from typing import Any, Union, List
import hashlib
from abc import ABC
from networkx.readwrite import node_link_data
from networkx import MultiDiGraph

from .utils import do_sanity_check
from ..steps.special_steps import Async, Await
from ..steps.base_steps import Step, AbstractDynamicStep
from ..steps import NON_RECURSIVE_ABSTRACT_STEPS
from ..errors import (
    XDLExecutionOnDifferentGraphError,
    XDLExecutionBeforeCompilationError
)
from ..utils import get_logger
from ..utils.graph import get_graph
if False:
    from ..xdl import XDL

class AbstractXDLExecutor(ABC):
    """Abstract class for XDL executor. The main functionality of this class is
    to perform compilation and execution of a given XDL object.

    Args:
        xdl (XDL): XDL object to compile / execute.

    Abstract Methods:
        _graph_hash -> str: Hash function for graph used to determine whether
            graph used to compile XDLEXE is the same as the one being used to
            execute it.
        prepare_for_execution: There is a bare bones implementation of this,
            but it should be overridden, especially for hardware mapping and
            anything else that is necessary to make procedures executable.

    Methods:
        perform_sanity_checks: Perfom sanity checks recursively for every step
            in XDL. Should be called at end of prepare_for_execution.
        add_internal_properties: Recursively add internal properties to every
            step in XDL.
        prepare_dynamic_steps_for_execution: Prepare start blocks of all
            dynamic steps for execution.
        execute_step: Execute individual step.
        execute: Execute entire procedure.
    """
    _prepared_for_execution = False
    _xdl = None
    _graph = None
    logger = None

    def __init__(self, xdl: 'XDL' = None) -> None:
        """Initalize member variables."""
        self._xdl = xdl
        self.logger = get_logger()

    ####################
    # Abstract Methods #
    ####################

    def _graph_hash(self, graph: MultiDiGraph = None) -> str:
        """Get SHA 256 hash of graph. Used to determine whether graph used for
        execution is the same as the one used for compilation.

        Recommended to override this basic implementation, as this will give
        you a different hash if the position of nodes change, even if the
        properties and connectivity stays the same.

        Args:
            graph (MultiDiGraph): Graph to get hash of.

        Returns:
            str: Hash of graph.
        """
        if not graph:
            graph = self._graph
        return hashlib.sha256(
            str(node_link_data(graph)).encode('utf-8')
        ).hexdigest()

    def prepare_for_execution(
        self,
        graph_file: Union[str, MultiDiGraph],
        **kwargs
    ) -> None:
        """Abstract compile method. Should perform all necessary steps to
        convert self._xdl into an executable form. Minimum is adding internal
        properties, doing sanity checks and setting self._prepared to True.

        This used to be called prepare_for_execution but is being renamed to
        compile as this has become the verbally used term and is less effort
        to type.

        Args:
            graph_file (Union[str, MultiDiGraph]): Path to graph file, or loaded
                graph to compile procedure with.
        """
        self._graph = get_graph(graph_file)
        self.add_internal_properties()
        self.perform_sanity_checks()
        self._prepared = True

    ########################
    # Non Abstract Methods #
    ########################

    def perform_sanity_checks(self, steps: List[Step] = None) -> None:
        """Recursively perform sanity checks on every step in steps list. If
        steps list not given defaults to self._xdl.steps.

        Args:
            steps (List[Step]): List of steps to perform sanity checks
                recursively for every step / substep.
                Defaults to self._xdl.steps
        """
        if steps is None:
            steps = self._xdl.steps
        for step in steps:
            do_sanity_check(self._graph, step)

    def add_internal_properties(
        self,
        graph: MultiDiGraph = None,
        steps: List[Step] = None
    ) -> None:
        """Recursively add internal properties to all steps and substeps in
        given list of steps.

        Args:
            graph (MultiDiGraph): Graph to use for adding internal properties.
            steps (List[Step]): List of steps to add internal properties to.
        """
        if graph is None:
            graph = self._graph
        if steps is None:
            steps = self._xdl.steps

        # Iterate through each step
        for step in steps:

            # Prepare the step for execution
            step.on_prepare_for_execution(graph)

            # Special case for Dynamic steps
            if isinstance(step, AbstractDynamicStep):
                step.prepare_for_execution(graph, self)

            # If the step has children, add internal properties to all children
            if 'children' in step.properties:
                self.add_internal_properties(graph, step.children)

            # Recursive steps, add internal proerties to all substeps
            if not isinstance(step, NON_RECURSIVE_ABSTRACT_STEPS):
                self.add_internal_properties(graph, step.steps)

    def prepare_dynamic_steps_for_execution(
        self,
        step: Step,
        graph: MultiDiGraph
    ) -> None:
        """Prepare any dynamic steps' start blocks for execution. This is used
        during add_internal_properties and during execution. The reason for
        using during execution is that when loaded from XDLEXE dynamic steps do
        not have a start block. In the future the start block of dynamic steps
        could potentially be saved in the XDLEXE.

        Args:
            step (Step): Step to recursively prepare any dynamic steps for
                execution.
            graph (MultiDiGraph): Graph to use when preparing for execution.
        """
        if isinstance(step, AbstractDynamicStep):
            if step.start_block is None:
                step.prepare_for_execution(graph, self)
            for substep in step.start_block:
                self.prepare_dynamic_steps_for_execution(substep, graph)
        elif not isinstance(step, NON_RECURSIVE_ABSTRACT_STEPS):
            for substep in step.steps:
                self.prepare_dynamic_steps_for_execution(substep, graph)

    def execute_step(
        self,
        platform_controller: Any,
        step: Step,
        async_steps: List[Async] = []
    ) -> bool:
        """Execute single step.

        Args:
            platform_controller (Any): Platform controller to use to execute
                step.
            step (Step): Step to execute.
            async_steps (List[Async]): List of async steps to pass to step
                execute method if step is an Await step.

        Returns:
            bool: If True, execution will continue, if False execution will
                stop.
        """
        # Prepare start blocks of any dynamic steps for execution.
        # This is because dynamic steps loaded from XDLEXE are not prepared
        # for execution. This needs to be changed to be compatible with other
        # platform controllers. Potentially start blocks should be saved to
        # XDLEXE.
        if hasattr(platform_controller, 'graph'):
            self.prepare_dynamic_steps_for_execution(
                step, platform_controller.graph.graph)

        self.logger.info(step.name)

        try:
            # Wait for async step to finish executing
            if type(step) == Await:
                keep_going = step.execute(async_steps, self.logger)

            # Normal step execution
            else:
                keep_going = step.execute(
                    platform_controller, self.logger)

        # Raise any errors during step execution with additional info about step
        # that failed.
        except Exception as e:
            self.logger.info(f'Step failed {type(step)} {step.properties}')
            raise e

        return keep_going

    def execute(self, platform_controller: Any) -> None:
        """Execute XDL procedure with given platform controller.
        The same graph must be passed to the platform controller and to
        prepare_for_execution.

        Args:
            platform_controller (Any): Platform controller object to execute XDL
                with.

        Raises:
            XDLExecutionOnDifferentGraphError: If trying to execute XDLEXE on
                different graph to the one which was used to compile it.
            XDLExecutionBeforeCompilationError: Trying to execute XDL object
                before it has been compiled.
        """
        # XDLEXE, check graph hashes match
        if not self._prepared_for_execution and self._xdl.compiled:

            # Currently, this check only performed for Chemputer
            if hasattr(platform_controller, 'graph'):

                # Check graph hashes match
                if self._xdl.graph_sha256 == self._graph_hash(
                        platform_controller.graph.graph):

                    self.logger.info('Executing xdlexe, graph hashes match.')
                    self._prepared_for_execution = True

                # Graph hashes don't match raise error
                else:
                    raise XDLExecutionOnDifferentGraphError()

        # Execute procedure
        if self._prepared_for_execution:
            self.logger.info(
                f'\nProcedure\n---------\n\n{self._xdl.human_readable()}\n\n')

            # Store all ongoing async steps, so that they can be joined later
            # if necessary.
            async_steps = []

            # Iterate through all steps and execute.
            for step in self._xdl.steps:

                # Store all Async steps so that they can be awaited.
                if type(step) == Async:
                    async_steps.append(step)

                # Execute step
                keep_going = self.execute_step(
                    platform_controller, step, async_steps=async_steps)

                # If return value of step execution requests execution break,
                # then return.
                if not keep_going:
                    return

        else:
            raise XDLExecutionBeforeCompilationError()
