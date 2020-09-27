"""
    flaskapp.api.admin.token
    ~~~~~~~~~~~~~~

    Token endpoints
"""

from flask import Flask, Blueprint, request, current_app, jsonify
from flask_restful import Resource, Api, abort, reqparse
from os import path
import pkg_resources
import json

bp = Blueprint('version', __name__)
api = Api(bp)


def versioninfo():
    basepath = path.dirname(__file__)
    versionfilepath = path.abspath(path.join(basepath, "..", "..", "VERSION"))
    with open(versionfilepath) as version_file:
        cuplbackendversion = version_file.read().strip()

    cuplcodecversion = pkg_resources.get_distribution("cuplcodec").version

    versiondict = {'cuplcodec': cuplcodecversion,
                   'cuplbackend': cuplbackendversion}

    return versiondict


class Version(Resource):
    def get(self):
        """
        Get version information about wsbackend.
        """
        response = jsonify(versioninfo())
        response.status_code = 200
        return response


api.add_resource(Version, '/version')
