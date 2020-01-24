"""
    charityapp.api.admin.token
    ~~~~~~~~~~~~~~

    Token endpoints
"""

from flask import Flask, Blueprint, request, current_app, jsonify
from flask_restful import Resource, Api, abort, reqparse
from ...services import captures, boxes, users
from ...captures.schemas import ConsumerCaptureSchema
from ..baseresource import SingleResource, MultipleResource
from .usertokenauth import requires_user_token
from json import loads

bp = Blueprint('captures', __name__)
api = Api(bp)


class Capture(SingleResource):
    def __init__(self):
        super().__init__(ConsumerCaptureSchema, captures)

    def get(self, id):
        """
        Get a capture by ID
        ---
        summary: Get a capture by ID
        tags:
          - Open
        operationId: CaptureGet
        produces:
          - application/json
        responses:
            200:
              description: A capture object
              schema:
                $ref: '#/definitions/Capture'
              headers: {}
            400:
              description: invalid input, object invalid
              schema: {}
            404:
              description: Capture not found.
              schema: {}
        """
        return super().get(modelid=id)


class Captures(MultipleResource):
    def __init__(self):
        super().__init__(ConsumerCaptureSchema, captures)

    def get(self, userobj=None):
        """
        Get a list of captures for a box
        ---
        summary: get a list of captures for a box
        tags:
          - Open
        operationId: CapturesGet
        parameters:
          - name: serial
            in: query
            required: true
            type: string
            description: Box serial
          - name: offset
            in: query
            required: false
            type: integer
            description: Return samples starting from this index.
          - name: limit
            in: query
            required: false
            type: integer
            description: Limit the number of samples returned.
        produces:
          - application/json
        responses:
            200:
              description: A capture object
              schema:
                $ref: '#/definitions/Capture'
              headers: {}
            400:
              description: invalid input, object invalid
              schema: {}
            404:
              description: Box with serial not found.
              schema: {}
        """
        parsedargs = Captures.parse_body_args(request.args.to_dict(),
                                              requiredlist=['serial'],
                                              optlist=['offset', 'limit'])

        serial = parsedargs['serial']
        offset = parsedargs.get('offset', 0)
        limit = parsedargs.get('limit', None)

        boxobj = boxes.get_by_serial(serial)
        capturelist = captures.find(parent_box=boxobj).order_by("timestamp desc").offset(offset).limit(limit)

        schema = self.Schema()
        result = schema.dump(capturelist, many=True).data
        return jsonify(result)

    def post(self, userobj=None):
        """
        Create a capture
        ---
        summary: create a capture
        tags:
          - Open
        operationId: CapturesPost
        produces:
          - application/json
        parameters:
          - name: body
            in: body
            required: true
            description: 'Capture creation fields'
            schema:
              $ref: '#/definitions/EncodedCapture'
        responses:
            200:
              description: A capture object
              schema:
                $ref: '#/definitions/Capture'
              headers: {}
            400:
              description: invalid input, object invalid
              schema: {}
            401:
              description: Not authorised. HMAC does not correspond to input data.
              schema: {}
            404:
              description: Box not found
              schema: {}
            409:
              description: Conflict. A capture with this HMAC already exists. Dead battery or replay attack.
              schema: {}
        """
        current_app.logger.info("test")
        parsedargs = Captures.parse_body_args(request.get_json(),
                                              requiredlist=['serial', 'statusb64', 'timeintb64', 'circbufb64', 'ver'])

        boxobj = boxes.get_by_serial(parsedargs['serial'])

        current_app.logger.info("test")

        captureobj = captures.decode_and_create(boxobj=boxobj,
                                                userobj=userobj,
                                                statb64=parsedargs['statusb64'],
                                                timeintb64=parsedargs['timeintb64'],
                                                circb64=parsedargs['circbufb64'],
                                                ver=parsedargs['ver'])

        schema = self.Schema()
        result = schema.dump(captureobj).data

        return jsonify(result)


class MeCaptures(Captures):
    method_decorators = [requires_user_token]

    def __init__(self):
        super().__init__()

    def get(self, usertoken):
        """
        Get a list of captures taken by the current user ordered by most recent first.
        ---
        summary: Get a list of captures by a user.
        tags:
            - Access Token Required
        security:
            - Bearer: []
        operationId: MeCapturesGet
        parameters:
          - name: distinctOnBox
            in: query
            required: false
            type: boolean
            description: Return only the latest capture for each scanned box.
        produces:
          - application/json
        responses:
            200:
              description: A list of capture objects ordered from newest to oldest
              schema:
                type: array
                items: {
                   $ref: '#/definitions/Capture'
                }
              headers: {}
            400:
              description: invalid input, object invalid
              schema: {}
            401:
              description: Not authorised. HMAC does not correspond to input data or invalid JWT.
              schema: {}
            404:
              description: Box not found.
              schema: {}
        """
        decodedtoken = usertoken['decoded']
        oauth_id = decodedtoken['sub']
        userobj = users.get_by_oauth_id(oauth_id=oauth_id)

        distinctonbox = loads(request.args.get('distinctonbox') or 'false')

        if distinctonbox is True:
            capturelist = userobj.latest_capture_by_box()
        else:
            capturelist = captures.find(scanned_by_user=userobj).order_by("timestamp desc")

        schema = self.Schema()
        result = schema.dump(capturelist, many=True).data
        return jsonify(result)

    def post(self, usertoken):
        """
        Create a capture for a user
        ---
        summary: create a capture
        tags:
            - Access Token Required
        security:
            - Bearer: []
        operationId: MeCapturesPost
        produces:
          - application/json
        parameters:
          - name: body
            in: body
            required: true
            description: 'Capture creation fields'
            schema:
              $ref: '#/definitions/EncodedCapture'
        responses:
            200:
              description: A capture object
              schema:
                $ref: '#/definitions/Capture'
              headers: {}
            400:
              description: Invalid input, object invalid
              schema: {}
            401:
              description: Not authorised. HMAC does not correspond to input data.
              schema: {}
            403:
              description: Not authorised. Invalid JWT.
              schema: {}
            404:
              description: Parent box or user not found.
              schema: {}
            409:
              description: Conflict. A capture with this HMAC already exists. Dead battery or replay attack.
              schema: {}
        """
        decodedtoken = usertoken['decoded']
        oauth_id = decodedtoken['sub']
        userobj = users.get_by_oauth_id(oauth_id=oauth_id)
        return super().post(userobj=userobj)


api.add_resource(Capture, '/captures/<id>')
api.add_resource(Captures, '/captures')
api.add_resource(MeCaptures, '/me/captures')
