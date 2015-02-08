"""
Fragment Tasks
"""

from __future__ import division, print_function, absolute_import, unicode_literals
import re
import time
import logging
from zg.util import config
from zg.app import celery

logger = logging.getLogger('zg.task.fragment')

@celery.task
def store(item_id, tempfile, data):


