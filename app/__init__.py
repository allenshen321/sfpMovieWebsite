# 工厂函数，用来初始化Flask及第三方模块，注册蓝图

from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap


# 构建实例
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
bootstrap = Bootstrap()

def creat_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # 将flask实例app加载到第三方模块中
    db.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)

    # 注册蓝图
    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    # 最后返回的是初始化后的app
    return app

