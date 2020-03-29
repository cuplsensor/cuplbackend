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
        parsedargs = super().parse_body_args(request.args.to_dict(),
                                             optlist=['offset', 'limit', 'box_id'])

        offset = parsedargs.get('offset', 0)
        limit = parsedargs.get('limit', None)
        box_id = parsedargs.get('box_id', None)

        filters = dict()
        if box_id is not None:
            filters.update({'box_id': box_id})

        boxviewlist = self.service.find(**filters).order_by(self.service.__model__.id.desc()).offset(offset).limit(limit)

        schema = self.Schema()
        result = schema.dump(boxviewlist, many=True)
        return jsonify(result)

    def post(self):
        """
        Create a boxview
        """
        jsondata = request.get_json()
        schema = self.Schema()
        try:
            schemaobj = schema.load(jsondata)
        except ValidationError as err:
            return err.messages, 422

        schemaobj = boxviews.save(schemaobj)

        return schema.dump(schemaobj)


api.add_resource(BoxView, '/boxview/<id>')
api.add_resource(BoxViews, '/boxviews')
