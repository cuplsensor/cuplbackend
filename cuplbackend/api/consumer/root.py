"""
    flaskapp.api.consumer.root
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
        signpost = {'version': url_for('version.version', _external=True),
                    'captures': url_for('captures.captures', _external=True),
                    'random': url_for('tags.randomtag', _external=True)}
        response = jsonify(signpost)
        response.status_code = 200
        return response


api.add_resource(Root, '/')
