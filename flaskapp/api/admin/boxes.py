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
        nsamples = int(parsedargs.get('nsamples', 100))

        urlstr = boxes.simulate(id, frontendurl, nsamples)
        return urlstr


class Boxes(MultipleAdminResource):
    def __init__(self):
        super().__init__(BoxSchema, boxes)

    def get(self):
        """
        Get a list of boxes.
        Returns:

        """
        return super().get_filtered()


api.add_resource(Box, '/box/<id>')
api.add_resource(Boxes, '/boxes')
api.add_resource(BoxSimulate, '/box/<id>/simulate')
