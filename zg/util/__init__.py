"""
Utilities
~~~~~~~~~

Test.
"""

from tempfile import mkstemp
import shutil
from .util import *
from .config import config
import logging

logger = logging.getLogger('zg.util')

def mktemp():
    fd, tempfile = mkstemp('.dl', '', config('client.temp'))
    logger.debug('temporary file created: ' + repr(tempfile))
    return (os.fdopen(fd, 'w'), tempfile)

def cptemp(source):
    """Copies source in a temporary destination."""
    file, tempfile = mktemp()
    file.close()
    shutil.copy(source, tempfile)
    return tempfile



