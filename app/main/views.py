#coding:utf-8

from .. import db
from . import main
from flask import current_app, render_template, flash, redirect, url_for, abort, request, session, jsonify
from flask_login import logout_user, login_required, current_user
from .forms import WriteAticleForm
from ..models import User, Post, Permission, Category
from datetime import datetime
import time

@main.route('/', methods=['GET','POST'])
def index():
    page = request.args.get('page', 1, type = int)
    posts = Post.query.order_by(Post.timestamp.desc()).all()    # desc() 降序排序，从后往前
    posts_amount = Post.query.order_by(Post.timestamp.desc()).count()
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['BLOG_POSTS_PER_PAGE'],
        error_out=False)
    return render_template("index.html", posts = posts,
                           posts_amount = posts_amount,
                           redir = '.index', page = page,
                           pagination = pagination)


#编辑更新文章
@main.route('/edit-article/<int:id>', methods=['GET','POST'])
@login_required
def edit_article(id):
    post = Post.query.get_or_404(id)
    form = WriteAticleForm()
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.body_html = form.body_html.data
        post.category = Category.query.get(form.category.data)
        post.post_expect = form.post_expect.data
        post.author = current_user._get_current_object()  # 根据 model里的这个地方，笔记奇特
        post.timestamp = time.strftime("%Y-%m-%d %X", time.localtime())

        db.session.add(post)
        try:
            db.session.commit()
        except:
            db.session.rollback()
        flash(u"文章更新成功")
        return redirect(url_for('main.index'))

    if post is not None:
        form.title.data = post.title
        form.body.data = post.body
        form.post_expect.data = post.post_expect   # 重新编写的时候，form.post_expect.data 应为是下拉框形式，所以赋予的是 int 类型
        form.category.data = post.category_id

    return render_template("edit_article.html", post = post, form = form)


#显示单篇文章
@main.route('/article/<int:id>')
def show_article(id):
    post = Post.query.get_or_404(id)
    return render_template("show_aticle.html", post = post)

#用户中心
@main.route('/user/<username>', methods=['GET','POST'])
def user(username):
    user = User.query.filter_by(username = username).first()
    if user is None:
        abort(404)
    return render_template("user.html")

#写文章
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
            timestamp = time.strftime("%Y-%m-%d %X", time.localtime()),
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

#删除文章
@main.route('/delete-article/<int:id>', methods=['GET','POST'])
@login_required
def delete_article(id):
    post = Post.query.get_or_404(id)
    if current_user.can(Permission.ADMINISTER) or current_user.username == post.author.username:
        try:
            db.session.delete(post)
            db.session.commit()
            flash(u'删除文章成功')
        except:
            db.session.rollback()
            flash(u'删除文章失败')
    return redirect(request.args.get('next') or url_for('main.index'))

#关于我
@main.route('/about-me')
def about_me():
    return render_template("about_me.html")

#给我留言
@main.route('/give-me-msg', methods=['GET','POST'])
def give_me_msg():
    return render_template("give-me-msg.html")

#友情链接
@main.route('/links')
def links():
    return render_template("links.html")

#资源分享
@main.route('/shares')
def shares():
    return render_template("shares.html")
