#coding:utf-8

from . import users
from flask import render_template, flash, redirect, url_for, request
from forms import RegistrationForm, LoginForm
from flask_login import login_user, logout_user, login_required, current_user
from ..models import User
from .. import db
from ..email import send_email


@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data,
                    username = form.username.data,
                    password = form.password.data
                    )
        db.session.add(user)
        db.session.commit()
        #得到令牌
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm', '/user/email/confirm', user = user, token = token)
        flash(u'邮件已经发送致你的邮箱，若未收到，请注意查看你的邮件垃圾箱')
        return redirect(url_for('users.login'))
    return render_template("user/register.html",form = form)

@users.route('/login', methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is not None and user.verify_password(form.passowrd.data):
            login_user(user)
            return redirect(request.args.get('next') or url_for('main.index'))
    return render_template('login.html', form = form)

@users.route('/')
def index():
    return render_template("base.html")

@users.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        flash(u'你已经通过了验证,请不要重复')
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash(u'你已经通过了验证')
    else:
        flash(u'验证失败，请确认链接无误')
    return redirect(url_for('main.index'))
