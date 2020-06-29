# Inspired by overholt
"""
    flaskapp.api.admin.tagviews
    ~~~~~~~~~~~~~~

    TagView endpoints
"""

from flask import Blueprint, request, jsonify, current_app
from flask_restful import Api, abort, reqparse
from ...services import tagviews
from ...tagviews.schemas import TagViewSchema
from ...core import ma
from marshmallow import fields, ValidationError
from .adminresource import SingleAdminResource, MultipleAdminResource


bp = Blueprint('admintagviews', __name__)
api = Api(bp)


class TagView(SingleAdminResource):
    """Get, modify or delete one tag. """
    def __init__(self):
        super().__init__(TagViewSchema, tagviews)


class TagViews(MultipleAdminResource):
    def __init__(self):
        super().__init__(TagViewSchema, tagviews)

    def get(self):
        """
        Get a list of tagviews.
        Returns:

        """
        return super().get_filtered(optfilterlist=['tag_id'])


api.add_resource(TagView, '/tagview/<id>')
api.add_resource(TagViews, '/tagviews')
