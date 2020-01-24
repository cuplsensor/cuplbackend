# -*- coding: utf-8 -*-
"""
    web.log.forms

    Log forms
"""

from flask_wtf import Form
from flask_wtf.html5 import IntegerField, SearchField
from wtforms import StringField, HiddenField, TextField, SubmitField, SelectField, DecimalField
from wtforms.validators import DataRequired
from ..baseform import RedirectForm

__all__ = []
