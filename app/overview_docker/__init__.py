from flask import Blueprint

blueprint = Blueprint('overview_docker_blueprint',
                      __name__,
                      template_folder='templates',
                      static_folder='static')
