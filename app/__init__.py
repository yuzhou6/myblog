#coding:utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from config import config
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

bootstrap = Bootstrap()
db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()

login_manager.session_protection = 'strong'
login_manager.login_view = 'users.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)


    #初始化各插件
    bootstrap.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)


    # users 蓝图注册
    from .users import users as users_blueprint
    app.register_blueprint(users_blueprint, url_prefix = '/user')

    # main 蓝图注册
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
