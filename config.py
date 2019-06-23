from os import environ


class Config(object):
    SECRET_KEY = environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = environ.get(
        'SQLALCHEMY_TRACK_MODIFICATIONS')


class ProductionConfig(Config):
    DEBUG = False


class DebugConfig(Config):
    DEBUG = True


class TestConfig1(Config):
    DEBUG = True
    LOGIN_DISABLED = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '12346789'


class TestConfig2(Config):
    DEBUG = True
    LOGIN_DISABLED = False
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '12346789'


config_dict = {
    'Production': ProductionConfig,
    'Debug': DebugConfig,
    'Test1': TestConfig1,
    'Test2': TestConfig2
}
