import os
from tempfile import mkdtemp

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    CSFR_ENABLED = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///rules.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
