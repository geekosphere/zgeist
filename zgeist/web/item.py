# -*- coding: utf-8 -*-

from flask import Response, Blueprint, g, jsonify, abort, request,\
    redirect, render_template, url_for, session
from flask_wtf import Form
from wtforms import *
from wtforms.validators import *

from sqlalchemy.sql import func

from functools import wraps
from math import ceil
import datetime
import pytz
import json
import logging

import zgeist.task as task
from zgeist.util import is_valid_url

logger = logging.getLogger('zgeist.web')
bp = Blueprint('item', __name__, template_folder='templates')

class CreateForm(Form):
    def valid_url_check(form, field):
        for url in field.data.split('\n'):
            if not is_valid_url(url):
                raise ValidationError('Invalid URL!')
    urls = TextAreaField(u'URL(s)', validators=[required(), valid_url_check])

@bp.route('/item/create', methods=['GET', 'POST'])
def create():
    form = CreateForm(request.form)
    if request.method == 'POST' and form.validate():
        pass
    return render_template('item/create.html', form=form)


