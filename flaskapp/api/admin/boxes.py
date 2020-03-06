# Inspired by overholt
"""
    flaskapp.api.admin.boxes
    ~~~~~~~~~~~~~~

    Box endpoints
"""

from flask import Blueprint, request, jsonify
from flask_restful import Api, abort
from ...services import boxes
from ...boxes.schemas import BoxSchema
from .adminresource import SingleAdminResource, MultipleAdminResource


bp = Blueprint('adminboxes', __name__)
api = Api(bp)


class Box(SingleAdminResource):
    """Get, modify or delete one box. """
    def __init__(self):
        super().__init__(BoxSchema, boxes)

    def get(self, id):
        """
        Get a box by its serial.
        """
        return super().get(id)

    def delete(self, id):
        """
        Delete a box by its serial.
        """
        return super().delete(id)


class Boxes(MultipleAdminResource):
    def __init__(self):
        super().__init__(BoxSchema, boxes)

    def post(self):
        """
        Create a new box.
        """
        return super().post()


api.add_resource(Box, '/box/<id>')
api.add_resource(Boxes, '/boxes')
