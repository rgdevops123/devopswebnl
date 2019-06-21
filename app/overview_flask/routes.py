from app.overview_flask import blueprint
from flask import render_template


@blueprint.route('/overview-flask')
def overview_flask():
    with blueprint.open_resource('overview_flask.txt', "r") as f:
        content = f.read()
    return render_template('overview_flask.html', content=content)
