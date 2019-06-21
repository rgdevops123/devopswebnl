from app.overview_python import blueprint
from flask import render_template


@blueprint.route('/overview-python')
def overview_python():
    with blueprint.open_resource('overview_python.txt', "r") as f:
        content = f.read()
    return render_template('overview_python.html', content=content)
