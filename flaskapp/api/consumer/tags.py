# Inspired by overholt
"""
    flaskapp.api.admin.tags
    ~~~~~~~~~~~~~~

    Tag endpoints
"""

from flask import Blueprint, request, jsonify
from flask_restful import Api, abort
from ...services import tags
from ...tags.schemas import ConsumerTagSchema
from ..baseresource import SingleResource


bp = Blueprint('consumertags', __name__)
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


api.add_resource(Tag, '/tag/<serial>')