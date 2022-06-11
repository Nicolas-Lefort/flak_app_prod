import os
basedir = os.path.abspath(os.path.dirname(__file__))

username = 'root'
password = 'root12'
dbname = 'myflaskapp'

class Config(object):
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = 'mysql://'+username+':'+password+'@localhost/'+dbname
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

config = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig,
    'default': DevelopmentConfig,
}