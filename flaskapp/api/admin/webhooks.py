# Inspired by overholt
"""
    flaskapp.api.admin.webhooks
    ~~~~~~~~~~~~~~

    Webhook endpoints
"""

from flask import Blueprint, request, jsonify, current_app
from flask_restful import Api, abort, reqparse
from sqlalchemy.exc import IntegrityError
from ...services import webhooks
from ...webhooks.schemas import WebhookSchema
from .adminresource import SingleAdminResource, MultipleAdminResource


bp = Blueprint('adminwebhooks', __name__)
api = Api(bp)


class Webhook(SingleAdminResource):
    """Get or delete one webhook. """
    def __init__(self):
        super().__init__(WebhookSchema, webhooks)


class Webhooks(MultipleAdminResource):
    def __init__(self):
        super().__init__(WebhookSchema, webhooks)

    def get(self):
        abort(404)

    def post(self):
        """
        Post a webhook
        :return:
            The newly created webhook or an error code.
        """
        try:
            return super().post()
        except IntegrityError as err:
            return str(err), 409


api.add_resource(Webhook, '/webhook/<id>')
api.add_resource(Webhooks, '/webhooks')
