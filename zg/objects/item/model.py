"""
Item Model
"""

from __future__ import division, print_function, absolute_import, unicode_literals
from sqlalchemy import Table, ForeignKey, Column, Integer, String, Text
from sqlalchemy.orm import relationship
from zg.database import Base, UTCDateTime
from zg.objects.tag.model import TagModel

TaggingModel = Table('tagging', Base.metadata,
    Column('item_id', Integer, ForeignKey('item.id')),
    Column('tag_id', Integer, ForeignKey('tag.id')))

class ItemModel(Base):
    __tablename__ = 'item'

    id          = Column(Integer, primary_key=True)

    title       = Column(String(2048))
    description = Column(Text)

    created_at  = Column(UTCDateTime, nullable=False)
    updated_at  = Column(UTCDateTime)

    tags        = relationship('TagModel', secondary=TaggingModel)

    #: item stauts either pending, failed or available
    status      = Column(String(32))





