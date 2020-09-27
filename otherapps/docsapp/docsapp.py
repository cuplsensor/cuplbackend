from flask import Flask
from .apidoc import apidoc


def create_app(api_docs_folder):
    app = Flask(__name__)
    app.config["API_DOCS_FOLDER"] = api_docs_folder
    app.register_blueprint(apidoc)
    return app



