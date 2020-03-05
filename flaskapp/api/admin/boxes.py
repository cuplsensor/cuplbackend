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
        ---
        summary: get a box
        operationId: BoxGet
        produces:
          - application/json
        security:
          - Bearer: []
        parameters:
          - name: id
            in: query
            required: false
            type: integer
            description: Box id
        responses:
            200:
              description: A box object
              schema:
                $ref: '#/definitions/Box'
              headers: {}
            400:
              description: bad input parameter
              schema: {}
        definitions:
          Box:
            title: Box
            type: object
            properties:
              id:
                type: integer
                format: int32
              serial:
                example: YWJjZGVM
                type: string
              secretKey:
                example: AAAAcCcC
                type: string
              timeregistered:
                type: string
                format: date-time
        """
        return super().get(id)

    def delete(self, id):
        """
        Delete a box by its serial.
        ---
        summary: delete a box
        operationId: BoxDelete
        produces:
          - application/json
        security:
          - Bearer: []
        parameters:
          - name: id
            in: query
            required: false
            type: integer
            description: Box id
        responses:
            204:
              description: Box has been deleted
              schema: {}
            400:
              description: bad input parameter
              schema: {}
            404:
              description: No box found
              schema: {}
        """
        return super().delete(id)


class Boxes(MultipleAdminResource):
    def __init__(self):
        super().__init__(BoxSchema, boxes)

    def post(self):
        """
        Create a new box.
        ---
        summary: create a box
        operationId: BoxPost
        produces:
          - application/json
        security:
          - Bearer: []
        parameters:
          - name: body
            in: body
            required: false
            description: User details
            schema:
              $ref: '#/definitions/Box'
        responses:
            201:
              description: Box created
              schema:
              $ref: '#/definitions/Box'
              headers: {}
            400:
              description: invalid input, object invalid
              schema: {}
            409:
              description: a user with the same oauth_id already exists
              schema: {}

        """
        return super().post()


api.add_resource(Box, '/box/<id>')
api.add_resource(Boxes, '/boxes')
