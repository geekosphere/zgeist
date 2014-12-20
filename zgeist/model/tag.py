
import datetime

from sqlalchemy import Column, Integer, String

from zgeist.model import Base, UTCDateTime

class Tag(Base):
    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True)

    name = Column(String(255), unique=True, nullable=True)

    created_at = Column(UTCDateTime, default=datetime.datetime.utcnow)
    updated_at = Column(UTCDateTime, default=None)

