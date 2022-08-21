import contextlib
import logging

import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@contextlib.contextmanager
def request_safety():
    """Log RequestExceptions if any are raised."""
    try:
        yield
    except requests.exceptions.RequestException as e:
        logger.error(f"Error saving detection: {e}")
        raise e
