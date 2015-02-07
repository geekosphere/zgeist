
from __future__ import division, print_function, absolute_import, unicode_literals
from zg.objects.event import Event
from zg.objects.service import Service
from .model import TagModel

class Tag(Service):
    __model__ = TagModel

    class event(Service.event):
        assigned = Event()
        unassigned = Event()

    @classmethod
    def suggest(cls, query):
        query = Tag.query()\
            .filter(TagModel.name.ilike('%{}%'.format(query)))\
            .order_by(TagModel.name)\
            .limit(10)
        return Tag.all(query)

