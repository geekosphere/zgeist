"""
Application Routes
"""

from __future__ import division, print_function, absolute_import, unicode_literals
from flask import url_for, redirect
from zg.util import config
from zg.app import app
from .frontend import frontend

app.register_blueprint(frontend)

@app.template_global('config')
def get_config_global(*args):
    return config(*args)

@app.route('/')
def index():
    return redirect(url_for('frontend.upload'))


