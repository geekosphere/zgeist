"""
"""

from __future__ import division, print_function, absolute_import, unicode_literals
from zg.objects.service import Service, ManyMapping
from zg.objects.tag.service import Tag
from .model import ItemModel

class Tagging(ManyMapping):
    __service__ = Tag
    __collection__ = 'tags'

class ItemStatus(object):
    pending = 'pending'
    failed = 'failed'
    available = 'available'

# item.status = 'pendig'  => exceptioN!!1

class Item(Service):
    __model__ = ItemModel

    def __init__(self, model):
        super(Item, self).__init__(model)
        #self.tags = ManyMapping(self, Tag, 'tags')
        self.tags = Tagging(self)


