# Inspired by overholt
"""
    flaskapp.api.admin.tags
    ~~~~~~~~~~~~~~

    Tag endpoints
"""

from flask import Blueprint, request, jsonify
from flask_restful import Api, abort
from ...services import tags
from ...tags.schemas import TagSchema
from .adminresource import SingleAdminResource, MultipleAdminResource

bp = Blueprint('admintags', __name__)
api = Api(bp)


class Tag(SingleAdminResource):
    """Get, modify or delete one tag. """

    def __init__(self):
        super().__init__(TagSchema, tags)


class TagSimulate(SingleAdminResource):
    """Get a URL created by the encoder in wscodec. Similar to what the tag will produce. """

    def __init__(self):
        super().__init__(TagSchema, tags)

    def get(self, id):
        """
        Get a URL for simulating the website response to a tag scan.

        Args:
            id: Tag id.

        Returns:
            A URL.
        """
        parsedargs = super().parse_body_args(request.args.to_dict(),
                                             requiredlist=['frontendurl'],
                                             optlist=['nsamples'])

        frontendurl = parsedargs['frontendurl']
        nsamples = int(parsedargs.get('nsamples', 100))

        urlstr = tags.simulate(id, frontendurl, nsamples)
        return urlstr


class Tags(MultipleAdminResource):
    def __init__(self):
        super().__init__(TagSchema, tags)

    def get(self):
        """
        Get a list of tags.
        Returns:

        """
        return super().get_filtered()

    def post(self):
        """
        Create a new tag. It is optional to specify serial, secretkey, fwversion, hwversion and description.
        """
        jsondata = request.get_json(silent=True) or dict()
        parsedargs = super().parse_body_args(jsondata, optlist=['serial',
                                                                'secretkey',
                                                                'fwversion',
                                                                'hwversion',
                                                                'description'])

        tagobj = self.service.create(**parsedargs)
        schema = self.Schema()
        return schema.dump(tagobj)


api.add_resource(Tag, '/tag/<id>')
api.add_resource(Tags, '/tags')
api.add_resource(TagSimulate, '/tag/<id>/simulate')
