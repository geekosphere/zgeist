
import datetime

from sqlalchemy import Column, Integer, String

from zgeist.model import Base, UTCDateTime

class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    created_at = Column(UTCDateTime, default=datetime.datetime.utcnow)
    updated_at = Column(UTCDateTime, default=None)


