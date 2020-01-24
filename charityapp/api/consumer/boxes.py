# Inspired by overholt
"""
    charityapp.api.admin.boxes
    ~~~~~~~~~~~~~~

    Box endpoints
"""

from flask import Blueprint, request, jsonify
from flask_restful import Api, abort
from ...services import boxes, users
from ...boxes.schemas import ConsumerBoxSchema
from ..baseresource import SingleResource
from .userresource import SingleUserResource


bp = Blueprint('consumerboxes', __name__)
api = Api(bp)


class Box(SingleResource):
    """Get, modify or delete one box. """
    def __init__(self):
        super().__init__(ConsumerBoxSchema, boxes)

    def get(self, serial):
        """
        Get a box by its serial.
        ---
        summary: get a box
        tags:
          - Open
        operationId: BoxGet
        produces:
          - application/json
        parameters:
          - name: serial
            in: query
            required: false
            type: string
            description: Box serial
        responses:
            200:
              description: A box object
              schema:
                $ref: '#/definitions/Box'
              headers: {}
            400:
              description: Bad input parameter.
              schema: {}
            404:
              description: Box not found.
        """
        boxobj = boxes.get_by_serial(serial)

        schema = self.Schema()
        result = schema.dump(boxobj).data

        return jsonify(result)


class HasScannedBox(SingleUserResource):
    """Get, modify or delete one box. """
    def __init__(self):
        super().__init__(ConsumerBoxSchema, boxes)

    def get(self, usertoken, serial):
        """
        Has a box with a given serial been scanned by the current user?
        ---
        summary: get a box
        tags:
          - Access Token Required
        operationId: HasScannedBox
        produces:
          - application/json
        security:
          - Bearer: []
        parameters:
          - name: serial
            in: query
            required: true
            type: string
            description: Box serial
        responses:
            200:
              description: True if the box has a capture taken by the current user.
              type: boolean
              headers: {}
            400:
              description: Bad input parameter
              schema: {}
            404:
              description: Box or user not found.
              schema: {}
        """
        decodedtoken = usertoken['decoded']
        oauth_id = decodedtoken['sub']
        userobj = users.get_by_oauth_id(oauth_id=oauth_id)

        # Check that the user has scanned this box
        result = userobj.has_scanned_box(serial)

        return jsonify(result)

api.add_resource(Box, '/box/<serial>')
api.add_resource(HasScannedBox, '/box/<serial>/scanned')
