#coding:utf-8

from .. import db
from . import main
from flask import render_template, flash, redirect, url_for, abort
from flask_login import logout_user, login_required, current_user
from .forms import PostForm
from ..models import User, Post, Permission



@main.route('/', methods=['GET','POST'])
def index():
    if current_user.is_authenticated:
        flash(u'登录成功')
        # return u"已经登陆"
    else:
        flash(u'还未登录')
    return render_template("index.html")

@main.route('/user/<username>', methods=['GET','POST'])
def user(username):
    user = User.query.filter_by(username = username).first()
    if user is None:
        abort(404)
    return render_template("user.html")

@main.route('/post', methods = ['GET','POST'])
@login_required
def post():
    form = PostForm()
    post = None
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        # post = Post(
        #     title = form.title.data,
        #     body = form.body.data,
        #     author = current_user._get_current_object(),
        # )
        # db.session.add(post)
        # db.session.commit()
        # return redirect(url_for('main.index'))
        # return render_template('post.html',form = form, post = form.body.data)
        return form.body.data
    return render_template('post.html', form = form, post = post)
