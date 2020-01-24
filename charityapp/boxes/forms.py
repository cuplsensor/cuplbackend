# -*- coding: utf-8 -*-
"""
    web.boxes.forms

    Box forms
"""

from flask_wtf import Form
from wtforms import StringField, TextField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError, Length
from ..services import boxes


__all__ = ['AddBoxForm', 'SelectBoxForm']

class BoxExists(object):
    def __init__(self, message=None):
        if not message:
            message = u'Box with this serial does not exist.'
        self.message = message

    def __call__(self, form, field):
        boxserial = field.data
        boxobj = boxes.get_by_serial(boxserial)
        if boxobj is None:
            raise ValidationError(self.message)


# Form for the campaign page
class AddBoxForm(Form):
    submit = SubmitField('Add')

class SelectBoxForm(Form):
    serial = StringField('serial', validators=[DataRequired(), BoxExists(), Length(min=6, max=6)])
    submit = SubmitField('Add')
