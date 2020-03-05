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

bp = Blueprint('boxviews', __name__)
api = Api(bp)


class BoxView(SingleUserResource):
    def __init__(self):
        super().__init__(BoxViewSchema, boxviews)

    def get(self, usertoken, id):
        """
        Get a boxview for the current user
        """
        # oauth_id is in the sub claim of the decoded token
        decodedtoken = usertoken['decoded']
        oauth_id = decodedtoken['sub']
        userobj = users.get_by_oauth_id(oauth_id=oauth_id)

        boxview = self.service.first_or_404(parent_user=userobj, id=id)
        current_app.logger.info(boxview)

        schema = self.Schema()
        result = schema.dump(boxview)
        return jsonify(result)

    def delete(self, usertoken, id):
        """
        Delete box view from the current user.
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
        result = schema.dump(boxviewlist, many=True)
        return jsonify(result)

    def post(self, usertoken):
        """
        Post a box view
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
        result = schema.dump(boxviewobj)

        current_app.logger.info(boxviewobj)
        current_app.logger.info(result)

        return jsonify(result)


api.add_resource(BoxView, '/me/boxviews/<id>')
api.add_resource(BoxViews, '/me/boxviews')