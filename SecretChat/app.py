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
from forms import (
        LoginForm, RegistForm, MessageForm,
        UploadForm,
        )
from werkzeug.utils import secure_filename
from SecretChat.extensions import (
    bootstrap, bcrypt
)
from datetime import timedelta
from db import User, Message


app = Flask('Chat')
app.config.from_pyfile('app.config')
bootstrap.init_app(app)
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


@login_manager.user_loader
def load_user(id):
    return User.objects(id=id).first()


@app.route('/')
def index():
    if current_user:
        return render_template('user.html')
    redirect('/login')


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect('/user/me')
    elif request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        remember = form.remember.data
        password = form.password.data
        user = User.objects(username=username).first()
        if user.check_password(password):
            login_user(user, remember=remember)
            return redirect('/user/me')
        return render_template('login.html', form=form, status=0)
    return render_template('login.html', form=form, status=1)


@app.route('/regist', methods=['POST', 'GET'])
def regist():
    form = RegistForm()
    if current_user.is_authenticated:
        return render_template('user.html', user=current_user)
    elif request.method == 'POST' and form.validate_pwd() and form.validate_on_submit():
        if not form.agreed():
            flash('If you disagree the protocol, you can not use our product')
            return render_template('regist.html', form=form)
        nikename = form.nikename.data
        username = form.username.data
        password = form.password.data
        email = form.email.data
        phone = form.phone.data
        user = User(
            username=username,
            nikename=nikename,
            email=email,
            phone=phone,
        )
        user.password = user.set_password(password)
        user.save()
        flash('regist success, you can login now')
        return redirect('login')
    return render_template('regist.html', form=form)


@app.route('/user/<id_>')
def user_info(id_='me'):
    if not current_user:
        flash('Plz login or regist')
        return redirect('login')
    if id_ == 'me':
        user = current_user
    else:
        user = User.get_or_404(id=id_)
    return render_template('user.html', user=user)


@login_required
@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('index'))


@login_required
@app.route('/chat/private/<int:id_>', methods=['POST', 'GET'])
def priv_chat(id_=None):
    form = MessageForm()
    if request.method == 'POST':
        content = form.data.content
        send2 = form.data.send2
        send2user = User.get_or_404(id=send2)
        message = Message(
                create_by=current_user.id,
                content=content,
                send2=send2
                )
        message.save()
    src_msgs = Message.objects(create=current_user.id, send2=id_)
    dst_msgs = Message.objects(send2=current_user.id, create=id_)
    return render_template('/priv_chat.html',src_msgs=src_msgs, dst_msgs=dst_msgs, form=form)


@login_required
@app.route('/chat/group/<int:id_>', methods=['POST', 'GET'])
def group_chat(id_=None):
    form = MessageForm()
    if request.method == 'POST':
        content = form.data.content
        send2 = form.data.send2
        send2user = User.get_or_404(id=send2)
        message = Message(
                create_by=current_user.id,
                content=content,
                send2=send2
                )
        message.save()
    msgs = Message.objects(send2=id_)
    return render_template('/group_chat.html', msgs=msgs, form=form)


app.run(debug=1)
