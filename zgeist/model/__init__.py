# -*- coding: utf-8 -*-

import datetime

import pytz
from sqlalchemy import create_engine, Table, Column, ForeignKey, Integer, String, Text, Boolean, DateTime, TypeDecorator
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

from zgeist import config

engine = create_engine(config['database.uri'], convert_unicode=True)
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = session.query_property()

class UTCDateTime(TypeDecorator):
    impl = DateTime
    def process_result_value(self, value, engine):
        return pytz.utc.localize(value) if value else value

    def process_bind_param(self, value, engine):
        return value

from .item import Item
from .tag import Tag

