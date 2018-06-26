# coding: utf-8

"""
forms.py  password表单
~~~~~~~~~~~~~~~~~~~~~

"""

from flask_wtf import FlaskForm
from wtforms import PasswordField,SubmitField
from wtforms.validators import DataRequired


class Form(FlaskForm):
    password=PasswordField("Enter  password",validators=[DataRequired()])
    submit=SubmitField('Submit')