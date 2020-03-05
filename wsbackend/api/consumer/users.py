"""
    charityapp.api.admin.token
    ~~~~~~~~~~~~~~

    Token endpoints
"""

from flask import Flask, Blueprint, request, current_app, jsonify
from flask_restful import Resource, Api, abort, reqparse
import os
from ...services import users
from ...users.schemas import UserSchema
from .userresource import SingleUserResource, MultipleUserResource
from .usertokenauth import get_userinfo
from requests import post
import json
import traceback
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

bp = Blueprint('users', __name__)
api = Api(bp)


class Me(SingleUserResource):
    def __init__(self):
        super().__init__(UserSchema, users)

    def get(self, usertoken):
        """
        Get current user from the Auth0 access token.
        """

        # oauth_id is in the sub claim of the decoded token
        decodedtoken = usertoken['decoded']
        oauth_id = decodedtoken['sub']

        # Look up a user by oauth_id
        try:
            userobj = self.service.get_by_oauth_id(oauth_id)
        except NoResultFound:
            abort(404, description="User does not exist")

        userinfo = get_userinfo(access_token=usertoken['token'])
        schema = self.Schema()
        result = schema.dump(userobj)
        result['userinfo'] = userinfo
        response = jsonify(result)
        response.status_code = 200
        return response

    def delete(self, usertoken):
        """
        Delete current user.
        """
        decodedtoken = usertoken['decoded']
        oauth_id = decodedtoken['sub']
        userobj = self.service.get_by_oauth_id(oauth_id)
        try:
            self.service.delete(userobj)
        except ValueError:
            abort(404, description=traceback.format_exc(limit=1, chain=False))
        # 204 Response
        return '', 204


class Users(MultipleUserResource):
    def __init__(self):
        super().__init__(UserSchema, users)

    def get(self, usertoken):
        return abort(404)

    def post(self, usertoken):
        """
        Create a new user from the Auth0 access token.
        """

        userinfo = get_userinfo(access_token=usertoken['token'])

        # Userinfo is used to create a user object
        try:
            userobj = self.service.create(oauth_id=userinfo['sub'])
        except IntegrityError:
            abort(409, description=traceback.format_exc(limit=1))
        except Exception:
            abort(400, description=traceback.format_exc())

        schema = self.Schema()
        result = schema.dump(userobj)
        result['userinfo'] = userinfo
        response = jsonify(result)
        response.status_code = 201

        return response


api.add_resource(Me, '/me')
api.add_resource(Users, '/users')