"""
Item Service Tests
"""

from nose.tools import *
from datetime import datetime
from zg.util import config
from zg.error import NotFound
from zg.objects import Item, Tag
from zg.objects.event import EventRecorder

def test_create():
    item = Item.create()

    assert_is_instance(item, Item)
    assert_equal(type(item.id), int)
    assert_is_instance(item.created_at, datetime)
    assert_is_none(item.updated_at)

    item = Item.create(title='title', description='test')

    assert_equal(item.title, 'title')
    assert_equal(item.description, 'test')

def test_created_event():
    rec = EventRecorder(Item.event.created)

    with rec:
        item = Item.create()

    assert_in((item,), rec)

def test_delete():
    item = Item.create()
    id = item.id
    item.delete()
    with assert_raises(NotFound):
        Item.get(id)

def test_deleted_event():
    rec = EventRecorder(Item.event.deleted)
    item = Item.create()
    id = item.id

    with rec:
        item.delete()

    assert_in((id,), rec)

def test_update():
    item = Item.create(title='foo')
    item.update(title='bar')
    assert_is_instance(item.updated_at, datetime)

    assert_equal(item.title, 'bar')

def test_updated_event():
    rec = EventRecorder(Item.event.updated)
    item = Item.create()

    with rec:
        item.update(title='test')

    assert_in((item,), rec)

def test_get():
    item = Item.create()
    item2 = Item.get(item.id)

    assert_is_instance(item2, Item)
    assert_equal(item.id, item2.id)

def test_find_all():
    item = Item.create()
    items = Item.find_all()
    assert len(items) > 0
    assert_in(item.id, map(lambda o: o.id, items))

def test_tagging_assign():
    item = Item.create()
    tag = Tag.find_or_create(name='tag')
    item.tags.assign(tag)

    assert_equals([tag.model], [x.model for x in item.tags])
    assert_equals(len(item.tags), 1)
    assert_in(tag, item.tags)

def test_tagging_assigned_event():
    rec = EventRecorder(Tag.event.assigned)
    item = Item.create()
    tag = Tag.find_or_create(name='tag')

    with rec: item.tags.assign(tag)

    assert_in((item,tag), rec)

def test_tagging_unassign():
    item = Item.create()
    tag = Tag.find_or_create(name='tag')

    item.tags.assign(tag)
    assert_equals(len(item.tags), 1)
    item.tags.unassign(tag)
    assert_equals(len(item.tags), 0)

def test_tagging_unassigned_event():
    rec = EventRecorder(Tag.event.unassigned)
    item = Item.create()
    tag = Tag.find_or_create(name='tag')

    item.tags.assign(tag)
    with rec: item.tags.unassign(tag)

    assert_in((item,tag), rec)


