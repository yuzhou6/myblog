#coding:utf-8

from .. import db
from . import main
from flask import render_template, flash, redirect, url_for, abort, request
from flask_login import logout_user, login_required, current_user
from .forms import WriteAticleForm
from ..models import User, Post, Permission, Category



@main.route('/', methods=['GET','POST'])
def index():
    if current_user.is_authenticated:
        flash(u'登录成功')
        # return u"已经登陆"
    else:
        flash(u'还未登录')
    posts = Post.query.all()
    return render_template("index.html", posts = posts)

#显示单片文章
@main.route('/article/<int:id>')
def show_article(id):
    post = Post.query.get_or_404(id)

    return render_template("show_aticle.html", post = post)

@main.route('/user/<username>', methods=['GET','POST'])
def user(username):
    user = User.query.filter_by(username = username).first()
    if user is None:
        abort(404)
    return render_template("user.html")

@main.route('/write-article', methods=['GET','POST'])
@login_required
def write_article():
    form = WriteAticleForm()
    post = None
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        post = Post(
            title = form.title.data,
            body = form.body.data,
            body_html = form.body_html.data,
            category = Category.query.get(form.category.data),
            post_expect = form.post_expect.data,
            author = current_user._get_current_object()         # 根据 model里的这个地方，笔记奇特
        )
        db.session.add(post)
        try:
            db.session.commit()
        except:
            db.session.rollback()
        flash(u"文章发布成功")
        return redirect(url_for('main.index'))
    return render_template("write_article.html", form = form, post = post)

@main.route('/post', methods = ['GET','POST'])
@login_required
def post():
    form = WriteAticleForm()
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
        # return render_template('write_article.html',form = form, post = form.body.data)
        return form.body.data
    return render_template('write_article.html', form = form, post = post)
