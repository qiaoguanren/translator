import logging

def get_logger():
    logger = logging.getLogger('xdl')
    if not logger.hasHandlers():
        # logger.addHandler(get_info_handler())
        logger.addHandler(get_debug_handler())
    return logger

def get_info_handler():
    info_handler = logging.StreamHandler()
    info_formatter = logging.Formatter('XDL: %(message)s')
    info_handler.setFormatter(info_formatter)
    info_handler.setLevel(logging.INFO)
    return info_handler

def get_debug_handler():
    debug_handler = logging.StreamHandler()
    debug_formatter = logging.Formatter('XDL: %(message)s')
    debug_handler.setFormatter(debug_formatter)
    debug_handler.setLevel(logging.DEBUG)
    return debug_handler
