#coding:utf-8

from . import users
from flask import render_template, flash, redirect, url_for
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
        token = user.generate_confirmtion_token()
        send_email(user.email, 'Confirm', '/user/email/confirm', user = user, token = token)
        flash(u'邮件已经发送致你的邮箱，若未收到，请注意查看你的邮件垃圾箱')
        return redirect(url_for('users.index'))
    return render_template("user/register.html",form = form)

@users.route('/login', methods = ['GET' , 'POSt'])
def login():
    return render_template('login.html')

@users.route('/')
def index():
    return render_template("base.html")
    # return render_template("login.html")