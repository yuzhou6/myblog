#coding:utf-8

from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, TextAreaField, SelectField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo,DataRequired
from wtforms import ValidationError
from ..models import Category

class WriteAticleForm(Form):
    title = StringField(u'文章标题', validators=[DataRequired(), Length(1,64)])
    body = TextAreaField(u'文章内容', validators=[DataRequired()])
    body_html = TextAreaField(u"预览框内容", validators=[DataRequired()])
    post_expect = TextAreaField(u'摘要')
    category = SelectField(u'文章种类',coerce=int)
    submit = SubmitField(u'发表文章')

    def __init__(self, *args, **kwargs):
        super(WriteAticleForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.category)
                                 for category in Category.query.order_by(Category.category).all()]