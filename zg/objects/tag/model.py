"""
Item Tag Model
"""

from __future__ import division, print_function, absolute_import, unicode_literals
from sqlalchemy import Column, Integer, String, Text
from zg.database import Base, UTCDateTime

class TagModel(Base):
    __tablename__ = 'tag'

    id         = Column(Integer, primary_key=True)

    name       = Column(String(2048), nullable=False)

    created_at = Column(UTCDateTime, nullable=False)
    updated_at = Column(UTCDateTime)

