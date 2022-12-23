import argparse
import os

import appdirs
import ChemputerAPI
from chempiler import Chempiler

from xdl import XDLController


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("graph", type=str)
    args = parser.parse_args()

    graph_file = args.graph

    if not os.path.exists(graph_file) or not graph_file.lower().endswith(
        (".json", ".graphml")
    ):
        raise FileNotFoundError(f'"{graph_file}" is not a graph file.')

    platform_controller = Chempiler(
        experiment_code="standby",
        output_dir=appdirs.user_log_dir("xdl_standby"),
        graph_file=graph_file,
        simulation=True,
        device_modules=[ChemputerAPI],
    )

    xdl_controller = XDLController(platform_controller, graph_file)

    xdl_controller.standby(
        time_interval="24 hrs",
        solvent="water",
    )


if __name__ == "__main__":
    main()
