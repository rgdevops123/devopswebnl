from flask import Blueprint

blueprint = Blueprint('users_blueprint',
                      __name__,
                      template_folder='templates',)
