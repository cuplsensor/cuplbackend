# Inspired by overholt
"""
    flaskapp.api.admin.tags
    ~~~~~~~~~~~~~~

    Tag endpoints
"""

from flask import Blueprint, request, jsonify
from flask_restful import Api, abort
from ...services import tags, users
from ...tags.schemas import ConsumerTagSchema
from ..baseresource import SingleResource
from .userresource import SingleUserResource


bp = Blueprint('consumertags', __name__)
api = Api(bp)


class Tag(SingleResource):
    """Get, modify or delete one tag. """
    def __init__(self):
        super().__init__(ConsumerTagSchema, tags)

    def get(self, serial):
        """
        Get a tag by its serial.
        """
        tagobj = tags.get_by_serial(serial)

        schema = self.Schema()
        result = schema.dump(tagobj)

        return jsonify(result)


class HasScannedTag(SingleUserResource):
    """Get, modify or delete one tag. """
    def __init__(self):
        super().__init__(ConsumerTagSchema, tags)

    def get(self, usertoken, serial):
        """
        Has a tag with a given serial been scanned by the current user?
        """
        decodedtoken = usertoken['decoded']
        oauth_id = decodedtoken['sub']
        userobj = users.get_by_oauth_id(oauth_id=oauth_id)

        # Check that the user has scanned this tag
        result = userobj.has_scanned_tag(serial)

        return jsonify(result)


api.add_resource(Tag, '/tag/<serial>')
api.add_resource(HasScannedTag, '/tag/<serial>/scanned')
