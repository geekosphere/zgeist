
import os
from nose.tools import *
from mock import Mock
from zg.app import celery
from zg.error import NotFound
from zg.util import config, md5file, root, cptemp, mktemp
from zg.task.helpers import TaskMapper, MockTask
from zg.task.file import file_mapper, discover, validate_file, gen_checksum, gen_cryptohash
from zg.objects import Item

def test_validate_file():
    assert_equal((42360, 'image/jpeg'), validate_file(root('test/files/test1.jpg')))
    assert_equal((None, None), validate_file(root('test/files/test.zip')))
    assert_equal((None, None), validate_file(root('test/files/invalid.exe')))
    assert_equal((None, None), validate_file(root('test/files/2MiBfile')))

def test_discover():
    tempfile = cptemp(root('test/files/test3.gif'))

    # image file delegate to image.discover:
    with MockTask('zg.task.image.discover') as mock:
        discover.delay(1, tempfile)
        mock.assert_called_once_with(1, tempfile, mimetype='image/gif', url=None, upload=None)

    os.remove(tempfile)

