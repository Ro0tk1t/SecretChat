#!/usr/bin/env python
# coding=utf-8

from flask import (
        url_for, Flask, render_template, session,
        redirect, abort, flash, request,
        )
from flask_login import (
        LoginManager, login_user, logout_user,
        current_user, login_required,
        )
from datetime import timedelta
from db import User


app = Flask('Chat')
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.init_app(app)


app.permanent_session_lifetime = timedelta(minutes=120)

@app.errorhandler(404)
def error_404(error):
    return render_template('404.html'), 404


@app.errorhandler(403)
def error_403(error):
    return render_template('403.html'), 403


@app.route('/')
def index():
    if current_user:
        return render_template('user.html')
    redirect('/login')


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if current_user:
        return render_template('user.html', user=current_user)
    elif request.method == 'POST' and form.validate_on_submit():
        username = form.data.username
        password = form.data.password
        remmeber = form.data.remember
        user = User.objects(username=username, password=password, remember=remember).first()
        if user:
            login_user(user, remember=remember)
            return redirect('/user')
        return render_template('user.html', user=current_user)
    return render_template('login.html')


@app.route('/user')
def user_info():
    if not current_user:
        flash('Plz login or regist')
        return redirect('login')
    else:
       # username = current_user.username
       # nikename = current_user.nikename
       # describe = current_user.describe
       # phone = current_user.phone
       # email = current_user.email
       # state = current_user.state
       # last_online = current_user.last_online
        return render_template('user.html', user=current_user)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('index'))


app.run(debug=1)
