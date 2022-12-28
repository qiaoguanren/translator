from ..utils.logging import get_logger

# Should match, '1', '11', '1.1', '1.01', '13.12' etc.
float_regex: str = r'([0-9]+([.][0-9]+)?)'

def parse_bool(s: str) -> bool:
    """Parse string for bool."""
    if s.strip().lower() in ['true', '1']:
        return True
    elif s.strip().lower() in ['false', '0']:
        return False
    return None

def read_file(file_name: str) -> str:
    """Read file, allowing for different encodings caused by Windows.
    Assumes existence of file etc has already been checked, just here to read.

    Args:
        file_name (str): File to read.

    Returns:
        str: Contents of file.
    """
    try:
        with open(file_name, encoding='utf8') as fileobj:
            contents = fileobj.read()
    except UnicodeDecodeError:
        # Try different encoding to UTF-8
        logger = get_logger()
        logger.debug('Unable to decode file using UTF-8.\
 Falling back to ISO-8859-1')

        with open(file_name, encoding='iso-8859-1') as fileobj:
            contents = fileobj.read()

    return contents
