from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
from logging import DEBUG, Formatter, StreamHandler, getLogger
from logging.handlers import RotatingFileHandler

from os import mkdir, path

db = SQLAlchemy()
logger = getLogger(__name__)
logger.setLevel(DEBUG)
login_manager = LoginManager()
login_manager.login_view = 'users_blueprint.login'
mail = Mail()


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)


def register_blueprints(app):
    for module_name in ('base',
                        'home',
                        'overview_ansible',
                        'overview_docker',
                        'overview_flask',
                        'overview_kubernetes',
                        'overview_linux',
                        'overview_postgresql',
                        'overview_python',
                        'overview_sqlite',
                        'users'):
        module = import_module('app.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def register_error_handlers(app):
    module = import_module('app.errors.handlers')
    app.register_blueprint(module.errors)


def configure_database(app):

    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()


def configure_logs(app):
    if not path.exists('logs'):
        mkdir('logs')

    file_handler = RotatingFileHandler(
       'logs/devopsweb.log', maxBytes=3000, backupCount=10)

    frmt = '%(asctime)s %(levelname)s: %(message)s [%(pathname)s:%(lineno)d]'
    file_handler.setFormatter(
        Formatter(frmt))

    file_handler.setLevel(DEBUG)

    stream_handler = StreamHandler()
    stream_handler.setLevel(DEBUG)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)


def create_app(config, selenium=False):
    app = Flask(__name__, static_folder='static')
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    register_error_handlers(app)
    configure_database(app)
    configure_logs(app)
    logger.info('Dev Ops Web Startup')
    return app
