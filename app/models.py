#coding:utf-8

import hashlib
from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin

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
    password_hash = db.Column(db.String(18))
    email = db.Column(db.String(64), unique=True, index=True)
    confirmed = db.Column(db.Boolean, default=False)    #用户认证
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)    #注册时间
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)       #最后登陆时间

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmtion_token(self, expiration = 3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})        # 由用户 id 生成的密令

"""
    角色表
"""
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64),unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)     #对应 1, 2， 3， 等权限

    users = db.relationship('User', backref='role')

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




