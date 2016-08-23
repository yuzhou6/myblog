#coding:utf-8
import os
# basedir = os.path.abspath(os.path.dirname(__file__))  # 这行有什么用

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess to string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ZHIHU_MAIL_SUBJECT_PREFIX = '[ZHIHU]'
    PHONE_API_KEY =  os.environ.get('PHONE_API_KEY')

    #y邮箱参数
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_SENDER = os.environ.get('MAIL_SENDER')  #邮箱发送者


    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL')

class ProductionCpnfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


config = {
    'production': ProductionCpnfig,

    'default': DevelopmentConfig
}