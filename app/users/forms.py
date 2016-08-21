#coding:utf-8

from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo,DataRequired
from wtforms import ValidationError
from ..models import User

class RegistrationForm(Form):
    email = StringField(u'电子邮箱', validators=[DataRequired(), Length(1,64), Email()])
    username = StringField(u'用户名', validators=[
        DataRequired(),
        Length(1,64),
        Regexp('^[A-Za-z0-9_.]*$', 0,
               u'用户名必须为字母， '
               u'数字，点或者下划线')
    ])
    password = PasswordField(u'密码', validators=[
        Required(), EqualTo('password2', message=u'密码不匹配')])
    password2 = PasswordField(u'密码确认', validators=[Required()])
    submit = SubmitField(u'注册')

    def validate_email(self, field):
        if User.query.filter_by(email = field.data).first():
            raise ValidationError(u'该邮箱已经被使用')

    def validate_username(self, field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError(u'该用户名已经被使用')

class LoginForm(Form):
    email = StringField(u'邮箱', validators=[DataRequired(), Length(1,64), Email()])
    passowrd = PasswordField(u'密码', validators=[DataRequired()])
    remember_me = BooleanField(u'保持登陆')
    submit = SubmitField(u'登陆')

