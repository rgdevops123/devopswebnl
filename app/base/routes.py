from flask import abort, redirect, url_for

from app.base import blueprint


@blueprint.route('/')
def route_default():
    return redirect(url_for('home_blueprint.home'))


@blueprint.route('/devopsweb-403')
def route_devopsweb_403():
    abort(403)


@blueprint.route('/devopsweb-404')
def route_devopsweb_404():
    abort(404)


@blueprint.route('/devopsweb-500')
def route_devopsweb_500():
    abort(500)


@blueprint.route('/devopsweb-501')
def route_devopsweb_501():
    abort(501)


@blueprint.route('/devopsweb-503')
def route_devopsweb_503():
    abort(503)
