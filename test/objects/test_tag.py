"""
Tag Service Tests
"""

from nose.tools import *
from datetime import datetime
from zg.error import NotFound
from zg.objects import Item, Tag
from zg.objects.event import EventRecorder

def test_tag_find_or_create():
    tag = Tag.find_or_create(name='tag')

    assert_equals(type(tag.id), int)
    assert_equals(tag.name, 'tag')

