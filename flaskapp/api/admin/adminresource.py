from ..baseresource import SingleResource, MultipleResource
from .admintokenauth import requires_admin_token
from flask import request, jsonify


class SingleAdminResource(SingleResource):
    method_decorators = [requires_admin_token]


class MultipleAdminResource(MultipleResource):
    method_decorators = [requires_admin_token]

