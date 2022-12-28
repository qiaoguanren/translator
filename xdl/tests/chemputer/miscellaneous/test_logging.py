import logging
import os
import re
import sys
import time

import pytest

from xdl import XDL

try:
    from chempiler.tools.logging import console_filter
    from chemputerxdl import ChemputerPlatform
except ModuleNotFoundError:
    pass

from ...utils import get_chempiler, remove_dir

HERE = os.path.abspath(os.path.dirname(__file__))
FOLDER = os.path.join(HERE, "..", "..", "files")
INTEGRATION_FOLDER = os.path.join(HERE, "..", "..", "files")

CHEMPILER_OUTPUT = os.path.join(HERE, "chempiler_output")
os.makedirs(CHEMPILER_OUTPUT, exist_ok=True)
TEMP_LOG_FILE = os.path.join(CHEMPILER_OUTPUT, "logging-test.txt")


class RemoveANSIFormatter(logging.Formatter):
    """Formatter to remove ANSI codes introduced by user of ``termcolor``.

    Necessary for saving logs to file.
    """

    ansi_re = re.compile(r"\x1b\[[0-9;]*m")

    def format(self, record):  # noqa: A003
        return re.sub(self.ansi_re, "", record.msg)


test_handler: logging.FileHandler = None


def add_logging_handler():
    """Add logging handler to xdl logger that will save logs to a temporary
    test file for verification.
    """
    # Global test handler so the object can be used when removing it after the
    # test. I don't know why this has to be in here and you can't create the
    # handler globally, but it doesn't work when running more than one test and
    # removing / re-adding the handler if you create the handler outside this
    # function.
    global test_handler
    test_handler = logging.FileHandler(TEMP_LOG_FILE)
    test_handler.setFormatter(RemoveANSIFormatter())

    # Needs chempiler dependency so has to be wrapped
    try:
        test_handler.addFilter(console_filter)
    except Exception:  # nosec B110  # TODO: Really ignore exception?
        pass
    test_handler.setLevel(logging.INFO)

    logger = logging.getLogger("xdl")
    logger.addHandler(test_handler)


def remove_logging_handler():
    """Remove test logging handler."""
    logger = logging.getLogger("xdl")
    logger.removeHandler(test_handler)


TESTS = [
    ("async.xdl", "bigrig.json"),
    ("repeat_parent.xdl", "bigrig.json"),
    ("async_advanced.xdl", "async_advanced.json"),
]


@pytest.mark.chemputer
@pytest.mark.parametrize(
    argnames="test_case",
    argvalues=TESTS,
    ids=[item[0] for item in TESTS],
)
def test_logging_step_indexes(test_case):
    """Test that there are no irregular patterns in step indexes in execution
    logs.
    """
    # Add test handler to save logs to file
    add_logging_handler()

    xdl_f, graph_f = test_case
    xdl_full_f = os.path.join(FOLDER, xdl_f)
    graph_full_f = os.path.join(FOLDER, graph_f)

    # Try to run the test and verify the logs
    try:
        # Reset test log file
        if os.path.exists(TEMP_LOG_FILE):
            with open(TEMP_LOG_FILE, "w") as fd:
                fd.write("")

        # Execute test file execution
        c = get_chempiler(graph_full_f)
        x = XDL(xdl_full_f, platform=ChemputerPlatform)
        x.prepare_for_execution(graph_full_f, testing=True)
        x.execute(c)

        # Wait for all threads to finish
        if xdl_f.startswith("async"):
            time.sleep(2)

        # Verify the logs
        verify_logs()

    # In the case an exception is thrown during the test, log the test files
    # that failed before raising the exception.
    except Exception as e:
        logger = logging.getLogger("xdl")
        logger.exception(f"Failed: {xdl_f} {graph_f}")
        raise e

    # Cleanup. Remove the temporary log file and the test logging handler.
    remove_logging_handler()
    if sys.platform.startswith("win"):
        remove_dir(CHEMPILER_OUTPUT)


@pytest.mark.chemputer
def test_logging_step_indexes_executing_steps_individually():
    """Test that step indexes also work when executing steps individually."""
    # Add test handler to save logs to file
    add_logging_handler()

    xdl_f = os.path.join(INTEGRATION_FOLDER, "DMP.xdl")
    graph_f = os.path.join(INTEGRATION_FOLDER, "DMP_graph.json")

    # Try to run the test and verify the logs
    try:
        # Reset test log file
        if os.path.exists(TEMP_LOG_FILE):
            with open(TEMP_LOG_FILE, "w") as fd:
                fd.write("")

        # Execute test file execution
        c = get_chempiler(graph_f)
        x = XDL(xdl_f, platform=ChemputerPlatform)
        x.prepare_for_execution(graph_f, testing=True)
        for i, step in enumerate(x.steps):
            # Check passing step object works
            if i % 2 == 0:
                x.execute(c, step)
            # Check passing step index works
            else:
                x.execute(c, i)

        # Verify the logs
        verify_logs()

    # In the case an exception is thrown during the test, log the test files
    # that failed before raising the exception.
    except Exception as e:
        logger = logging.getLogger("xdl")
        logger.exception(f"Failed: {xdl_f} {graph_f}")
        raise e

    # Cleanup. Remove the temporary log file and the test logging handler.
    remove_logging_handler()
    if sys.platform.startswith("win"):
        remove_dir(CHEMPILER_OUTPUT)


def verify_logs():
    """Verify log files contain no errors. Conditions checked for:

    1. All step starts have a corresponding step end.
    2. There are no duplicate step starts or step ends.
    """
    # Get step starts / ends in format [('start', '1.4'), ('end', '1.4')...] in
    # the order that they appear in the log file.
    step_index_rows = parse_logs()
    open_indexes = []
    all_indexes = []
    for start_or_finish, step_index in step_index_rows:
        # Store all step indexes encountered
        all_indexes.append(step_index)

        # Track which steps have been started and finished to check that there
        # is a start and finish for all steps.
        if start_or_finish == "start":
            open_indexes.append(step_index)
        else:
            try:
                open_indexes.remove(step_index)
            except ValueError:
                raise ValueError(
                    f"Step finish logged without corresponding step start\
{step_index}"
                )
    # Assert condition 1, all step starts have a corresponding step end.
    assert not open_indexes

    # Assert condition 2, there are no duplicate step starts or step ends.
    assert len(set(all_indexes)) == len(all_indexes) / 2


def parse_logs():
    """Convert logs to list of step starts and ends in format:
    [('start', '1'), ('start', '1.1'), ('end', '1.1'), ('end', '1')...]
    """
    # Searches for 2.2.1 etc. Allows 30 levels of depth.
    index_re = r"[0-9]" + r"(\.)?[0-9]?" * 30

    # Extract lines
    with open(TEMP_LOG_FILE) as fd:
        lines = [line.strip() for line in fd.readlines() if line.strip()]

    # Extract lines containing step starts / finishes
    step_index_lines = []
    for line in lines:
        if line.startswith(("Executing step", "Finished executing step")):
            step_index_lines.append(line)

    # Convert step starts and finishes to (start/end, step_index) format.
    step_index_rows = []
    for line in step_index_lines:
        if line.startswith("Executing step"):
            step_index_rows.append(("start", re.search(index_re, line)[0]))
        else:
            step_index_rows.append(("end", re.search(index_re, line)[0]))
    return step_index_rows
