
import datetime

from sqlalchemy import Column, Integer, String, Text

from zgeist.model import session, Base, UTCDateTime

class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)

    title = Column(String(2048))
    description = Column(Text)

    created_at = Column(UTCDateTime, default=datetime.datetime.utcnow)
    updated_at = Column(UTCDateTime, default=None)

    @staticmethod
    def create(title, description):
        item = Item(title=title, description=description)
        session.add(item)
        session.commit()
        return item



