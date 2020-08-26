"""
    flaskapp.api.admin.token
    ~~~~~~~~~~~~~~

    Token endpoints
"""

from flask import Flask, Blueprint, request, current_app, jsonify
from flask_restful import Resource, Api, abort, reqparse
from wscodec.decoder.exceptions import *
from ...services import captures, tags
from ...captures.schemas import ConsumerCaptureSchema
from ..baseresource import SingleResource, MultipleResource
from json import loads

bp = Blueprint('captures', __name__)
api = Api(bp)


class Capture(SingleResource):
    def __init__(self):
        super().__init__(ConsumerCaptureSchema, captures)


class Captures(MultipleResource):
    def __init__(self):
        super().__init__(ConsumerCaptureSchema, captures)

    def get(self):
        """
        Get a list of captures for a tag
        """
        parsedargs = Captures.parse_body_args(request.args.to_dict(),
                                              requiredlist=['serial'],
                                              optlist=['offset', 'limit'])

        serial = parsedargs['serial']
        offset = parsedargs.get('offset', 0)
        limit = parsedargs.get('limit', None)

        tagobj = tags.get_by_serial(serial)
        capturelist = captures.find(parent_tag=tagobj).order_by(captures.__model__.timestamp.desc()).offset(offset).limit(limit)

        schema = self.Schema()
        result = schema.dump(capturelist, many=True)
        return jsonify(result)

    def post(self):
        """
        Create a capture
        """
        parsedargs = super().parse_body_args(request.get_json(),
                                              requiredlist=['serial', 'statusb64', 'timeintb64', 'circbufb64', 'vfmtb64'])

        tagobj = tags.get_by_serial(parsedargs['serial'])

        try:
            captureobj = captures.decode_and_create(tagobj=tagobj,
                                                    statb64=parsedargs['statusb64'],
                                                    timeintb64=parsedargs['timeintb64'],
                                                    circb64=parsedargs['circbufb64'],
                                                    vfmtb64=parsedargs['vfmtb64'])

            schema = self.Schema()
            result = schema.dump(captureobj)
            return jsonify(result)

        except InvalidMajorVersionError as e:
            return jsonify(ecode=101, description=str(e),
                           encoderversion=e.encoderversion, decoderversion=e.decoderversion), 422

        except InvalidFormatError as e:
            return jsonify(ecode=102, description=str(e), circformat=e.circformat), 422

        except MessageIntegrityError as e:
            return jsonify(ecode=103, description=str(e), urlhash=e.urlhash, calchash=e.calchash), 401

        except NoCircularBufferError as e:
            return jsonify(ecode=104, description=str(e), status=e.status), 400

        except DelimiterNotFoundError as e:
            return jsonify(ecode=105, description=str(e), status=e.status, circb64=e.circb64), 422


api.add_resource(Capture, '/captures/<id>')
api.add_resource(Captures, '/captures')