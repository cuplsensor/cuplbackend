# -*- coding: utf-8 -*-
"""
    web.locations.forms

    Location forms
"""

from flask_wtf import Form
from wtforms import StringField, IntegerField, SubmitField, HiddenField
from wtforms.widgets import HiddenInput
from wtforms.validators import DataRequired, ValidationError, Length
from ..services import locations

__all__ = ['AddLocationForm', 'EditLocationForm']

class AddLocationForm(Form):
    description = StringField('description', validators=[DataRequired(), Length(min=1, max=50)])
    capturesample_id = IntegerField('capturesample_id', widget=HiddenInput(), validators=[DataRequired()])
    submit = SubmitField('Add')

class EditLocationForm(Form):
    description = StringField('description', validators=[DataRequired(), Length(min=1, max=50)])
    location_id = IntegerField('location_id', widget=HiddenInput(), validators=[DataRequired()])
    submit = SubmitField('Add')
