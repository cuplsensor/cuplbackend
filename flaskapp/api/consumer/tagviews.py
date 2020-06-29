"""
    flaskapp.api.admin.token
    ~~~~~~~~~~~~~~

    Token endpoints
"""

from flask import Flask, Blueprint, request, current_app, jsonify
from flask_restful import Resource, Api, abort, reqparse
import os
from json import loads
from ...services import tagviews, users, tags
from ...tagviews.schemas import TagViewSchema
from .userresource import SingleUserResource, MultipleUserResource

import traceback
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

bp = Blueprint('tagviews', __name__)
api = Api(bp)


class TagView(SingleUserResource):
    def __init__(self):
        super().__init__(TagViewSchema, tagviews)

    def get(self, usertoken, id):
        """
        Get a tagview for the current user
        """
        # oauth_id is in the sub claim of the decoded token
        decodedtoken = usertoken['decoded']
        oauth_id = decodedtoken['sub']
        userobj = users.get_by_oauth_id(oauth_id=oauth_id)

        tagview = self.service.first_or_404(parent_user=userobj, id=id)
        current_app.logger.info(tagview)

        schema = self.Schema()
        result = schema.dump(tagview)
        return jsonify(result)

    def delete(self, usertoken, id):
        """
        Delete tag view from the current user.
        """
        tagviewobj = self.service.first_or_404(id=tagviewid)
        self.service.delete(tagviewobj)
        # 204 Response
        return '', 204


class TagViews(MultipleUserResource):
    def __init__(self):
        super().__init__(TagViewSchema, tagviews)

    def get(self, usertoken):
        """
        Get a list of TagViews for the current user.
        """
        distinctontag = loads(request.args.get('distinctontag') or 'false')

        # oauth_id is in the sub claim of the decoded token
        decodedtoken = usertoken['decoded']
        oauth_id = decodedtoken['sub']
        userobj = users.get_by_oauth_id(oauth_id=oauth_id)

        if distinctontag is True:
            tagviewlist = userobj.latest_tagview_by_tag()
        else:
            tagviewlist = self.service.find(parent_user=userobj)

        schema = self.Schema()
        result = schema.dump(tagviewlist, many=True)
        return jsonify(result)

    def post(self, usertoken):
        """
        Post a tag view
        """
        decodedtoken = usertoken['decoded']
        oauth_id = decodedtoken['sub']
        userobj = users.get_by_oauth_id(oauth_id=oauth_id)

        # Obtain tagserial from the body
        req = request.get_json()
        tagserial = req.get('tagserial')

        current_app.logger.info(req)

        if tagserial is None:
            abort(400, message="tag serial required")

        # Find the tag object
        tagobj = tags.get_by_serial(tagserial)

        # Create the tag view.
        tagviewobj = self.service.create(parent_tag=tagobj, parent_user=userobj)

        # Dump tag view into the JSON schema
        schema = self.Schema()
        result = schema.dump(tagviewobj)

        current_app.logger.info(tagviewobj)
        current_app.logger.info(result)

        return jsonify(result)


api.add_resource(TagView, '/me/tagviews/<id>')
api.add_resource(TagViews, '/me/tagviews')