"""
Database Initialization
"""

from __future__ import division, print_function, absolute_import, unicode_literals
import pytz
from sqlalchemy import create_engine, DateTime, TypeDecorator
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from zg.util import config

# engine = create_engine(config('database.uri'), convert_unicode=True, echo=config('database.echo'))
engine = create_engine(config('database.uri'))
# session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = session.query_property()

"""
def create_all():
    #global engine, session, Base
    #engine = create_engine(config('database.uri'), convert_unicode=True,
    #        echo=config('database.echo'))
    #session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    #Base = declarative_base()
    #Base.query = session.query_property()
    Base.metadata.create_all(engine) 
    #session.commit()

def drop_all():
    session.commit()
    session.remove()
    engine.close()
    Base.metadata.drop_all(engine) 
"""

class UTCDateTime(TypeDecorator):
    impl = DateTime
    def process_result_value(self, value, engine):
        return pytz.utc.localize(value) if value else value

    def process_bind_param(self, value, engine):
        return value

