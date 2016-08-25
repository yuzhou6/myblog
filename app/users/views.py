#coding:utf-8

import random
from . import users
from flask import render_template, flash, redirect, url_for, request, session, jsonify
from forms import Email_RegistrationForm, Phone_RegistrationForm,LoginForm
from flask_login import login_user, logout_user, login_required, current_user,current_app
from ..models import User
from .. import db
from sqlalchemy.sql import or_
from ..email import send_email
from ..phone import send_sms

@users.route('/')
def index():
    return render_template("base.html")

@users.route('/email-register', methods=['GET', 'POST'])
def email_register():
    form = Email_RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                        username=form.username.data,
                        password=form.password.data
                        )
        db.session.add(user)
        db.session.commit()
        # 得到令牌
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm', '/user/email/confirm', user=user, token=token)
        flash(u'邮件已经发送致你的邮箱，若未收到，请注意查看你的邮件垃圾箱')
        return redirect(url_for('users.login'))
    return render_template("user/email_register.html", form = form)

@users.route('/phone-register', methods=['GET', 'POST'])
def phone_register():
    form = Phone_RegistrationForm()
    if form.validate_on_submit():
        if session['code'] == form.validate_code.data:
            user = User(phone=form.phone.data,
                            password=form.password.data
                            )
            user.confirmed = True
            db.session.add(user)
            db.session.commit()
            flash(u'手机验证成功')
            return redirect(url_for('users.login'))
    return render_template("user/phone_register.html", form = form)

@users.route('/phone-register-code')
def phone_register_code():
    # 随机生成 6位数 code
    if request.args.get('phone') is not None:
        code = random.randint(100000, 999999)
        session['code'] = code
        text = "【少寨主lucat】监控：验证码为%s" % code
        phone = request.args.get('phone')
        #调用短信接口发送
        if current_app.config['PHONE_API_KEY'] is not None:
            send_sms(current_app.config['PHONE_API_KEY'], text, phone)
            return jsonify({'phone': phone})
        return  jsonify({'phone':'false 1'})
    return jsonify({'phone': 'false 2'})

@users.route('/login', methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # user = User.query.filter_by(email = form.email.data).first()
        user = User.query.filter(or_(User.username == form.login_name.data, User.phone == form.login_name.data ,User.email == form.login_name.data)).first()
        if user is not None and user.verify_password(form.passowrd.data):
            login_user(user)
            return redirect(request.args.get('next') or url_for('main.index'))
    return render_template('login.html', form = form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

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
