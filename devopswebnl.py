from flask_migrate import Migrate
from os import environ
from sys import exit

from config import config_dict
from app import create_app

get_config_mode = environ.get('DEVOPSWEB_CONFIG_MODE', 'Debug')

try:
    config_mode = config_dict[get_config_mode.capitalize()]
except KeyError:
    exit('Error: Invalid DEVOPS_CONFIG_MODE environment variable.')

app = create_app(config_mode)
Migrate(app)
