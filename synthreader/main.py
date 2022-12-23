from typing import Optional
import logging
from .tagging import tag_synthesis
from .interpreting import extract_actions
from .finishing import action_list_to_xdl #有一个chempiler下不下来
from .logging import get_logger
from xdl.utils.graph import get_graph

def text_to_xdl(synthesis_text: str, save_file: Optional[str] = None) -> str:
    """Convert synthesis text to XDL file of procedure described.

    Args:
        synthesis_text (str): Description of synthetic procedure.
        save_file (str): File path to save XDL to. Optional.

    Returns:
        str: Raw XDL str of synthesis text interpretation.
    """
    logger = get_logger()
    logger.setLevel(logging.INFO)
    logger.info('Tagging entities in text...')
    labelled_text = tag_synthesis(synthesis_text)
    print(labelled_text)
    logger.info('Extracting actions from tagged text...')
    action_list = extract_actions(labelled_text)
    print(action_list)
    logger.info('Converting actions to XDL...')
    G = get_graph("D://HSZD//ChemputerAntiviralXDL-master//Arbidol//XDL//Step1//graph.json")
    #print(G)
    xdl = action_list_to_xdl(action_list)
    if save_file:
        xdl.save(save_file)
        logger.info(f'Saved to {save_file}')
    return xdl
