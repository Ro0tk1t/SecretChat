#!/usr/bin/env python
# coding=utf-8

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import DataRequired, Length, EqualTo
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, HiddenField, FormField


class LoginForm(FlaskForm):
    username = StringField('Username', [DataRequired(), Length(max=20)])
    password = PasswordField('Password', [DataRequired()])
    remember = BooleanField('Remember Me')


class RegistForm(FlaskForm):
    username = StringField('Username', [DataRequired(), Length(max=20)])
    password = PasswordField('Password', [DataRequired()])
    password1 = PasswordField('Password1', [DataRequired()])
    agree = BooleanField('Agree')
    nikename = StringField('Nikename')
    email = StringField('Email')
    phone = StringField('Phone')

    def validate_pwd(self):
        return self.password.data == self.password1.data

    def agreed(self):
        return self.agree


class ContentForm(FlaskForm):
    content = TextAreaField('Content', [DataRequired()])


class UploadForm(FlaskForm):
    file = FileField('File', [FileRequired()])


class MessageForm(FlaskForm):
    send2 = HiddenField('Send2', [DataRequired()])
    content = FormField(ContentForm)
    upload = FormField(UploadForm)
