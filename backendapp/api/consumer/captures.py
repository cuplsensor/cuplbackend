"""
    flaskapp.api.admin.token
    ~~~~~~~~~~~~~~

    Token endpoints
"""

from flask import Flask, Blueprint, request, current_app, jsonify, make_response, url_for
from flask_restful import Resource, Api, abort, reqparse
from wscodec.decoder.exceptions import *
from sqlalchemy.orm import noload
from sqlalchemy.exc import IntegrityError
import requests
import hmac
import json
from hashlib import sha256
from base64 import b64encode
from ...services import captures, tags
from ...captures.schemas import ConsumerCaptureSchema, ConsumerCaptureSchemaWithSamples
from ..baseresource import SingleResource, MultipleResource
import jwt
from datetime import datetime, timedelta
from secrets import token_hex
from ...config import TAGTOKEN_CLIENTID, TAGTOKEN_CLIENTSECRET
from json import dumps

bp = Blueprint('captures', __name__)
api = Api(bp)


class Capture(SingleResource):
    def __init__(self):
        super().__init__(ConsumerCaptureSchema, captures)

    def delete(self, id):
        abort(404)


class Captures(MultipleResource):
    def __init__(self):
        super().__init__(ConsumerCaptureSchema, captures)

    def createtoken(self, tagserial:str):
        """ Inspired by https://h.readthedocs.io/en/latest/publishers/authorization-grant-tokens/#python """
        now = datetime.utcnow()

        payload = {
            'aud': tagserial,
            'iss': TAGTOKEN_CLIENTID,
            'sub': token_hex(32),
            'nbf': now,
            'exp': now + timedelta(minutes=10),
        }

        return jwt.encode(payload, TAGTOKEN_CLIENTSECRET, algorithm='HS256')

    def generatehmac(self, jsonstr: str, secretkey: str):
        digest = hmac.new(secretkey.encode('utf-8'), jsonstr.encode('utf-8'), sha256).digest()
        computed_hmac = b64encode(digest)
        return computed_hmac

    def webhooktx(self, tagobj, captureobj):
        """
        Transmit JSON dictionary to a webhook
        :param tagobj: Tag object
        :param captureobj: A capture object
        :return: None
        """
        webhook = tagobj.webhook
        if webhook is None:
            return

        fieldsjson = webhook.fields
        if fieldsjson is not None:
            fieldslist = json.loads(fieldsjson)
        else:
            fieldslist = None

        try:
            schema = ConsumerCaptureSchemaWithSamples(only=fieldslist)
            capturedict = schema.dump(captureobj)
        except ValueError:
            # Should not reach here if the API is doing its job and returning an error if an invalid field is submitted.
            capturedict = {'webhook_error': 'Field does not exist. Create a new webhook and check the fields parameter'}


        #webhook.address = 'https://webhook.site/672d3cf8-828b-4908-b57c-16e47ecb1727'
        print(webhook.address)

        capturejson = json.dumps(capturedict)
        hmacstr = self.generatehmac(jsonstr=capturejson, secretkey=webhook.wh_secretkey)
        headers = {'X-CuplBackend-Hmac-SHA256': hmacstr}
        # Thanks to https://stackoverflow.com/questions/16511337/correct-way-to-try-except-using-python-requests-module

        try:
            response = requests.post(webhook.address, json=capturedict, headers=headers, timeout=2)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(str(e))
            print("New connection error. Bad URL but must carry on. Not reported to user yet.")


    def get(self):
        """
        Get a list of captures for a tag
        """
        parsedargs = Captures.parse_body_args(request.args.to_dict(),
                                              requiredlist=['serial'],
                                              optlist=['page', 'per_page'])

        serial = parsedargs['serial']
        page = int(parsedargs.get('page', 1))
        per_page = int(parsedargs.get('per_page', 10))

        tagobj = tags.get_by_serial(serial)
        capturepages = tagobj.captures.options(noload('samples')).paginate(page=page, per_page=per_page, max_per_page=25)
        capturelist = capturepages.items

        schema = self.Schema()
        result = schema.dump(capturelist, many=True)
        response = jsonify(result)
        linkheader = self.make_link_header(capturepages)
        response.headers.add('Link', linkheader)
        return response

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

            tagtoken = self.createtoken(tagserial=tagobj.serial).decode('utf-8')
            tagtoken_type = 'Bearer'

            schema = self.Schema()
            capturedict = schema.dump(captureobj)

            # If the tag has a webhook post to this.
            self.webhooktx(tagobj, captureobj)

            capturedict.update({'tagtoken': tagtoken})
            capturedict.update({'tagtoken_type': tagtoken_type})
            return jsonify(capturedict)

        except InvalidMajorVersionError as e:
            return make_response(jsonify(ecode=101, description=str(e),
                                 encoderversion=e.encoderversion, decoderversion=e.decoderversion), 422)

        except InvalidFormatError as e:
            return make_response(jsonify(ecode=102, description=str(e), circformat=e.circformat), 422)

        except MessageIntegrityError as e:
            return make_response(jsonify(ecode=103, description=str(e), urlhash=e.urlhash, calchash=e.calchash), 401)

        except NoCircularBufferError as e:
            return make_response(jsonify(ecode=104, description=str(e), status=e.status), 400)

        except DelimiterNotFoundError as e:
            return make_response(jsonify(ecode=105, description=str(e), status=e.status, circb64=e.circb64), 422)

        except IntegrityError as e:
            return make_response(jsonify(ecode=106, description=str(e)), 409)


api.add_resource(Capture, '/captures/<id>')
api.add_resource(Captures, '/captures')
