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


class BoxSimulate(SingleAdminResource):
    """Get a URL created by the encoder in wscodec. Similar to what the box will produce. """
    def __init__(self):
        super().__init__(BoxSchema, boxes)

    def get(self, id):
        """
        Get a URL for simulating the website response to a box scan.

        Args:
            id: Box id.

        Returns:
            A URL.
        """
        parsedargs = super().parse_body_args(request.args.to_dict(),
                                             requiredlist=['frontendurl'],
                                             optlist=['nsamples'])

        frontendurl = parsedargs['frontendurl']
        nsamples = parsedargs.get('nsamples', 100)

        urlstr = boxes.simulate(id, frontendurl, nsamples)
        return urlstr


class Boxes(MultipleAdminResource):
    def __init__(self):
        super().__init__(BoxSchema, boxes)

    def post(self):
        """
        Create a new box. Optionally an ID can be specified.
        """
        parsedargs = super().parse_body_args(request.args.to_dict(),
                                             optlist=['id'])

        boxobj = self.service.create(id=parsedargs['id'])

        schema = self.Schema()
        return schema.dump(boxobj)

    def get(self):
        """
        Get a list of boxes.
        Returns:

        """
        parsedargs = super().parse_body_args(request.args.to_dict(),
                                             optlist=['offset', 'limit'])

        offset = parsedargs.get('offset', 0)
        limit = parsedargs.get('limit', None)

        boxlist = self.service.all().order_by(self.service.__model__.id.desc()).offset(offset).limit(limit)

        schema = self.Schema()
        result = schema.dump(boxlist, many=True)
        return jsonify(result)


api.add_resource(Box, '/box/<id>')
api.add_resource(Boxes, '/boxes')
api.add_resource(BoxSimulate, '/box/<id>/simulate')
