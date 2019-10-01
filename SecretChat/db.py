#!/usr/bin/env python
# coding=utf-8

from flask import Flask
from flask_mongoengine import MongoEngine
from flask_sqlalchemy import SQLAlchemy
from flask_login import AnonymousUserMixin
from datetime import datetime


app = Flask('Chat')
app.config.from_pyfile('app.config')

db = SQLAlchemy(app)
mongo = MongoEngine(app)


class User(mongo.Document):
    id = mongo.IntField(primary_key=True, required=True, default=1)
    username = mongo.StringField(required=True, unique=True, default='admin')
    password = mongo.StringField(required=True, default='123456')
    nikename = mongo.StringField(default='Mr. null')
    last_online = mongo.DateTimeField(default=datetime.now())
    phone = mongo.StringField()
    email = mongo.EmailField()

    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        return True

    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User:  %r>' % self.username


class Message(mongo.Document):
    create = mongo.DateTimeField(required=True, default=datetime.now())
    create_by = mongo.ObjectIdField(required=True)
    content = mongo.StringField(required=True)
    send2 = mongo.ObjectIdField(required=True)


class Group(mongo.EmbeddedDocument):
    create = mongo.DateTimeField(default=datetime.now())
    users = mongo.ListField(mongo.EmbeddedDocumentField('User'))
