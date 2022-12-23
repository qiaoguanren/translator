import logging

def get_logger():
    logger = logging.getLogger('synthreader')
    if not logger.hasHandlers():
        logger.addHandler(get_handler())
    return logger

def get_handler():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('SynthReader: %(message)s')
    handler.setFormatter(formatter)
    return handler
