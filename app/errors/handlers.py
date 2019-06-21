from app.errors import errors
from flask import render_template

from app import login_manager


@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('401.html'), 401


@errors.app_errorhandler(403)
def forbidden_error_403_handler(error):
    return render_template('403.html'), 403


@errors.app_errorhandler(404)
def not_found_error_404_handler(error):
    return render_template('404.html'), 404


@errors.app_errorhandler(500)
def internal_server_error_500_handler(error):
    return render_template('500.html'), 500


@errors.app_errorhandler(501)
def not_implemented_error_501_handler(error):
    return render_template('501.html'), 501


@errors.app_errorhandler(503)
def service_unavailable_error_503_handler(error):
    return render_template('503.html'), 503
