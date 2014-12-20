# -*- coding: utf-8 -*-

import re

from flask_wtf import Form
from wtforms import Form, TextAreaField, StringField, FileField, BooleanField
from wtforms.validators import required, ValidationError

import zgeist.util as util
from . import ListField

class CreateForm(Form):
    def valid_url_check(form, field):
        #for url in re.split(r'\s+', field.data):
        #    if not util.is_valid_url(url):
        #        raise ValidationError('This URL is invalid: {}'.format(url))
        for url in field.data:
            if not util.is_valid_url(url):
                raise ValidationError('This URL is invalid: {}'.format(url))
    urls = ListField(u'urls', validators=[required(), valid_url_check])
    upload = FileField(u'upload')
    title = StringField(u'title')
    description = TextAreaField(u'description')
    group = BooleanField(u'group')
    irc_announce = BooleanField(u'announce')

