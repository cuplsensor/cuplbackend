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

    def get(self):
        """
        Get a list of users.
        Returns:

        """
        return super().get_filtered()



api.add_resource(User, '/user/<id>')
api.add_resource(Users, '/users')
