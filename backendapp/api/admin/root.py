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
    Define a Resource for the Root of the Admin API.
    """
    def get(self):
        """
        Return URLs for the 4 top-level resources in this API.

        HATEOAS stipulates that an API cannot assume an HTTP client is aware of its structure.
        """
        signpost = {'token': url_for('tokens.token', _external=True),
                    'tags': url_for('admintags.tags', _external=True),
                    'captures': url_for('admincaptures.captures', _external=True),
                    'webhooks': url_for('adminwebhooks.webhooks', _external=True)}
        response = jsonify(signpost)
        response.status_code = 200
        return response


# Add the Root resource to the API root.
api.add_resource(Root, '/')
