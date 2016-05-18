import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    UPLOAD_FOLDER = '/uploads'


class DevelopmentConfig(Config):
    DEBUG = True
    DB_URI = 'sqlite:///{}'.format(os.path.join(basedir, 'data-dev.sqlite'))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or DB_URI
    SSL_DISABLE = True


class ProductionConfig(Config):
    DB_URI = 'sqlite:///{}'.format(os.path.join(basedir, 'data.sqlite'))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or DB_URI


class TestingConfig(Config):
    TESTING = True


config = dict(development=DevelopmentConfig, testing=TestingConfig, production=ProductionConfig,
              default=DevelopmentConfig)
