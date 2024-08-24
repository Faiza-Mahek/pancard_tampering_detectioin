import os

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'pianalytix'
    DB_NAME = "production-db"
    DB_USERNAME = "root"
    DB_PASSWORD = "pianalytix"
    UPLOADS = "/home/username/app/app/static/uploads"
    SESSION_COOKIE_SECURE = True
    DEFAULT_THEME = None

class ProductionConfig(Config):
    # Production-specific settings can be added here
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False
    # Development-specific settings can be added here

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SESSION_COOKIE_SECURE = False
    # Testing-specific settings can be added here
