# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin

from apps import db, login_manager

from apps.authentication.util import hash_pass

class Users(db.Model, UserMixin):

    __tablename__ = 'Userss'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.LargeBinary)
    fullname = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.BIGINT(), nullable=False)
    company = db.Column(db.String(128), nullable=False)
    payment = db.Column(db.String(128), nullable=False)
    amount = db.Column(db.BIGINT(), nullable=False)
    slug = db.Column(db.String(400), nullable=False)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.email)


class dhcxo(db.Model, UserMixin):

    __tablename__ = 'dhcxos'

    id = db.Column(db.Integer,primary_key=True,nullable=True)
    slug = db.Column(db.String(400), nullable=False)
    avatar = db.Column(db.String(128),nullable=False)
    platform = db.Column(db.String(128),nullable=False)

@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    email = Users.query.filter_by(email=email).first()
    return email if email else None
