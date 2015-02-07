"""
Test Task Helpers Utilities
"""

import os
from nose.tools import *
from mock import Mock
from zg.util import md5file
from zg.task.helpers import TaskMapper

def test_task_mapper():
    tm = TaskMapper()

    mock = Mock()
    tm.by_pattern(r'test_\d.jpeg')(mock.pattern)
    tm.by_domain('example.com')(mock.domain)
    tm.by_mimetype('image/*')(mock.mimetype)

    # test task mapper get_task_by_*
    assert_equal(mock.pattern, tm.get_task_by_pattern('http://example.com/test_1.jpeg'))
    assert_equal(mock.domain, tm.get_task_by_domain('http://example.com/test_1.jpeg'))
    assert_equal(mock.mimetype, tm.get_task_by_mimetype('image/jpeg'))
    assert_equal(None, tm.get_task_by_pattern('http://example.com/test.jpeg'))
    assert_equal(None, tm.get_task_by_domain('http://example2.com/test_1.jpeg'))
    assert_equal(None, tm.get_task_by_mimetype('video/webm'))

    # tests get_task_for_url
    assert_equal(None, tm.get_task_for_url('http://example2.com/test.jpeg'))
    assert_equal(mock.pattern, tm.get_task_for_url('http://example2.com/test_1.jpeg'))
    assert_equal(mock.mimetype, tm.get_task_for_mimetype('image/jpeg'))

    # search order: pattern, domain (this test url matches for both domain and pattern)
    assert_equal(mock.pattern, tm.get_task_for_url('http://example.com/test_1.jpeg'))
