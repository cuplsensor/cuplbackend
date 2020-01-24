# Inspired by overholt
"""
    charityapp.api.admin.boxes
    ~~~~~~~~~~~~~~

    Box endpoints
"""

from flask import Blueprint, request, jsonify, current_app
from flask_restful import Api, abort, reqparse
from ...services import captures
from ...captures.schemas import CaptureSchema
from ...core import ma
from marshmallow import fields, ValidationError
from .adminresource import SingleAdminResource, MultipleAdminResource


bp = Blueprint('admincaptures', __name__)
api = Api(bp)


class Capture(SingleAdminResource):
    """Get, modify or delete one box. """
    def __init__(self):
        super().__init__(CaptureSchema, captures)

    def get(self, id):
        """
        Get a capture by ID.
        ---
        summary: get a capture.
        operationId: AdminCaptureGet
        produces:
          - application/json
        security:
            - Bearer: []
        parameters:
          - name: id
            in: query
            required: false
            type: integer
            description: Capture id
        responses:
            200:
              description: A capture object
              schema:
                $ref: '#/definitions/Capture'
              headers: {}
            400:
              description: bad input parameter
              schema: {}
        """
        return super().get(id)

    def delete(self, id):
        """
        Delete a capture.
        ---
        summary: delete a capture
        operationId: AdminCaptureDelete
        produces:
          - application/json
        security:
            - Bearer: []
        parameters:
          - name: id
            in: query
            required: false
            type: integer
            description: Capture id
        responses:
            204:
              description: Capture has been deleted
              schema: {}
            400:
              description: bad input parameter
              schema: {}
            404:
              description: No capture found
              schema: {}
        """
        return super().delete(id)


class Captures(MultipleAdminResource):
    def __init__(self):
        super().__init__(CaptureSchema, captures)

    def post(self):
        """
        Create a capture
        ---
        summary: create a capture
        operationId: AdminCapturePost
        produces:
          - application/json
        security:
            - Bearer: []
        parameters:
          - name: body
            in: body
            required: false
            description: Capture object
            schema:
              $ref: '#/definitions/Capture'
        responses:
            201:
              description: Capture created
              schema:
              $ref: '#/definitions/Capture'
              headers: {}
            400:
              description: invalid input, object invalid
              schema: {}
            409:
              description: a capture with the same id already exists
              schema: {}

        """
        jsondata = request.get_json()
        schema = self.Schema()
        try:
            schemaobj = schema.load(jsondata).data
        except ValidationError as err:
            return err.messages, 422

        schemaobj = captures.save(schemaobj)

        return schema.dump(schemaobj).data


api.add_resource(Capture, '/capture/<id>')
api.add_resource(Captures, '/captures')
