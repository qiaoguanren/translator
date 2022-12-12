=========================
Integrating New Platforms
=========================

XDL is designed to be platform-independent, so that XDL files can be written once,
and the same file executed on two completely different platforms, that both support
the same synthetic operations. The two platforms currently implemented for XDL
are the Cronin group's Chemputer and Modular Wheel systems. This aims to be a
complete guide to integrating any other platform into the system.

Creating a custom platform
*****************************

To add support for another platform, you must make a subclass of `xdl.platforms.AbstractPlatform`. This class
has two abstract methods, `step_library` and `executor`, that must be implemented.

::

    from xdl.platforms import AbstractPlatform

    class MyPlatform(AbstractPlatform):

        def step_library(return):
            return

        def executor(self):
            return

Creating a custom executor
**************************

An executor must be created as a subclass of `xdl.execution.AbstractExecutor`.
The only method that needs to be implemented is `prepare_for_execution`. What this
method does is very flexible and depends on the specific platform. The general purpose
of the method is to take a XDL object (the attribute `self._xdl`), and alter it
so that it will be executable using the given graph. The minimum
it must do is to replace vessel names in the XDL with appropriate node names from the graph.
Other things that can be done at this stage are rigorously checking compatibility
of the graph and adding in cleaning routines.

::

    from xdl.execution import AbstractExecutor

    class MyExecutor(AbstractExecutor):

        def prepare_for_execution(
            graph_file,
            interactive: bool = True,
            save_path: str = '',
            sanity_check: bool = True
        ):
            return

Creating a custom step library
******************************
