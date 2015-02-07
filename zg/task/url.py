"""
Url Tasks
"""

from __future__ import division, print_function, absolute_import, unicode_literals
import logging
import requests
import os
import re
from zg.util import config, to_bytes, format_bytes, mktemp, url_valid
from zg.util.client import URLClient
from .helpers import TaskMapper
from zg.app import celery
from zg.task import file

logger = logging.getLogger('zg.task.url')

url_mapper = TaskMapper()

@celery.task
def discover(item_id, urls):
    """Delegates urls by domain or pattern matching."""
    logger.info('discover(item: {}, urls: {})'.format(item_id, urls))

    for url in urls:
        # ensure url validity
        if not url_valid(url): continue

        # continue with generic or url specific task
        (url_mapper.get_task_for_url(url) or generic).delay(item_id, url)

@celery.task
def generic(item_id, url):
    """Determines the mimetype of a url."""
    logger.info('generic(item: {}, url: {})'.format(item_id, url))

    # loads the first few bytes to discover the magic number
    mimetype = URLClient(url).discover()

    if mimetype in config('upload.accept_mimetypes'):
        download.delay(item_id, url)

@celery.task
def download(item_id, url):
    """Download a url and delegate to file.discover."""
    logger.info('download(item: {}, url: {})'.format(item_id, url))

    tempfile = URLClient(url).download()
    if tempfile:
        file.discover.delay(item_id, tempfile, url=url)


