# -*- coding: utf-8 -*-
"""
    web.users.forms

    User forms
"""

from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired

__all__ = ['NewUserForm']

# Form to create a new user
class NewUserForm(Form):
    oauth_id = TextField('oauth_id', validators=[DataRequired()])
    email = TextField('email', validators=[DataRequired()])
    first_name = TextField('first_name', validator=[DataRequired()])
    last_name = TextField('last_name', validator=[DataRequired()])
    locale = TextField('locale', validator=[DataRequired()])
