
import logging
from zg.util import config
from zg.database import Base, engine

def setup():
    logging.config.dictConfig(config('logger'))
    Base.metadata.create_all(engine)

# def teardown():
#     Base.metadata.drop_all(engine)

