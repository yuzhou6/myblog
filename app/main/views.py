#coding:utf-8

from . import main
from flask import render_template, flash
from flask_login import logout_user, login_required, current_user


@main.route('/', methods=['GET','POST'])
def index():
    if current_user.is_authenticated:
        flash(u'登录成功')
        # return u"已经登陆"
    else:
        flash(u'还未登录')
    return render_template("index.html")
