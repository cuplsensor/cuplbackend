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
    flaskapp.api.admin.tags
    ~~~~~~~~~~~~~~

    Tag endpoints
"""

from flask import Blueprint, request, jsonify, url_for
from flask_restful import Api, abort
from ...services import tags
from ...tags.schemas import ConsumerTagSchema
from .tagtokenauth import requires_tagtoken
from ..baseresource import SingleResource, BaseResource

bp = Blueprint('tags', __name__)
api = Api(bp)


class Tag(SingleResource):
    """Get, modify or delete one tag. """
    def __init__(self):
        super().__init__(ConsumerTagSchema, tags)

    def get(self, serial):
        """
        Get a tag by its serial.
        """
        tagobj = tags.get_by_serial(serial)
        schema = self.Schema()
        result = schema.dump(tagobj)
        return jsonify(result)

    @requires_tagtoken
    def put(self, serial):
        """Edit a tag description"""
        parsedargs = super().parse_body_args(request.get_json(), requiredlist=['description'])
        description = parsedargs['description']
        tagobj = tags.get_by_serial(serial)
        tags.update(tagobj, description=description)
        return '', 204

    def delete(self, serial):
        abort(404)


class RandomTag(BaseResource):
    """ Get a random tag. """

    def __init__(self):
        super().__init__(ConsumerTagSchema, tags)

    def get(self):
        """
        Get a tag by its serial.
        """
        tagobj = tags.random()
        schema = self.Schema()
        result = schema.dump(tagobj)
        return jsonify(result)


api.add_resource(Tag, '/tag/<serial>')
api.add_resource(RandomTag, '/random/tag')
