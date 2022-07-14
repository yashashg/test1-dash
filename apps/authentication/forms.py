# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField
from wtforms.validators import Email, DataRequired,Length

# login and registration


class LoginForm(FlaskForm):
    email = StringField('Email',
                         id='email_login',
                         validators=[DataRequired()])
    password = PasswordField('Password',
                             id='pwd_login',
                             validators=[DataRequired()])


class CreateAccountForm(FlaskForm):
    email = StringField("email", validators=[Email()])
    password = PasswordField("password", validators=[Length(min=5)])
    repeat_password = PasswordField("repated_password", validators=[Length(min=5)])
    fullname = StringField("fullname" , validators = [DataRequired()])
    phone = StringField('phone', validators=[DataRequired()])
    company = StringField('company', validators=[DataRequired()])


class Update(FlaskForm):
    avatar = RadioField('Label', choices=[('value','description'),('value_two','whatever')])
