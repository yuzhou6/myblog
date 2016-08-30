#! -*- coding: utf-8 -*-

from . import login_manager
from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin

"""
    权限类
"""
class Permission:
    FOLLOW = 0x01       #关注
    COMMENT = 0x02      #评论
    WRITE_ARTICLES = 0x04   #写文章
    MODERATE_COMMENTS = 0x08    #协管员
    ADMINISTER = 0x80           #超级管理缘

"""
    用户表
"""
class User(UserMixin, db.Model):
    __tablename__= 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    name = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64), unique=True, index=True)
    confirmed = db.Column(db.Boolean, default=False)    #用户认证
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)    #注册时间
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)       #最后登陆时间
    phone = db.Column(db.String(64), unique=True, index=True)           #电话认证

    # about_me = db.Column(db.Text())
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    posts = db.relationship('Post', backref='author' ,lazy='dynamic')


    #刷新用户的访问时间
    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    #检查角色的权限
    def can(self, permissions):
        return self.role is not None and \
                (self.role.permissions & permissions) == permissions

    #检查是否是管理员
    def id_administrator(self):
        return self.can(Permission.ADMINISTER)

    #设置默认角色
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['BLOG_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    #若试图读取密码的属性，则会返回错误
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    #获取认证散列
    def generate_confirmation_token(self, expiration = 3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})        # 由用户 id 生成的密令

    #判断是否认证函数
    def confirm(self,token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

    def __repr__(self):
        return "<User %r , %r>" % (self.username, self.email)

"""
    角色表
"""
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64),unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)     #对应 1, 2， 3， 等权限

    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return "<Role %r>" % self.name

    @staticmethod
    def insert_roles():
        roles = {
            'User':(
                Permission.FOLLOW |
                Permission.COMMENT |
                Permission.WRITE_ARTICLES, True
            ),
            'Moderator':(
                Permission.FOLLOW |
                Permission.COMMENT |
                Permission.WRITE_ARTICLES |
                Permission.MODERATE_COMMENTS, False
            ),
            'Administrator':(
                0xff, False
            )
        }
        for r in roles:
            role = Role.query.filter_by(name = r).first()
            if role is None:
                role = Role(name = r)
            role.permissions = roles[r][0]      #roles 字典中的权限
            role.default = roles[r][1]          #roles 字典中的默认值， 即设定谁为默认值
            db.session.add(role)
            db.session.commit()

"""
文章列表
"""
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, index=True)
    title = db.Column(db.String(128))
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    post_expect = db.Column(db.Text)        # 文章预览
    category_id = db.Column(db.Integer, db.ForeignKey('categorys.id'))
    timestamp = db.Column(db.DateTime, index=True,default=datetime.utcnow)      # 发表时间
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='post', lazy='dynamic')


"""
文章评论表
"""
class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, index=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))


"""
文章种类表
"""
class Category(db.Model):
    __tablename__ = 'categorys'
    id = db.Column(db.Integer, primary_key=True, index=True)
    category = db.Column(db.Unicode(128), unique=True)
    post = db.relationship('Post',backref='category', lazy='dynamic')

    def __repr__(self):
        return " %s" % self.category     # 这句话也是搞笑

    @staticmethod
    def insert_categorys():
        categorys = [
            u'博客技术',
            u'生活感悟',
            u'杂乱文章',
            u'python',
            u'C#',
            u'前端语言'
        ]
        for c in categorys:
            category = Category.query.filter_by(category = c).first()
            if category is None:
                category = Category(category = c)
                db.session.add(category)
                db.session.commit()
"""
用户权限类
"""
class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administator(self):
        return False

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))





