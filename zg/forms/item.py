"""
"""

from __future__ import division, print_function, absolute_import, unicode_literals
import re
import logging
from flask import request
from wtforms import Form, TextAreaField, StringField, FileField, BooleanField
from wtforms.validators import optional, required, ValidationError
from zg.util import url_valid
from zg.forms import ListFieldTextArea, ListFieldInput

log = logging.getLogger('zg.form')

class CreateForm(Form):
    def valid_url_check(form, field):
        for url in field.data:
            if not valid_url(url):
                raise ValidationError('This URL is invalid: {}'.format(url))

        log.info('urls field {}, upload field {}'.format(len(field.data), len(request.files)))
        log.info(request.files['upload'])

        # make sure either a url or a file is present:
        if len(field.data) == 0 and not CreateForm.get_upload().filename:
            raise ValidationError('Missing URL or File Upload!')

    urls         = ListFieldTextArea(u'URLs', validators=[valid_url_check])
    upload       = FileField(u'File Upload')
    title        = StringField(u'Title')
    description  = TextAreaField(u'Description')
    tags         = ListFieldInput(u'Comma-seperated Tags', seperator=r',', joiner=u', ')
    group        = BooleanField(u'Group')
    irc_announce = BooleanField(u'Announce in IRC')

    @staticmethod
    def get_upload():
        return request.files['upload']

