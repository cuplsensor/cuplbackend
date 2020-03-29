# Inspired by overholt
"""
    flaskapp.api.admin.users
    ~~~~~~~~~~~~~~

    User endpoints
"""

from flask import Blueprint, request, jsonify, current_app
from flask_restful import Api, abort, reqparse
from ...services import users
from ...users.schemas import UserSchema
from ...core import ma
from marshmallow import fields, ValidationError
from .adminresource import SingleAdminResource, MultipleAdminResource


bp = Blueprint('adminusers', __name__)
api = Api(bp)


class User(SingleAdminResource):
    """Get, modify or delete one box. """
    def __init__(self):
        super().__init__(UserSchema, users)


class Users(MultipleAdminResource):
    def __init__(self):
        super().__init__(UserSchema, users)

    def post(self):
        """
        Create a user
        """
        jsondata = request.get_json()
        schema = self.Schema()
        try:
            schemaobj = schema.load(jsondata)
        except ValidationError as err:
            return err.messages, 422

        schemaobj = self.service.save(schemaobj)

        return schema.dump(schemaobj)


api.add_resource(User, '/user/<id>')
api.add_resource(Users, '/users')
