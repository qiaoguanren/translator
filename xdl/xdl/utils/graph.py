from typing import Union, Dict, Optional
import os
import json
from networkx.readwrite import json_graph
from networkx import MultiDiGraph, read_graphml, relabel_nodes

from typing import List
from ..errors import (
    XDLGraphFileNotFoundError,
    XDLGraphInvalidFileTypeError,
    XDLGraphTypeError,
)

FILTER: str = 'ChemputerFilter'
REACTOR: str = 'ChemputerReactor'
CARTRIDGE: str = 'ChemputerCartridge'
WASTE: str = 'ChemputerWaste'
FLASK: str = 'ChemputerFlask'
VACUUM: str = 'ChemputerVacuum'
SEPARATOR: str = 'ChemputerSeparator'
VALVE: str = 'ChemputerValve'
PUMP: str = 'ChemputerPump'

JULABO_CF41: str = 'JULABOCF41'
HUBER_PETITE_FLEUR: str = 'Huber'
IKA_RCT_DIGITAL: str = 'IKARCTDigital'
IKA_RET_CONTROL_VISC: str = 'IKARETControlVisc'
IKA_RV_10 = "IKARV10"
CVC3000 = "CVC3000"
IKA_MICROSTAR_75 = "IKAmicrostar75"
RZR_2052 = "RZR_2052"
HEIDOLPH_TORQUE_100 = "HeiTORQUE_100"


HEATER_CLASSES: List[str] = [IKA_RCT_DIGITAL, IKA_RET_CONTROL_VISC]
CHILLER_CLASSES: List[str] = [
    JULABO_CF41, HUBER_PETITE_FLEUR]

ROTAVAP_CLASSES: List[str] = [IKA_RV_10]
VACUUM_CLASSES: List[str] = [CVC3000]
STIRRER_CLASSES: List[str] = [IKA_MICROSTAR_75, RZR_2052, HEIDOLPH_TORQUE_100]
FILTER_CLASSES: List[str] = [FILTER]
REACTOR_CLASSES: List[str] = [REACTOR]
SEPARATOR_CLASSES: List[str] = [SEPARATOR]
FLASK_CLASSES: List[str] = [FLASK]

def undirected_neighbors(graph, node, data=False):
    """Return all neighbors whether they come from in edges or out edges.

    Args:
        graph (MultiDiGraph): Graph to find neighbors in.
        node (str): Node in graph to find neighbors of.
        data (bool): If True, also return neighbor properties. This replicates
            the way that networkx graph.nodes(data=True) works.

    Yields:
        (str, Optional[Dict]): If data is False, yields node name. If data is
           True, yields (node_name, node_properties).
    """
    yielded_neighbors = []
    for src, dest in graph.edges():
        if src == node and dest not in yielded_neighbors:
            yielded_neighbors.append(dest)
            if data:
                yield dest, graph.nodes[dest]
            else:
                yield dest

        elif dest == node and src not in yielded_neighbors:
            yielded_neighbors.append(src)
            if data:
                yield src, graph.nodes[src]
            else:
                yield src

def get_graph(graph_file: Union[str, Dict]) -> MultiDiGraph:
    """Given one of the args available, return a networkx Graph object.

    Args:
        graph_file (str, optional): Path to graph file. May be GraphML file,
            JSON file with graph in node link format, or dict containing graph
            in same format as JSON file.

    Returns:
        networkx.classes.multidigraph: MultiDiGraph object.
    """
    graph = None

    # Graph file is file path
    if type(graph_file) == str:

        # Graph file doesn't exist
        if not os.path.exists(graph_file):
            raise XDLGraphFileNotFoundError(graph_file)

        # Graphml file
        if graph_file.lower().endswith('.graphml'):
            graph = MultiDiGraph(read_graphml(graph_file))
            name_mapping = {}
            for node in graph.nodes():
                name_mapping[node] = graph.nodes[node]['label']
            graph = relabel_nodes(graph, name_mapping)

        # JSON graph file
        elif graph_file.lower().endswith('.json'):
            with open(graph_file) as fileobj:
                json_data = json.load(fileobj)
                graph = json_graph.node_link_graph(
                    json_data, directed=True, multigraph=True)

        # Invalid file type, raise error
        else:
            raise XDLGraphInvalidFileTypeError(graph_file)

    # Graph supplied as dict loaded from JSON graph file
    elif type(graph_file) == dict:
        graph = json_graph.node_link_graph(
            graph_file, directed=True, multigraph=True)

    # Graph supplied directly as MultiDiGraph, return unchanged.
    elif type(graph_file) == MultiDiGraph:
        graph = graph_file

    # Invalid value passed as graph_file, raise error
    else:
        raise XDLGraphTypeError(graph_file)

    # Convert port strings to lists, '(0,1)' -> ['0', '1']
    for edge in graph.edges:
        if 'port' in graph.edges[edge]:
            port_str = graph.edges[edge]['port']
            if type(port_str) == str:
                graph.edges[edge]['port'] = port_str[1:-1].split(',')

    return graph

def get_reagent_vessel(graph: MultiDiGraph, reagent: str) -> Optional[str]:
    """Get vessel containing given reagent.

    Args:
        reagent (str): Name of reagent to find vessel for.

    Returns:
        str: node name of vessel containing given reagent.
    """

    for node, data in graph.nodes(data=True):
        if data['class'] == FLASK:
            if data['chemical'] == reagent:
                return node
    return None

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
