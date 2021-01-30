"""
    flaskapp.api.admin.token
    ~~~~~~~~~~~~~~

    Token endpoints
"""

#  A web application that stores samples from a collection of NFC sensors.
#
#  https://github.com/cuplsensor/cuplbackend
#
#  Original Author: Malcolm Mackay
#  Email: malcolm@plotsensor.com
#  Website: https://cupl.co.uk
#
#  Copyright (c) 2021. Plotsensor Ltd.
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License
#  as published by the Free Software Foundation, either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the
#  GNU Affero General Public License along with this program.
#  If not, see <https://www.gnu.org/licenses/>.

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
