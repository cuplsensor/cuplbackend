# Inspired by overholt
"""
    flaskapp.api.consumer.webhooks
    ~~~~~~~~~~~~~~

    Webhook endpoints
"""

from flask import Blueprint, request, jsonify, make_response
from flask_restful import Api, abort
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from ...services import tags, webhooks
from ...webhooks.schemas import ConsumerWebhookSchema
from ..baseresource import SingleResource
from .tagtokenresource import TagTokenSingleResource, lookup_webhook_id, requires_tagtoken


bp = Blueprint('consumerwebhooks', __name__)
api = Api(bp)


class Webhook(SingleResource):
    """Get, delete or post one webhook. """
    def __init__(self):
        super().__init__(ConsumerWebhookSchema, webhooks)

    @requires_tagtoken
    @lookup_webhook_id
    def get(self, id):
        return super().get(id)

    @requires_tagtoken
    @lookup_webhook_id
    def delete(self, id):
        return super().delete(id)

    @requires_tagtoken
    def post(self, serial):
        # Get id of the tag
        tag_id = tags.get_by_serial(serial).id
        # Parse the data attribute as JSON.
        jsondata = request.get_json()
        # Append tag_id from the path
        jsondata['tag_id'] = tag_id
        # Create a schema for one model instance.
        schema = self.Schema()
        # Load schema with the JSON data
        try:
            schemaobj = schema.load(jsondata)
        except ValidationError as err:
            return err.messages, 422

        try:
            schemaobj = self.service.save(schemaobj)
        except IntegrityError as e:
            return make_response(jsonify(ecode=107, description=str(e)), 409)

        # Populate schema with the new model instance and return it.
        return schema.dump(schemaobj)


api.add_resource(Webhook, '/tag/<serial>/webhook')
