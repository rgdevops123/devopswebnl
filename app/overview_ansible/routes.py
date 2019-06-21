from app.overview_ansible import blueprint
from flask import render_template


@blueprint.route('/overview-ansible')
def overview_ansible():
    with blueprint.open_resource('overview_ansible.txt', "r") as f:
        content = f.read()
    return render_template('overview_ansible.html', content=content)
