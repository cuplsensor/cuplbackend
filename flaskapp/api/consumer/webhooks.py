# Inspired by overholt
"""
    flaskapp.api.consumer.webhooks
    ~~~~~~~~~~~~~~

    Webhook endpoints
"""

from flask import Blueprint, request, jsonify
from flask_restful import Api, abort
from ...services import tags
from ...webhooks.schemas import ConsumerWebhookSchema
from .tagtokenresource import TagTokenSingleResource
from marshmallow import ValidationError


bp = Blueprint('consumerwebhooks', __name__)
api = Api(bp)


class Webhook(TagTokenSingleResource):
    """Get, delete or post one webhook. """
    def __init__(self):
        super().__init__(ConsumerWebhookSchema, tags)

    def post(self, serial: str):
        # Get id of the tag
        tagobj = tags.get_by_serial(serial)
        tag_id = tagobj.id
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

        schemaobj = self.service.save(schemaobj)
        # Populate schema with the new model instance and return it.
        return schema.dump(schemaobj)


api.add_resource(Webhook, '/tag/<serial>/webhook')
