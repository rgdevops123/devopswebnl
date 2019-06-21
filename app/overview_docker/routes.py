from app.overview_docker import blueprint
from flask import render_template


@blueprint.route('/overview-docker')
def overview_docker():
    with blueprint.open_resource('overview_docker.txt', "r") as f:
        content = f.read()
    return render_template('overview_docker.html', content=content)
