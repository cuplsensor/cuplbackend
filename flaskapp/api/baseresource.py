# Inspired by overholt
"""
    flaskapp.api.baseresource
    ~~~~~~~~~~~~~~

    Base resource from https://marshmallow.readthedocs.io/en/3.0/examples.html
"""

from flask_restful import Resource, abort
from flask import jsonify, current_app, request, url_for
from marshmallow import ValidationError


class BaseResource(Resource):
    """
    Contains class variables common to all resources.
    """
    def __init__(self, Schema, service):
        """
        Constructor for the BaseResource class.
        :param Schema: Marshamallow schema for the model
        associated with the service.
        :param service: for creating and retrieving model instances.
        """
        self.Schema = Schema
        self.service = service

    @staticmethod
    def parse_body_args(requestjson, requiredlist=[], optlist=[]):
        # Obtain capture sample id from the body
        parsed = dict()

        for argname in requiredlist:
            try:
                parsed[argname] = requestjson[argname]
            except (KeyError, TypeError):
                abort(400, message="{} is required".format(argname))

        for argname in optlist:
            try:
                parsed[argname] = requestjson[argname]
            except KeyError:
                pass

        return parsed

    def make_relative_link(self, pageno: int, per_page: int, relstr: str, reqargs: dict):
        reqargs.update(page=pageno)
        reqargs.update(per_page=per_page)
        return '<{}>; rel="{}"'.format(url_for(request.endpoint, **dict(reqargs), _external=True), relstr)

    def make_link_header(self, resourcepages):
        reqargs = dict(request.view_args)
        linkheader = str()
        # First page link
        linkheader += self.make_relative_link(1, resourcepages.per_page, "first", reqargs) + ","
        # Previous page link
        if resourcepages.has_prev:
            linkheader += self.make_relative_link(resourcepages.prev_num, resourcepages.per_page, "prev", reqargs) + ","
        # Next page link
        if resourcepages.has_next:
            linkheader += self.make_relative_link(resourcepages.next_num, resourcepages.per_page, "next", reqargs) + ","
        # Last page link
        linkheader += self.make_relative_link(resourcepages.pages, resourcepages.per_page, "last", reqargs)
        return linkheader


class SingleResource(BaseResource):
    """Get, delete or modify one model instance. """
    def __init__(self, Schema, service):
        super().__init__(Schema, service)

    def get(self, id):
        """
        Return a resource schema for the model instance

        :param id: model instance ID.

        """
        schema = self.Schema()
        modelobj = self.service.get_or_404(id)
        result = schema.dump(modelobj)
        return jsonify(result)

    def delete(self, id):
        """
        Delete a model instance.

        :param id: model instance ID to delete.

        """
        # Obtain a model instance with identity id from the service.
        modelobj = self.service.get_or_404(id)
        # Use the service to delete the model instance.
        self.service.delete(modelobj)
        # 204 Response
        return '', 204


class MultipleResource(BaseResource):
    """Get all model instances or post a new one. """
    def __init__(self, Schema, service):
        super().__init__(Schema, service)

    def get_filtered(self, reqfilterlist=[], optfilterlist=[]):
        """
        Get a list of resources filtered by requiredlist and optionally by optlist.
        Returns:

        """
        optlist = ['page', 'per_page']
        optlist.extend(optfilterlist)

        parsedargs = super().parse_body_args(request.args.to_dict(), requiredlist=reqfilterlist, optlist=optlist)

        page = int(parsedargs.get('page', 1))
        per_page = int(parsedargs.get('per_page', 25))

        filters = dict()

        for optfilter in optfilterlist:
            optval = parsedargs.get(optfilter, None)
            if optval is not None:
                filters.update({optfilter: optval})

        for reqfilter in reqfilterlist:
            reqval = parsedargs.get(reqfilter)
            if reqval is not None:
                filters.update({reqfilter: reqval})

        resourcepages = self.service.find(**filters).order_by(self.service.__model__.id.desc()).paginate(page=page,
                                                                                                         per_page=per_page,
                                                                                                         max_per_page=100)
        resourcelist = resourcepages.items

        schema = self.Schema()
        result = schema.dump(resourcelist, many=True)
        response = jsonify(result)
        # https://github.com/pallets/flask/issues/2111
        linkheader = self.make_link_header(resourcepages)
        response.headers.add('Link', linkheader)
        return response

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

