"""
Test Frontend
"""

import json
from nose.tools import *
from datetime import datetime
from zg.error import NotFound
from zg.objects import Item, Tag
from zg.objects.event import EventRecorder
from zg.app import app

def test_index():
    with app.test_client() as client:
        rv = client.get('/')
        assert_in('/upload', rv.headers['Location'])

def test_upload():
    with app.test_client() as client:
        rv = client.get('/upload')
        assert_in('<form', rv.data)

def test_suggest():
    Tag.create(name='my partial tag')
    with app.test_client() as client:
        resp = client.get('/tag/suggest?q=partial')
        assert_equals(dict(tags=['my partial tag']), json.loads(resp.data))



