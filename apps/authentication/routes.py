# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_user,
    logout_user,
    login_required
)

from apps import db, login_manager
from sqlalchemy import update
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm, Update
from apps.authentication.models import Users, dhcxo
from datetime import datetime
import random
import shutil

from apps.authentication.util import verify_pass

@blueprint.route('/')
def route_default():
    return redirect(url_for('authentication_blueprint.login'))

# Login & Registration

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:

        # read form data
        email = request.form['email']
        password = request.form['password']

        # Locate user
        user = Users.query.filter_by(email=email).first()

        # Check the password
        if user and verify_pass(password, user.password):

            login_user(user)
            return redirect(url_for('authentication_blueprint.route_default'))

        # Something (user or pass) is not ok
        return render_template('accounts/login.html',
                               msg='Wrong user or password',
                               form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html',
                               form=login_form)
    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        email = request.form['email']
        company = request.form['company']
        password = request.form['password']
        confirm_password = request.form['repeat_password']

        # Confirm password
        if (password!= confirm_password):
            return render_template('accounts/register.html',
                                   msg='Password dosen\'t match',encoding='utf-8',
                                   success=False,
                                   form=create_account_form)


        # Check usename exists
        user = Users.query.filter_by(company=company).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Comapny already registered',encoding='utf-8',
                                   success=False,
                                   form=create_account_form)
        
        # Check email exists
        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Email already registered',encoding='utf-8',
                                   success=False,
                                   form=create_account_form)

        now = datetime.now()
        current_time = now.strftime("%Y%m%d%H%M%S")
        slugs = company + str(current_time) + str(random.randint(10000,99999))

        # else we can create the user
        user = Users(**request.form, payment="No", amount="0",slug = slugs )
        Dhcxo = dhcxo(
            slug = slugs,
            avatar = "Male",
            platform = "Website"
        )     
        db.session.add(user)
        db.session.commit()
        db.session.add(Dhcxo)
        db.session.commit()
        direc =  slugs
        source_dir = r"./aihuman"
        destination_dir =direc
        shutil.copytree(source_dir, destination_dir)

        # Delete user from session
        logout_user()

        return render_template('accounts/register.html',
                               msg='User created successfully.',encoding='utf-8',
                               success=True,
                               form=create_account_form)

        
    else:
        return render_template('accounts/register.html', form=create_account_form)

@blueprint.route('/configuration', methods=['GET', 'POST'])
@login_required
def configuration():
    
    # create_update= Update(request.form)
    if 'update' in request.form:
       # read form data
        value= request.form['customRadio']
        print(value)
        print(current_user.slug)
        updates = dhcxo.query.filter_by(slug=current_user.slug).first()
        print(updates)
        updates.avatar = value
        db.session.commit()
        db.session.commit()
        return redirect(url_for('authentication_blueprint.route_default'))
    else:
        return render_template('home/configuration.html')
    
@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login')) 

# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500
