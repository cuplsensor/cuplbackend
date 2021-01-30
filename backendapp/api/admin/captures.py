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

# Inspired by overholt
"""
    flaskapp.api.admin.captures
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Captures endpoints
"""

from flask import Blueprint, request, jsonify, current_app
from flask_restful import Api, abort, reqparse
from sqlalchemy.exc import IntegrityError
from ...services import captures
from ...captures.schemas import CaptureSchema
from ...core import ma
from .adminresource import SingleAdminResource, MultipleAdminResource


bp = Blueprint('admincaptures', __name__)
api = Api(bp)


class Capture(SingleAdminResource):
    """Get, modify or delete one tag. """
    def __init__(self):
        super().__init__(CaptureSchema, captures)


class Captures(MultipleAdminResource):
    def __init__(self):
        super().__init__(CaptureSchema, captures)

    def get(self):
        """
        Get a list of captures.
        Returns:

        """
        captures = super().get_filtered(optfilterlist=['tag_id'])
        return captures

    def post(self):
        """
        Post a capture
        :return:
            The newly created capture or an error code.
        """
        try:
            return super().post()
        except IntegrityError as err:
            return str(err), 409


api.add_resource(Capture, '/capture/<id>')
api.add_resource(Captures, '/captures')
