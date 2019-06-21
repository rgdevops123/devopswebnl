from app.overview_sqlite import blueprint
from flask import render_template


@blueprint.route('/overview-sqlite')
def overview_sqlite():
    with blueprint.open_resource('overview_sqlite.txt', "r") as f:
        content = f.read()
    return render_template('overview_sqlite.html', content=content)
