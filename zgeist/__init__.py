# -*- coding: utf-8 -*-

import os
import logging.config

from .util import ConfigAccessor

from celery import Celery
from flask import Flask, g, redirect
from flask_wtf.csrf import CsrfProtect
from flask.ext.assets import Environment, Bundle
from flask.ext.mail import Mail
from webassets.filter import get_filter

env = os.environ.get('ENV', 'development')

config = ConfigAccessor('test/test.yaml' if env == 'test' else 'local.yaml')

logging.config.dictConfig(config['logger'])

app = None
mail = Mail()
celery = Celery('zgeist')
celery.conf.update(config['celery'])

import zgeist.task

def create_app():
    global app, mail

    app = Flask('zgeist', **config['app'])
    app.config.update(config['flask'])
    mail.init_app(app)

    CsrfProtect(app)

    assets = Environment(app)
    assets.url = app.static_url_path
    assets.register('main_css', Bundle('main.scss', filters='pyscss,cssmin', output='main.min.css'))

    from .web import register_all_blueprints
    register_all_blueprints(app)

    return app

