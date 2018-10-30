# 配置文件
import secret


class BaseConfig(object):
    SECRET_KEY = 'nicaibudaoba'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    FLASK_MOVIE_PER_PAGE_COUNT = 20

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