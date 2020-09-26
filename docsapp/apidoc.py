from flask import current_app, Blueprint, send_from_directory

apidoc = Blueprint('apidoc', __name__, template_folder='.')


@apidoc.route('/')
def index():
    return send_from_directory('.', 'index.html')


@apidoc.route('/api.yaml')
def apispec():
    return send_from_directory(current_app.config["API_DOCS_FOLDER"], "api.yaml")