"""
"""

from __future__ import division, print_function, absolute_import, unicode_literals
from wtforms.widgets import TextArea, TextInput, HiddenInput
from wtforms import Field

class ListField(Field):
    def __init__(self, *args, **kwargs):
        self._seperator = kwargs['seperator'] if 'seperator' in kwargs else r'\s+'
        self._joiner = kwargs['joiner'] if 'joiner' in kwargs else u'\n'

        kwargs = {k: v for k, v in kwargs.items() if k not in ('seperator', 'joiner')}

        Field.__init__(self, *args, **kwargs)

    def _value(self):
        if self.data:
            return self._joiner.join(self.data)
        else:
            return u''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [x.strip() for x in re.split(self._seperator, valuelist[0]) if x.strip() != '']
        else:
            self.data = []

class ListFieldTextArea(ListField):
    widget = TextArea()

class ListFieldInput(ListField):
    widget = TextInput()

class ListFieldHidden(ListField):
    widget = HiddenInput()

