"""
Test Image Tasks
"""

from __future__ import division, print_function, absolute_import, unicode_literals
import os
from nose.tools import *
from mock import Mock
from zg.app import celery
from zg.error import NotFound
from zg.util import config, md5file, root, cptemp, mktemp
from zg.task.helpers import TaskMapper
from zg.util.client import URLClient
from zg.task.image import discover
from zg.objects import Item

def test_discover():

    # mock task download:
    # mock = Mock()
    # old_mimetypes = file_mapper.mimetypes
    # file_mapper.mimetypes = [('.*', mock)]

    # tests that jpegs with exif data are 

    tempfile = cptemp(root('test/files/test4.jpg'))

    discover.delay(1, tempfile, mimetype='image/gif', url='http://test')

    eb1964dab6ee752505c905819577cfe3

    #mock.delay.assert_called_once_with(1, tempfile, 'image/jpeg',
    #        url=None, upload=None)

    # file_mapper.mimetypes = old_mimetypes

