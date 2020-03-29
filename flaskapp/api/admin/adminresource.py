from ..baseresource import SingleResource, MultipleResource
from .admintokenauth import requires_admin_token
from flask import request, jsonify
from marshmallow import ValidationError


class SingleAdminResource(SingleResource):
    method_decorators = [requires_admin_token]


class MultipleAdminResource(MultipleResource):
    method_decorators = [requires_admin_token]

    def post(self):
        """Instantiate a model instance and return it."""
        # Parse the data attribute as JSON.
        jsondata = request.get_json()
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

