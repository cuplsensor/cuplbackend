# Inspired by overholt
"""
    flaskapp.api.admin.tags
    ~~~~~~~~~~~~~~

    Tag endpoints
"""

from flask import Blueprint, request, jsonify, current_app
from flask_restful import Api, abort, reqparse
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
        return super().get_filtered(optfilterlist=['tag_id'])


api.add_resource(Capture, '/capture/<id>')
api.add_resource(Captures, '/captures')
