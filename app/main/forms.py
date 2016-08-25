#coding:utf-8

from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, TextAreaField, SelectField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo,DataRequired
from wtforms import ValidationError

class PostForm(Form):
    title = StringField(u'文章标题', validators=[DataRequired(), Length(1,64)])
    body = TextAreaField(u'文章内容', validators=[DataRequired()])
    # Category = SelectField(u'文章种类',coerce=int)
    submit = SubmitField(u'发表文章')