"""
    charityapp.api.admin.token
    ~~~~~~~~~~~~~~

    Token endpoints
"""

from flask import Flask, Blueprint, request, current_app, jsonify
from flask_restful import Resource, Api, abort, reqparse
import os
from json import loads
from ...services import boxviews, users, boxes
from ...boxviews.schemas import BoxViewSchema
from .userresource import SingleUserResource, MultipleUserResource

import traceback
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

baseurl = os.environ["BASE_URL"]
auth0url = os.environ["AUTH0_URL"]

bp = Blueprint('boxviews', __name__)
api = Api(bp)


class BoxView(SingleUserResource):
    def __init__(self):
        super().__init__(BoxViewSchema, boxviews)

    def get(self, usertoken, id):
        """
        Get a boxview for the current user
        ---
        summary: get a user
        tags:
            - Access Token Required
        security:
            - Bearer: []
        operationId: BoxViewGet
        parameters:
          - name: id
            in: query
            required: false
            type: integer
            description: Box view ID
        produces:
            - application/json
        type: string
        description: Auth0 ID of the user.
        responses:
            200:
              description: A boxview object
              schema:
                $ref: '#/definitions/BoxView'
              headers: {}
            403:
              description: Invalid JWT
              schema: {}
            404:
              description: BoxView not found.
              schema: {}
        """
        # oauth_id is in the sub claim of the decoded token
        decodedtoken = usertoken['decoded']
        oauth_id = decodedtoken['sub']
        userobj = users.get_by_oauth_id(oauth_id=oauth_id)

        boxview = self.service.first_or_404(parent_user=userobj, id=id)
        current_app.logger.info(boxview)

        schema = self.Schema()
        result = schema.dump(boxview).data
        return jsonify(result)

    def delete(self, usertoken, id):
        """
        Delete box view from the current user.
        ---
        summary: Delete box view
        tags:
            - Access Token Required
        security:
            - Bearer: []
        operationId: BoxViewDelete
        produces:
          - application/json
        responses:
            204:
              description: BoxView deleted
              schema: {}
            400:
              description: Bad input.
              schema: {}
            404:
              description: BoxView not found
              schema: {}
        """
        boxviewobj = self.service.first_or_404(id=boxviewid)
        self.service.delete(boxviewobj)
        # 204 Response
        return '', 204


class BoxViews(MultipleUserResource):
    def __init__(self):
        super().__init__(BoxViewSchema, boxviews)

    def get(self, usertoken):
        """
        Get a list of BoxViews for the current user.
        ---
        summary: get a user
        tags:
            - Access Token Required
        security:
            - Bearer: []
        operationId: BoxViewsGet
        parameters:
          - name: distinctOnBox
            in: query
            required: false
            type: boolean
            description: Return only the latest BoxView for each scanned box.
        produces:
            - application/json
        type: string
        description: Auth0 ID of the user.
        responses:
            200:
              description: A list of boxview objects ordered from newest to oldest.
              schema:
                type: array
                items: {
                   $ref: '#/definitions/BoxView'
                }
              headers: {}
            403:
              description: Invalid JWT
              schema: {}
        """
        distinctonbox = loads(request.args.get('distinctonbox') or 'false')

        # oauth_id is in the sub claim of the decoded token
        decodedtoken = usertoken['decoded']
        oauth_id = decodedtoken['sub']
        userobj = users.get_by_oauth_id(oauth_id=oauth_id)

        if distinctonbox is True:
            boxviewlist = userobj.latest_boxview_by_box()
        else:
            boxviewlist = self.service.find(parent_user=userobj)

        schema = self.Schema()
        result = schema.dump(boxviewlist, many=True).data
        return jsonify(result)

    def post(self, usertoken):
        """
        Post a box view
        ---
        summary: create a user
        tags:
            - Access Token Required
        security:
            - Bearer: []
        parameters:
          - name: body
            in: body
            required: true
            description: 'Box view object'
            schema:
                $ref: '#/definitions/BoxView'

        operationId: BoxViewsPost
        produces:
            - application/json
        responses:
            201:
              description: BoxView created
              schema:
                $ref: '#/definitions/BoxView'
              headers: {}
            400:
              description: Invalid input, object invalid
              schema: {}
            403:
              description: Invalid JWT
              schema: {}
            404:
              description: Parent resource not found.
              schema: {}
        """
        decodedtoken = usertoken['decoded']
        oauth_id = decodedtoken['sub']
        userobj = users.get_by_oauth_id(oauth_id=oauth_id)

        # Obtain boxserial from the body
        req = request.get_json()
        boxserial = req.get('boxserial')

        current_app.logger.info(req)

        if boxserial is None:
            abort(400, message="box serial required")

        # Find the box object
        boxobj = boxes.get_by_serial(boxserial)

        # Create the box view.
        boxviewobj = self.service.create(parent_box=boxobj, parent_user=userobj)

        # Dump box view into the JSON schema
        schema = self.Schema()
        result = schema.dump(boxviewobj).data

        current_app.logger.info(boxviewobj)
        current_app.logger.info(result)

        return jsonify(result)


api.add_resource(BoxView, '/me/boxviews/<id>')
api.add_resource(BoxViews, '/me/boxviews')