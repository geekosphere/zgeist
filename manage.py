# -*- coding: utf-8 -*-

import logging

from flask.ext.script import Manager

from zgeist import create_app, app, celery
from zgeist.model import Item

logger = logging.getLogger('zgeist.manage')

manager = Manager(create_app())

if __name__ == "__main__":
    manager.run()

