"""
Image Tasks
"""

from __future__ import division, print_function, absolute_import, unicode_literals
import re
import time
import logging
from zg.util import config, url_valid
from .helpers import TaskMapper
from zg.app import celery
from PIL import Image

logger = logging.getLogger('zg.task.image')

class ImageQuery(object):
    def __init__(self, filename):
        self.img = Image.open(filename)
        self.format = self.img.format
        self.mode = self.img.mode
        self.dimension = self.img.size

    def is_animated(self):
        try:
            self.img.seek(1)
            self.img.seek(0)
            return True
        except:
            return False

    def close(self):
        self.img.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.img.close()

@celery.task
def discover(item_id, tempfile, **data):
    logger.info('discover({}, {}, {}, {})'.format(item_id, tempfile, data))

    # collect image information
    # if ImageQuery
    with ImageQuery(tempfile) as img:
        data['image'] = {
                'animated': img.is_animated(),
                'format':   img.format,   
                'mode':     img.mode,     
                'dimension':img.dimension}
    logger.info('image properties: ' + repr(data['image']))

    # store fragment
    fragment.store.delay(item_id, tempfile, data)

    






