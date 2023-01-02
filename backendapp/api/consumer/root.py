"""
    flaskapp.api.consumer.root
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

from flask import Blueprint, url_for, jsonify
from flask_restful import Resource, Api


bp = Blueprint('root', __name__)
api = Api(bp)


class Root(Resource):
    """
    Define a Resource for the Root of the Consumer API.
    """
    def get(self):
        """
        Return 3 URLs for obtaining version information, a list of captures or a random tag.

        This is a starting point for an HTTP client with no knowledge of the API structure (HATEOAS).
        """
        signpost = {'version': url_for('version.version', _external=True),
                    'captures': url_for('captures.captures', _external=True),
                    'random': url_for('tags.randomtag', _external=True)}
        response = jsonify(signpost)
        response.status_code = 200
        return response


# Add the Root resource to the API root.
api.add_resource(Root, '/')
