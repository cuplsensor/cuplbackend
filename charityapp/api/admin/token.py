"""
    charityapp.api.admin.token
    ~~~~~~~~~~~~~~

    Token endpoints
"""

from flask import Flask, Blueprint, request, current_app, jsonify
from flask_restful import Resource, Api, abort, reqparse
from ...config import ADMINAPI_AUDIENCE, ADMINAPI_CLIENTID, ADMINAPI_CLIENTSERET
import os
import datetime
import jwt

baseurl = os.environ["BASE_URL"]

bp = Blueprint('tokens', __name__)
api = Api(bp)

"""
        
        
        

        """

class Token(Resource):
    def createtoken(self):
        """ Inspired by https://h.readthedocs.io/en/latest/publishers/authorization-grant-tokens/#python """
        now = datetime.datetime.utcnow()

        payload = {
            'aud': ADMINAPI_AUDIENCE,
            'iss': ADMINAPI_CLIENTID,
            'sub': 'admin',
            'nbf': now,
            'exp': now + datetime.timedelta(minutes=10),
        }

        return jwt.encode(payload, ADMINAPI_CLIENTSERET, algorithm='HS256')

    def post(self):
        """
        Obtain a JWT for interacting with this API.
        ---
        summary: Obtain a bearer token.
        operationId: TokenPost
        produces:
            - application/json
        parameters:
            - name: body
              in: body
              required: true
              description: 'Token Request Credentials'
              schema:
                $ref: '#/definitions/TokenRequest'
        responses:
            200:
                description: A bearer token that can be used to make calls to other endpoints in this API.
                schema:
                    $ref: '#/definitions/Token'
                headers: {}
            400:
                description: No credentials supplied
                schema: {}
            401:
                description: Bad credentials
                schema: {}
        security: []

        definitions:
            Token:
                title: Token
                type: object
                properties:
                  token:
                    example: eyJz93a...k4laUWw
                    type: string
                  token_type:
                    example: Bearer
                    type: string
            TokenRequest:
                title: TokenRequest
                type: object
                properties:
                  client_id:
                    example: ABE39cASE940
                    type: string
                  client_secret:
                    example: nsfsaeASEFGSAE
                    type: string
        """
        parser = reqparse.RequestParser()
        parser.add_argument('client_id', type=str, required=True, help='client_id string needed')
        parser.add_argument('client_secret', type=str, required=True, help='client_secret string needed')
        args = parser.parse_args()
        # Only clients that send the correct ID and Secret will be given a token.
        if (args['client_id'] != ADMINAPI_CLIENTID) and (args['client_secret'] != ADMINAPI_CLIENTSERET):
            abort(401)
        else:
            token = self.createtoken()
        response = {'token': token.decode('utf-8'), 'token_type': 'Bearer'}
        return jsonify(response)


api.add_resource(Token, '/token')