# Inspired by overholt
"""
    flaskapp.api.admin.boxviews
    ~~~~~~~~~~~~~~

    BoxView endpoints
"""

from flask import Blueprint, request, jsonify, current_app
from flask_restful import Api, abort, reqparse
from ...services import boxviews
from ...boxviews.schemas import BoxViewSchema
from ...core import ma
from marshmallow import fields, ValidationError
from .adminresource import SingleAdminResource, MultipleAdminResource


bp = Blueprint('adminboxviews', __name__)
api = Api(bp)


class BoxView(SingleAdminResource):
    """Get, modify or delete one box. """
    def __init__(self):
        super().__init__(BoxViewSchema, boxviews)


class BoxViews(MultipleAdminResource):
    def __init__(self):
        super().__init__(BoxViewSchema, boxviews)

    def get(self):
        """
        Get a list of boxviews.
        Returns:

        """
        return super().get_filtered(optfilterlist=['box_id'])


api.add_resource(BoxView, '/boxview/<id>')
api.add_resource(BoxViews, '/boxviews')
