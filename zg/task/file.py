"""
File Tasks
"""

from __future__ import division, print_function, absolute_import, unicode_literals
import re
import os
import time
import logging
import magic
from zg.util import config, url_valid, md5file, sha512file, to_bytes
from .helpers import TaskMapper
from zg.app import celery
from zg.task import image

logger = logging.getLogger('zg.task.file')

file_mapper = TaskMapper()

def gen_checksum(filename):
    return md5file(filename)

def gen_cryptohash(filename):
    return sha512file(filename)

def validate_file(tempfile):
    if not os.path.isfile(tempfile):
        logger.info('tempfile validation failure: no tempfile')
        return (None, None)

    max_size = to_bytes(config('upload.max_size'))
    filesize = os.path.getsize(tempfile)
    if filesize > max_size:
        logger.info('tempfile validation failure: tempfile is too large!')
        return (None, None)

    ma = magic.Magic(mime=True)
    mimetype = ma.from_file(tempfile)
    if mimetype not in config('upload.accept_mimetypes'):
        logger.info('tempfile validation failure: mimetype not allowed!')
        return (None, None)

    return (filesize, mimetype)

@celery.task
def discover(item_id, tempfile, **data):
    """Discover a local file."""
    url = data.pop('url', None)
    upload = data.pop('upload', None)
    try:
        filesize, mimetype = validate_file(tempfile)
        if not filesize: raise Exception('tempfile validation failure')
        task = file_mapper.get_task_for_mimetype(mimetype)
        if not task: raise Exception('no applicable task found!')
        task.delay(item_id, tempfile, mimetype=mimetype, url=url, upload=upload)
    except Exception as e:
        logger.error('file discover failure: ' + str(e))
        logger.error(e)
        os.remove(tempfile)
        logger.debug('temporary file deleted: ' + tempfile)

file_mapper.by_mimetype('image/*')(image.discover)
"""
@celery.task
@file_mapper.by_mimetype('image/*')
def image_dispatch(item_id, tempfile, **data):
    image.discover.delay(item_id, tempfile, **data)
"""
    

