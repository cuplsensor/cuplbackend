from ..baseresource import SingleResource, MultipleResource
from .admintokenauth import requires_admin_token
from flask import request, jsonify


class SingleAdminResource(SingleResource):
    method_decorators = [requires_admin_token]


class MultipleAdminResource(MultipleResource):
    method_decorators = [requires_admin_token]

    def get_filtered(self, reqfilterlist=[], optfilterlist=[]):
        """
        Get a list of resources filtered by requiredlist and optionally by optlist.
        Returns:

        """
        optlist = ['offset', 'limit']
        optlist.extend(optfilterlist)

        parsedargs = super().parse_body_args(request.args.to_dict(), requiredlist=reqfilterlist, optlist=optlist)

        offset = parsedargs.get('offset', 0)
        limit = parsedargs.get('limit', None)

        filters = dict()

        for optfilter in optfilterlist:
            optval = parsedargs.get(optfilter, None)
            if optval is not None:
                filters.update({optfilter: optval})

        for reqfilter in reqfilterlist:
            reqval = parsedargs.get(reqfilter)
            if reqval is not None:
                filters.update({reqfilter: reqval})

        resourcelist = self.service.find(**filters).order_by(self.service.__model__.id.desc()).offset(offset).limit(
            limit)

        schema = self.Schema()
        result = schema.dump(resourcelist, many=True)
        return jsonify(result)