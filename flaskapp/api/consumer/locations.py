# Inspired by overholt
"""
    flaskapp.api.locations
    ~~~~~~~~~~~~~~

    Location endpoints
"""

from flask import Blueprint, request, jsonify, current_app
from flask_restful import Api, abort
from ...services import locations
from ...services import capturesamples
from ...services import tags
from ...services import users
from ...schemas import LocationSchema
from ..baseresource import SingleResource, MultipleResource
from .usertokenauth import requires_user_token
from dateutil.parser import parse

bp = Blueprint('locations', __name__)
api = Api(bp)


class ScanRequiredResource:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_capturesample(self, usertoken, capturesample_id):
        # Get a capturesample after checking the user has scanned the tag that it belongs to.
        current_app.logger.info(usertoken)
        decodedtoken = usertoken['decoded']
        oauth_id = decodedtoken['sub']
        userobj = users.get_by_oauth_id(oauth_id=oauth_id)

        # Find the capturesample object corresponding to capturesample_id
        capturesample = capturesamples.first_or_404(id=capturesample_id)

        # Find the tag owning this capturesample
        parentcapture = capturesample.parent_capture
        parenttag = parentcapture.parent_tag
        tagserial = parenttag.serial

        # Check that the user has scanned this tag
        if userobj.has_scanned_tag(tagserial) is False:
            abort(401, message="the user has not scanned this tag")

        return capturesample


class Location(SingleResource, ScanRequiredResource):
    # Only apply decorator to the POST request.
    method_decorators = {'patch': [requires_user_token],
                         'delete': [requires_user_token]}

    """Get, modify or delete a location. """
    def __init__(self):
        super().__init__(LocationSchema, locations)

    def delete(self, usertoken, id):
        """
        Delete a location
        """
        location = self.service.get_or_404(id)
        capturesample = location.parent_capturesample
        capturesample_id = capturesample.id

        # Check that we can edit this location
        self.get_capturesample(usertoken, capturesample_id)
        return super().delete(id=id)

    def patch(self, usertoken, id):
        """
        Edit location information for a tag
        """
        location = self.service.get_or_404(id)
        capturesample = location.parent_capturesample
        capturesample_id = capturesample.id

        # Check that we can edit this location
        self.get_capturesample(usertoken, capturesample_id)

        parsedargs = Location.parse_body_args(request.get_json(), optlist=['description'])

        description = parsedargs['description']

        if description is not None:
            location = locations.update(location, description=description)

        result = self.Schema().dump(location)
        return jsonify(result)


class Locations(MultipleResource, ScanRequiredResource):
    # Only apply decorator to the POST request.
    method_decorators = {'post': [requires_user_token]}
    """Get all locations or post a new one. """
    def __init__(self):
        super().__init__(LocationSchema, locations)

    def post(self, usertoken):
        """
        Add location information to a tag
        """

        # Obtain capture sample id from the body
        req = request.get_json()

        capturesample_id = req.get('capturesample_id')
        description = req.get('description')

        if capturesample_id is None:
            abort(400, message="capturesample_id required")

        if description is None:
            abort(400, message="description required")

        capturesample = self.get_capturesample(usertoken, capturesample_id)

        # Create the location
        location = self.service.create(capturesample=capturesample, description=description)

        # Dump location into the JSON schema
        schema = self.Schema()
        result = schema.dump(location)

        current_app.logger.info(location)
        current_app.logger.info(result)

        return jsonify(result)

    def get(self):
        """
        Get a list of locations for a tag ordered by most recent
        """
        tagserial = request.args.get('tagserial')
        starttimestr = request.args.get('starttime')
        endtimestr = request.args.get('endtime')
        kwargs = dict()

        if starttimestr is not None:
            kwargs['starttime'] = parse(starttimestr)

        if endtimestr is not None:
            kwargs['endtime'] = parse(endtimestr)

        if tagserial is None:
            abort(400, message="tagserial is required")

        # Obtain a tag object
        tag = tags.get_by_serial(tagserial)

        # Get a list of timestamped locations for this tag
        locationslist = tag.locations_in_window(**kwargs)
        current_app.logger.info(locationslist)

        # Dump location into the JSON schema
        schema = self.Schema()
        result = schema.dump(locationslist, many=True)

        return jsonify(result)


api.add_resource(Location, '/locations/<id>')
api.add_resource(Locations, '/locations')
