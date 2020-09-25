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
from ..baseresource import SingleResource

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


api.add_resource(Tag, '/tag/<serial>')