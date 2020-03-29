"""
    flaskapp.api.admin.token
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
        """
        return super().get(modelid=id)


class Captures(MultipleResource):
    def __init__(self):
        super().__init__(ConsumerCaptureSchema, captures)

    def get(self, userobj=None):
        """
        Get a list of captures for a box
        """
        parsedargs = Captures.parse_body_args(request.args.to_dict(),
                                              requiredlist=['serial'],
                                              optlist=['offset', 'limit'])

        serial = parsedargs['serial']
        offset = parsedargs.get('offset', 0)
        limit = parsedargs.get('limit', None)

        boxobj = boxes.get_by_serial(serial)
        capturelist = captures.find(parent_box=boxobj).order_by(captures.__model__.timestamp.desc()).offset(offset).limit(limit)

        schema = self.Schema()
        result = schema.dump(capturelist, many=True)
        return jsonify(result)

    def post(self, userobj=None):
        """
        Create a capture
        """
        parsedargs = super().parse_body_args(request.args.to_dict(),
                                              requiredlist=['serial', 'statusb64', 'timeintb64', 'circbufb64', 'ver'])

        boxobj = boxes.get_by_serial(parsedargs['serial'])

        captureobj = captures.decode_and_create(boxobj=boxobj,
                                                userobj=userobj,
                                                statb64=parsedargs['statusb64'],
                                                timeintb64=parsedargs['timeintb64'],
                                                circb64=parsedargs['circbufb64'],
                                                ver=parsedargs['ver'])

        schema = self.Schema()
        result = schema.dump(captureobj)

        return jsonify(result)


class MeCaptures(Captures):
    method_decorators = [requires_user_token]

    def __init__(self):
        super().__init__()

    def get(self, usertoken):
        """
        Get a list of captures taken by the current user ordered by most recent first.
        """
        decodedtoken = usertoken['decoded']
        oauth_id = decodedtoken['sub']
        userobj = users.get_by_oauth_id(oauth_id=oauth_id)

        distinctonbox = loads(request.args.get('distinctonbox') or 'false')

        if distinctonbox is True:
            capturelist = userobj.latest_capture_by_box()
        else:
            capturelist = captures.find(scanned_by_user=userobj).order_by(captures.__model__.timestamp.desc())

        schema = self.Schema()
        result = schema.dump(capturelist, many=True)
        return jsonify(result)

    def post(self, usertoken):
        """
        Create a capture for a user
        """
        decodedtoken = usertoken['decoded']
        oauth_id = decodedtoken['sub']
        userobj = users.get_by_oauth_id(oauth_id=oauth_id)
        return super().post(userobj=userobj)


api.add_resource(Capture, '/captures/<id>')
api.add_resource(Captures, '/captures')
api.add_resource(MeCaptures, '/me/captures')
