"""
    flaskapp.api.admin.root
    ~~~~~~~~~~~~~~

    Token endpoints
"""

from flask import Blueprint, url_for, jsonify
from flask_restful import Resource, Api


bp = Blueprint('root', __name__)
api = Api(bp)


class Root(Resource):
    def get(self):
        """
        Get version information about wsbackend.
        """
        signpost = {'token': url_for('tokens.token', _external=True),
                    'tags': url_for('admintags.tags', _external=True),
                    'captures': url_for('admincaptures.captures', _external=True),
                    'webhooks': url_for('adminwebhooks.webhooks', _external=True)}
        response = jsonify(signpost)
        response.status_code = 200
        return response


api.add_resource(Root, '/')
