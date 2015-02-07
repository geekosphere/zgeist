"""
Flask Application Initialization
"""

from __future__ import division, print_function, absolute_import, unicode_literals
from flask import Flask
from flask_wtf.csrf import CsrfProtect
from flask.ext.assets import Environment, Bundle
from flask.ext.mail import Mail
from celery import Celery
from webassets.filter import get_filter
from .util import root, config, DictAssetLoader

#: Flask application instance
app = Flask('zg', **config('app'))
app.config.update(config('flask'))

#: Celery instance
celery = Celery('zg-celery')
celery.conf.update(config('celery'))

#: Flask mail instance
mail = Mail()

CsrfProtect(app)

assets = Environment(app)
assets.url = ''
assets.directory = root('./public')
assets.load_path = [app.static_folder, root('./bower_components')]
assets.register(DictAssetLoader(config('assets')).load_bundles(assets))

import zg.routes

