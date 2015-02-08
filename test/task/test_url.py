"""
Test Url Tasks
"""

from __future__ import division, print_function, absolute_import, unicode_literals
from nose.tools import *
from mock import Mock
from zg.error import NotFound
from zg.util import config, md5file
from zg.task.helpers import MockTask
from zg.task.url import discover, generic, download, url_mapper
from zg.objects import Item
import os

def test_discover():
    with MockTask('zg.task.url.generic') as mock:
        discover.delay(1, 'http://example.com/test_1.jpeg')
        mock.assert_called_once_with(1, 'http://example.com/test_1.jpeg')

    with MockTask('zg.task.url.generic') as mock:
        discover.delay(1, 'httpX://invalid_url/')
        assert(not mock.called)

def test_generic():
    with MockTask('zg.task.url.download') as mock:
        generic.delay(1, 'http://apoc.cc/test/img/test1.jpg')
        mock.assert_called_once_with(1, 'http://apoc.cc/test/img/test1.jpg')

    with MockTask('zg.task.url.download') as mock:
        generic.delay(1, 'http://apoc.cc/test/img/')
        assert(not mock.called)

def test_download():
    with MockTask('zg.task.file.discover') as mock:
        url = 'http://apoc.cc/test/img/test1.jpg'
        download.delay(1, url)
        (item_id, tempfile), data = mock.call_args
        mock.assert_called_once_with(1, tempfile, url=url)
        os.remove(tempfile)


