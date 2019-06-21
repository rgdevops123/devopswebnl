from flask import Blueprint

errors = Blueprint('errors_blueprint',
                   __name__,
                   template_folder='templates')
