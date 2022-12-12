"""
.. module:: utils.execution
    :platforms: Unix, Windows
    :synopsis: Utility functions for use within the platform Executor

"""

from typing import Tuple, Dict, Optional, List
from networkx import MultiDiGraph, NetworkXNoPath
from networkx.algorithms import shortest_path_length
from xdl.utils.graph import undirected_neighbors
from xdl.constants import INERT_GAS_SYNONYMS, AIR
from xdl.errors import XDLError
from ..constants import (
    VACUUM_CLASSES,
    CHEMPUTER_FLASK,
    CHEMPUTER_FILTER,
    CHEMPUTER_PUMP,
    CHEMPUTER_WASTE,
    CHEMPUTER_VALVE,
    CHEMPUTER_CARTRIDGE,
    STIRRER_CLASSES,
    HEATER_CLASSES,
    CHILLER_CLASSES,
    FILTER_CLASSES,
    REACTOR_CLASSES,
    ROTAVAP_CLASSES,
    SEPARATOR_CLASSES,
    FLASK_CLASSES
)
# from chempiler import Chempiler
# import ChemputerAPI
# import commanduinolabware

def get_unused_valve_port(graph: Dict, valve_node: str) -> Optional[int]:
    """Gets the unused ports on a given valve

    Args:
        graph (Dict): Graph to check
        valve_node (str): Valve to check

    Returns:
        Optional[int]: Unused port, none if not found
    """

    used_ports = []
    # Get connected valve positions (In edges).
    for _, _, edge_data in graph.in_edges(valve_node, data=True):
        if 'port' in edge_data:
            used_ports.append(str(edge_data['port'][1]))

    # Get connected valve positions (Out edges).
    for _, _, edge_data in graph.out_edges(valve_node, data=True):
        if 'port' in edge_data:
            used_ports.append(str(edge_data['port'][0]))

    # Return first found unconnected valve positions.
    for i in range(0, 6):  # Possible valve ports are 0, 1, 2, 3, 4, 5.
        if str(i) not in used_ports:
            return str(i)

    # None found
    return None

def get_pneumatic_controller(
    graph: MultiDiGraph, vessel: str, port: str = None
) -> Tuple[str, int]:
    """Given vessel, return pneumatic controller node that is a direct neighbour
    of the vessel in the graph, with the pneumatic controller port number.

    Args:
        vessel (str): Vessel to find attached pneumatic controller
        graph (MultiDiGraph): Graph containing vessel

    Returns:
        Tuple[str, int]: (pneumatic_controller_node, pneumatic_controller_port)
    """

    controller, controller_port, vessel_port = None, None, None

    for src_node, _, info in graph.in_edges(vessel, data=True):
        if graph.nodes[src_node]['class'] == 'PneumaticController':
            controller = src_node
            controller_port, vessel_port = info['port']

            if port is None:
                return src_node, controller_port

            elif port == vessel_port:
                return src_node, controller_port

    return controller, controller_port

def get_vacuum_configuration(
    graph: MultiDiGraph, vessel: str
) -> Dict[str, str]:
    """Get node names and ports to fully describe vacuum setup as follows:
    vessel <-> ChemputerValve -> ChemputerVacuum <-(Optional vacuum device)

    Args:
        graph (MultiDiGraph): Graph
        vessel (str): Vessel to get vacuum configuration.

    Returns:
        Dict[str, str]: Dictionary containing node names and ports:
            {
                valve: ,  # Valve connecting vessel and vacuum
                source: ,  # ChemputerVacuum attached to valve
                device: ,  # Optional CVC3000 vacuum device attached to source.
                valve_unused_port: ,  # Unused port on valve.
                valve_inert_gas_port: ,  # Port on valve connected to inert gas.
            }
    """
    valve = source = device = valve_unused_port = valve_inert_gas = None

    for neighbor, neighbor_data in undirected_neighbors(
            graph, vessel, data=True):

        # Find valve
        if not valve and neighbor_data['class'] == 'ChemputerValve':

            for valve_neighbor, valve_neighbor_data in undirected_neighbors(
                    graph, neighbor, data=True):

                # Find vacuum
                if valve_neighbor_data['class'] == 'ChemputerVacuum':

                    # Only assign valve as attached valve connected to vacuum
                    valve = neighbor
                    source = valve_neighbor

                    # Find vacuum device if there.
                    for source_neighbor, source_neighbor_data in\
                            undirected_neighbors(
                                graph, source, data=True):
                        if source_neighbor_data['class'] in VACUUM_CLASSES:
                            device = source_neighbor

                # Find inert gas
                elif valve_neighbor_data['class'] == 'ChemputerFlask':
                    if valve_neighbor_data['chemical'] in INERT_GAS_SYNONYMS:
                        valve_inert_gas = valve_neighbor

    if valve:
        valve_unused_port = get_unused_valve_port(graph, valve)

    return {
        'valve': valve,
        'source': source,
        'device': device,
        'valve_unused_port': valve_unused_port,
        'valve_inert_gas': valve_inert_gas,
    }

def get_buffer_flask(
        graph: MultiDiGraph, vessel: str, return_single=True) -> str:
    """Get buffer flask closest to given vessel.

    Args:
        vessel (str): Node name in graph.

    Returns:
        str: Node name of buffer flask (unused reactor) nearest vessel.
    """
    # Get all reactor IDs
    flasks = [
        flask
        for flask, data in graph_flasks(graph, data=True)
        if not data['chemical']
    ]

    # From remaining reactor IDs, return nearest to vessel.
    if flasks:
        if len(flasks) == 1:
            return flasks[0] if return_single else [flasks[0]]

        # More than one flask
        else:
            shortest_paths = []
            for flask in flasks:
                shortest_paths.append((
                    flask,
                    shortest_path_length(graph, source=vessel, target=flask)
                ))

            if return_single:
                return sorted(shortest_paths, key=lambda x: x[1])[0][0]

            else:
                return [
                    item[0]
                    for item in sorted(shortest_paths, key=lambda x: x[1])
                ]

    return None if return_single else [None, None]


def get_heater_chiller(graph: Dict, node: str) -> Tuple[str, str]:
    """Gets the Heater and Chiller nodes from the graph

    Args:
        graph (Dict): Graph to check
        node (str): Node to check

    Returns:
        Tuple[str, str]: Heater and Chiller
    """

    heater, chiller = None, None

    # Get all neighbors of the node
    neighbors = undirected_neighbors(graph, node)

    # Iterate through each neighbor
    for neighbor in neighbors:
        # Found a heater
        if graph.nodes[neighbor]['class'] in HEATER_CLASSES:
            heater = neighbor

        # Found a chiller
        elif graph.nodes[neighbor]['class'] in CHILLER_CLASSES:
            chiller = neighbor

    return heater, chiller

def get_chiller(graph: MultiDiGraph, vessel: str) -> str:
    """Gets chiller attached to given vessel.

    Args:
        graph (Dict): Graph to check
        node (str): Node to check

    Returns:
        Tuple[str, str]: Heater and Chiller
    """

    chiller = None

    # Get all neighbors of the node
    neighbors = undirected_neighbors(graph, vessel)

    # Iterate through each neighbor
    for neighbor in neighbors:

        # Found chiller
        if graph.nodes[neighbor]['class'] in CHILLER_CLASSES:
            chiller = neighbor

    return chiller

def get_heater(graph: MultiDiGraph, vessel: str) -> str:
    """Gets heater attached to given vessel.

    Args:
        graph (Dict): Graph to check
        node (str): Node to check

    Returns:
        str: Heater node name
    """

    heater = None

    # Get all neighbors of the node
    neighbors = undirected_neighbors(graph, vessel)

    # Iterate through each neighbor
    for neighbor in neighbors:

        # Found heater
        if graph.nodes[neighbor]['class'] in HEATER_CLASSES:
            heater = neighbor

    return heater

def get_nearest_node(
    graph: MultiDiGraph, src: str, target_vessel_class: str
) -> str:
    """Gets the nearest node from the src of target vessel class

    Args:
        graph (MultiDiGraph): Graph to check
        src (str): Node to check
        target_vessel_class (str): Node class to search for

    Raises:
        NetworkXNoPath: Cannot find a path between nodes

    Returns:
        str: Nearest node of vessel class
    """

    # Make graph undirected so actual closest waste vessels are found, not
    # closest in liquid flow path. As long as vessels are all attached to a
    # valve which is attached to a waste vessel this should be fine.
    target_vessels = [
        node for node in graph.nodes()
        if (graph.nodes[node]['class']
            == target_vessel_class)
    ]

    # Make shortest length huge on purpose
    shortest_path_found = 100000
    closest_target_vessel = None

    # Go through each target vessel
    for target_vessel in target_vessels:
        try:
            # Calculate shortest path
            shortest_path_to_target_vessel = shortest_path_length(
                graph, source=src, target=target_vessel
            )

            # Shortest so far, set target vessel to node
            if shortest_path_to_target_vessel < shortest_path_found:
                shortest_path_found = shortest_path_to_target_vessel
                closest_target_vessel = target_vessel

        except NetworkXNoPath:
            pass

    # Return node with the shortest path found
    return closest_target_vessel

def get_vessel_stirrer(graph: Dict, vessel: str) -> Optional[str]:
    """Get any stirrer attached to given vessel
    Heaters can be stirrers in the case of stirrer hot plates

    Args:
        graph (Dict): Graph to search
        vessel (str): Vessel to check

    Returns:
        Optional[str]: Stirrer node, none if not found
    """
    stirrer_neighbors, heater_neighbors = [], []
    stirrer = None
    # Iterate through each neighbor node of the vessel
    for neighbor, data in undirected_neighbors(graph, vessel, data=True):
        # Found a stirrer
        if data['class'] in STIRRER_CLASSES:
            stirrer_neighbors.append(neighbor)

        # Found a heater
        elif data['class'] in HEATER_CLASSES:
            heater_neighbors.append(neighbor)

    # Return first stirrer found
    if stirrer_neighbors:
        stirrer = stirrer_neighbors[0]

    # Return first heater/stirrer found
    elif heater_neighbors:
        stirrer = heater_neighbors[0]

    return stirrer

def get_reagent_vessel(graph: MultiDiGraph, reagent: str) -> Optional[str]:
    """Get vessel containing given reagent.

    Args:
        reagent (str): Name of reagent to find vessel for.

    Returns:
        str: ID of vessel containing given reagent.
    """

    for node, data in graph.nodes(data=True):
        if data['class'] == CHEMPUTER_FLASK:
            if data['chemical'] == reagent:
                return node

    return None

def get_backbone(graph: Dict, ordered: bool = False) -> List[str]:
    """Get list of all valves that have a pump attached.

    Args:
        graph (Dict): Graph to check
        ordered (bool): Order the backbone or not

    Raises:
        XDLError: No backbone found

    Returns:
        List[str]: List of all backbone valves
    """

    backbone = []

    # Iterate through all valves
    for valve in graph_valves(graph):
        has_pump = False

        # Determine if valve has a pump attached
        for _, neighbor_data in undirected_neighbors(graph, valve, data=True):
            if neighbor_data['class'] == CHEMPUTER_PUMP:
                has_pump = True
                break

        # Has a pump, should be in the backbone
        if has_pump:
            backbone.append(valve)

    # Order not important just return
    if not ordered:
        return backbone

    # Order from start to finish
    else:
        # Get the valves at the end of the backbone
        backbone_end_valves = get_backbone_end_valves(graph, backbone)

        # Two valves at the end of the backbone
        if len(backbone_end_valves) == 2:
            start = backbone_end_valves[0]
            end = backbone_end_valves[1]

            # Swap valves
            if graph.nodes[start]['x'] > graph.nodes[end]['x']:
                start = backbone_end_valves[1]
                end = backbone_end_valves[0]

            node = start
            ordered_backbone = [start]

            # Start shifting all valves in order
            while node != end:
                for neighbor in undirected_neighbors(graph, node):
                    if (neighbor in backbone
                            and neighbor not in ordered_backbone):
                        node = neighbor
                        ordered_backbone.append(node)
                        break

            return ordered_backbone

        # Return the valves as only one end
        elif len(backbone_end_valves) == 1:
            return backbone_end_valves

        # No backbone found
        else:
            raise XDLError(
                f'No backbone found.\n\
Backbone end valves: {backbone_end_valves}\n\
Backbone valves: {backbone}.'
            )

def get_backbone_end_valves(graph: Dict, backbone: List[str]) -> List[str]:
    """Get two valves at each end of backbone.

    Args:
        graph (Dict): Graph to search
        backbone (List[str]): List of backbone valves

    Returns:
        List[str]: Valves at each end of the backbone
    """

    backbone_end_valves = []

    if len(backbone) == 1:
        return [backbone[0], backbone[0]]

    # iterate through all backbone valves
    for valve in backbone:
        valve_neighbors = 0

        # Iterate through all neighbors of current valve
        for neighbor, _ in undirected_neighbors(
                graph, valve, data=True):

            # Neighbor is in backbone, increment counter
            if neighbor in backbone:
                valve_neighbors += 1

        # One neighbor, add to end valves
        if valve_neighbors == 1:
            backbone_end_valves.append(valve)

    return backbone_end_valves

def get_waste_vessel(graph: Dict, vessel: str) -> str:
    """Get nearest waste vessel to node.

    Args:
        graph (Dict): Graph to check
        vessel (str): Vessel to check

    Returns:
        str: Waste vessel
    """

    # Get waste vessel from valve
    waste = get_waste_on_valve(graph, vessel)

    # Can't find on valve, get nearest waste
    if not waste:
        waste = get_nearest_node(graph, vessel, CHEMPUTER_WASTE)

    return waste

def get_waste_on_valve(graph: Dict, vessel: str) -> Optional[str]:
    """Get waste vessel connected to backbone valve connected to node. If
    node given is a backbone valve just use that.

    Args:
        graph (Dict): Graph to check
        vessel (str): Vessel to check

    Returns:
        Optional[str]: Waste vessel if found, else None
    """

    # Vessel is valve
    if graph.nodes[vessel]['class'] == CHEMPUTER_VALVE:
        return _waste_on_valve(graph, vessel)

    # Vessel is not valve, find connected valve then find waste.
    else:
        for node, data in undirected_neighbors(graph, vessel, data=True):
            if data['class'] == CHEMPUTER_VALVE:
                waste = _waste_on_valve(graph, node)
                if waste:
                    return waste

    return None

def _waste_on_valve(graph: Dict, valve: str) -> Optional[str]:
    """Used by get_waste_on_valve to get waste connected to given valve.

    Args:
        graph (Dict): Graph to search
        valve (str): Valve to check

    Returns:
        Optional[str]: Waste vessel if found else None
    """

    has_pump = False
    waste = None

    # Iterate through all neighbors of the valve
    for valve_neighbor, valve_neighbor_data in undirected_neighbors(
        graph, valve, data=True
    ):
        # Found a waste vessel
        if valve_neighbor_data['class'] == CHEMPUTER_WASTE:
            waste = valve_neighbor
        elif valve_neighbor_data['class'] == CHEMPUTER_PUMP:
            has_pump = True
        if has_pump and waste:
            return waste

    return None

def get_pump_on_valve(graph: Dict, valve: str) -> Optional[str]:
    """Find pump attached to given valve.

    Args:
        graph (Dict): Graph to search
        valve (str): Valve to check

    Returns:
        Optional[str]: Pump node name if found else None
    """

    # Iterate through all neighbors of the valve
    for valve_neighbor, valve_neighbor_data in undirected_neighbors(
        graph, valve, data=True
    ):
        # Found pump
        if valve_neighbor_data['class'] == CHEMPUTER_PUMP:
            return valve_neighbor

    return None


def get_flush_tube_vessel(graph: Dict, vessel: str) -> Optional[str]:
    """Look for gas vessel to flush tube with after Add steps. Vessel must be on
    the backbone.

    Args:
        graph (Dict): Graph to check
        vessel (str): Vessel to check

    Returns:
        str: Flask to use for flushing tube.
            Preference is nitrogen > air > None.
    """
    inert_gas_flasks, air_flasks = [], []

    # Iterate through all backbone valves
    for valve in get_backbone(graph):
        # Find all vessels that contain inert gas or air
        for neighbor, data in undirected_neighbors(graph, valve, data=True):
            if data['class'] == CHEMPUTER_FLASK:
                if data['chemical'].lower() in INERT_GAS_SYNONYMS:
                    inert_gas_flasks.append(neighbor)

                elif data['chemical'].lower() == AIR:
                    air_flasks.append(neighbor)

    # Inert gas flasks were found
    if inert_gas_flasks:
        # Only one, return
        if len(inert_gas_flasks) == 1:
            return inert_gas_flasks[0]

        # More than one, get the closest one
        else:
            path_lengths = []
            for inert_gas_flask in inert_gas_flasks:
                path_lengths.append((
                    inert_gas_flask,
                    shortest_path_length(
                        graph, inert_gas_flask, vessel
                    )
                ))
            return sorted(path_lengths, key=lambda x: x[1])[0][0]

    # Flasks contianing air found
    elif air_flasks:
        # Only one, return that
        if len(air_flasks) == 1:
            return air_flasks[0]

        # More than one, return the closest one
        else:
            path_lengths = []
            for air_flask in air_flasks:
                path_lengths.append((
                    air_flask,
                    shortest_path_length(
                        graph, air_flask, vessel
                    )
                ))
            return sorted(air_flasks, key=lambda x: x[1])[0][0]

    return None

def get_chempiler(graph: Dict, device_modules: List = []) -> Chempiler:
    """Creates a Chempiler object

    Args:
        graph (Dict): Chempiler graph
        device_modules (List, optional): Device module to load into
                                        the chempiler. Defaults to [].

    Returns:
        Chempiler: Chempiler object
    """

    return Chempiler(
        experiment_code="null",
        output_dir='',
        simulation=True,
        device_modules=[ChemputerAPI, commanduinolabware] + device_modules,
        graph_file=graph
    )

def get_vessel_type(graph: Dict, vessel: str) -> Optional[str]:
    """Gets the type of vessel from the graph

    Args:
        graph (Dict): Graph to check
        vessel (str): Name of the vessel

    Returns:
        Optional[str]: Vessel type, None if not found
    """

    # Get the vessel type
    vessel_class = graph.nodes[vessel]['class']

    # Determine type
    if vessel_class in FILTER_CLASSES:
        return 'filter'
    elif vessel_class in ROTAVAP_CLASSES:
        return 'rotavap'
    elif vessel_class in REACTOR_CLASSES:
        return 'reactor'
    elif vessel_class in SEPARATOR_CLASSES:
        return 'separator'
    elif vessel_class in FLASK_CLASSES:
        return 'flask'

    # Type not found
    return None

def node_in_graph(graph: Dict, node: str) -> bool:
    """Determines if a node is present within the graph

    Args:
        graph (Dict): Graph to check
        node (str): Node to check for

    Returns:
        bool: Node is present in the graph
    """

    return node in graph.nodes()

def get_cartridge(graph: Dict, chemical: str) -> Optional[str]:
    """Get the cartridge from the graph

    Args:
        graph (Dict): Graph to check
        chemical (str): Cartridge to check for

    Returns:
        Optional[str]: Cartridge if found, else None
    """

    for cartridge, data in graph_cartridges(graph, data=True):
        if data['chemical'] == chemical:
            return cartridge

    return None

def graph_flasks(graph, data=False) -> str:
    """Generator to iterate through all ChemputerFlasks in graph.

    Args:
        graph (MultiDiGraph): Graph
        data (bool): Give node data in (node, data) tuple. Defaults to False.

    Yields:
        str: Flask from the graph
    """

    for item in graph_iter_class(graph, CHEMPUTER_FLASK, data=data):
        yield item

def graph_cartridges(graph: Dict, data: bool = False) -> str:
    """Generator to iterate through all ChemputerCartridges in graph.

    Args:
        graph (MultiDiGraph): Graph
        data (bool): Give node data in (node, data) tuple. Defaults to False.

    Yields:
        str: Cartridge from the graph
    """

    for item in graph_iter_class(graph, CHEMPUTER_CARTRIDGE, data=data):
        yield item

def graph_valves(graph: Dict, data: bool = False) -> str:
    """Generator to iterate through all ChemputerValves in graph.

    Args:
        graph (MultiDiGraph): Graph
        data (bool): Give node data in (node, data) tuple. Defaults to False.

    Yields:
        str: Valve from the graph
    """

    for item in graph_iter_class(graph, CHEMPUTER_VALVE, data=data):
        yield item

def graph_filters(graph: Dict, data: bool = False) -> str:
    """Generator to iterate through all ChemputerFilters in graph.

    Args:
        graph (MultiDiGraph): Graph
        data (bool): Give node data in (node, data) tuple. Defaults to False.

    Yields:
        str: Valve from the graph
    """

    for item in graph_iter_class(graph, CHEMPUTER_FILTER, data=data):
        yield item

def graph_wastes(graph: Dict, data: bool = False) -> str:
    """Generator to iterate through all ChemputerWastes in graph.

    Args:
        graph (MultiDiGraph): Graph
        data (bool): Give node data in (node, data) tuple. Defaults to False.

    Yields:
        str: Valve from the graph
    """

    for item in graph_iter_class(graph, CHEMPUTER_WASTE, data=data):
        yield item

def graph_iter_class(
    graph: Dict, target_class: str, data: bool = False
) -> Tuple[str, Dict[str, str]]:
    """Iterates through all classes in the graph

    Args:
        graph (Dict): Graph to check
        target_class (str): Class to check for
        data (bool, optional): Use graph data or not. Defaults to False.

    Yields:
        Tuple[str, Dict[str, str]]: Node and data, or just Node
    """

    for node, node_data in graph.nodes(data=True):
        if node_data['class'] == target_class:
            if data:
                yield node, node_data
            else:
                yield node
