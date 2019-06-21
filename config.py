from os import environ


class Config(object):
    SECRET_KEY = environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI_DEBUG')
    SQLALCHEMY_TRACK_MODIFICATIONS = environ.get(
        'SQLALCHEMY_TRACK_MODIFICATIONS')
    MAIL_SERVER = environ.get('MAIL_SERVER')
    MAIL_PORT = environ.get('MAIL_PORT')
    MAIL_USE_TLS = environ.get('MAIL_USE_TLS')
    MAIL_USERNAME = environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD')


class ProductionConfig(Config):
    DEBUG = False

    """PostgreSQL Database"""
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format(
        environ.get('DEVOPSWEB_DATABASE_USER', 'devopsweb'),
        environ.get('DEVOPSWEB_DATABASE_PASSWORD', 'devopsweb'),
        environ.get('DEVOPSWEB_DATABASE_HOST', 'db'),
        environ.get('DEVOPSWEB_DATABASE_PORT', 5432),
        environ.get('DEVOPSWEB_DATABASE_NAME', 'devopsweb')
    )


class DebugConfig(Config):
    DEBUG = True


class TestConfig1(Config):
    DEBUG = True
    LOGIN_DISABLED = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '12346789'


class TestConfig2(Config):
    DEBUG = True
    LOGIN_DISABLED = False
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '12346789'


config_dict = {
    'Production': ProductionConfig,
    'Debug': DebugConfig,
    'Test1': TestConfig1,
    'Test2': TestConfig2
}
