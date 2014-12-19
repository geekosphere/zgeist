# -*- coding: utf-8 -*-

from flask import Response, Blueprint, g, jsonify, abort, request,\
    redirect, render_template, url_for, session

from sqlalchemy.sql import func

from functools import wraps
from math import ceil
import datetime
import pytz
import json
import logging

import zgeist.task as task

logger = logging.getLogger('zgeist.web')
bp = Blueprint('public', __name__, template_folder='templates')

@bp.route('/')
def index():
    logger.info('index route')
    #task.url.discover.delay({})
    return render_template('index.html')

