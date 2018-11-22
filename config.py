# 配置文件
import secret


class BaseConfig(object):
    SECRET_KEY = 'nicaibudaoba'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 管理员
    FLASK_ADMIN = secret.FLASK_ADMIN

    # 邮件相关
    FLASK_MAIL_NAME = secret.FLASK_MAIL_NAME
    FLASK_MAIL_PASSWORD = secret.FLASK_MAIL_PASSWORD
    FLASK_MAIL_SERVER = secret.FLASK_MAIL_SERVER
    FLASK_MAIL_PORT = secret.FLASK_MAIL_PORT

    # 分页
    FLASK_MOVIE_PER_PAGE_COUNT = 30
    FLASK_COMMENT_PER_PAGE_COUNT = 20
    FLASK_USERLOG_PER_PAGE_COUNT = 20

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = secret.SQLALCHEMY_DATABASE_URI_DEV


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = secret.SQLALCHEMY_DATABASE_URI_TEST


class ProductConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = secret.SQLALCHEMY_DATABASE_URI_PROD


config = {
    'dev': DevelopmentConfig,
    'prod': ProductConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}