# -*- coding: utf-8 -*-
"""
    web.tags.forms

    Tag forms
"""

from flask_wtf import Form
from wtforms import StringField, TextField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError, Length
from ..services import tags


__all__ = ['AddTagForm', 'SelectTagForm']

class TagExists(object):
    def __init__(self, message=None):
        if not message:
            message = u'Tag with this serial does not exist.'
        self.message = message

    def __call__(self, form, field):
        tagserial = field.data
        tagobj = tags.get_by_serial(tagserial)
        if tagobj is None:
            raise ValidationError(self.message)


# Form for the campaign page
class AddTagForm(Form):
    submit = SubmitField('Add')

class SelectTagForm(Form):
    serial = StringField('serial', validators=[DataRequired(), TagExists(), Length(min=6, max=6)])
    submit = SubmitField('Add')
