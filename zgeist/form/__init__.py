# -*- coding: utf-8 -*-

import re

from flask_wtf import Form
from wtforms import Field, Form, TextAreaField, FileField, BooleanField
from wtforms.widgets import TextArea
from wtforms.validators import required, ValidationError

class ListField(Field):
    widget = TextArea()

    def _value(self):
        if self.data:
            return u'\n'.join(self.data)
        else:
            return u''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [x.strip() for x in re.split(r'\s+', valuelist[0])]
        else:
            self.data = []

from .item import CreateForm

