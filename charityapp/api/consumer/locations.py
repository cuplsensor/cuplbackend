# Inspired by overholt
"""
    charityapp.api.locations
    ~~~~~~~~~~~~~~

    Location endpoints
"""

from flask import Blueprint, request, jsonify, current_app
from flask_restful import Api, abort
from ...services import locations
from ...services import capturesamples
from ...services import boxes
from ...services import users
from ...forms import AddLocationForm, EditLocationForm
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
        # Get a capturesample after checking the user has scanned the box that it belongs to.
        current_app.logger.info(usertoken)
        decodedtoken = usertoken['decoded']
        oauth_id = decodedtoken['sub']
        userobj = users.get_by_oauth_id(oauth_id=oauth_id)

        # Find the capturesample object corresponding to capturesample_id
        capturesample = capturesamples.first_or_404(id=capturesample_id)

        # Find the box owning this capturesample
        parentcapture = capturesample.parent_capture
        parentbox = parentcapture.parent_box
        boxserial = parentbox.serial

        # Check that the user has scanned this box
        if userobj.has_scanned_box(boxserial) is False:
            abort(401, message="the user has not scanned this box")

        return capturesample


class Location(SingleResource, ScanRequiredResource):
    # Only apply decorator to the POST request.
    method_decorators = {'patch': [requires_user_token],
                         'delete': [requires_user_token]}

    """Get, modify or delete a location. """
    def __init__(self):
        super().__init__(LocationSchema, locations)

    def get(self, id):
        """
        Get a list of locations for a box ordered by most recent
        """
        return super().get(modelid=id)

    def delete(self, usertoken, id):
        """
        Delete a location
        """
        location = self.service.get_or_404(id)
        capturesample = location.parent_capturesample
        capturesample_id = capturesample.id

        # Check that we can edit this location
        self.get_capturesample(usertoken, capturesample_id)
        return super().delete(modelid=id)

    def patch(self, usertoken, id):
        """
        Edit location information for a box
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

        result = self.Schema().dump(location).data
        return jsonify(result)


class Locations(MultipleResource, ScanRequiredResource):
    # Only apply decorator to the POST request.
    method_decorators = {'post': [requires_user_token]}
    """Get all locations or post a new one. """
    def __init__(self):
        super().__init__(LocationSchema, locations)

    def post(self, usertoken):
        """
        Add location information to a box
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
        result = schema.dump(location).data

        current_app.logger.info(location)
        current_app.logger.info(result)

        return jsonify(result)

    def get(self):
        """
        Get a list of locations for a box ordered by most recent
        """
        boxserial = request.args.get('boxserial')
        starttimestr = request.args.get('starttime')
        endtimestr = request.args.get('endtime')
        kwargs = dict()

        if starttimestr is not None:
            kwargs['starttime'] = parse(starttimestr)

        if endtimestr is not None:
            kwargs['endtime'] = parse(endtimestr)

        if boxserial is None:
            abort(400, message="boxserial is required")

        # Obtain a box object
        box = boxes.get_by_serial(boxserial)

        # Get a list of timestamped locations for this box
        locationslist = box.locations_in_window(**kwargs)
        current_app.logger.info(locationslist)

        # Dump location into the JSON schema
        schema = self.Schema()
        result = schema.dump(locationslist, many=True).data

        return jsonify(result)


api.add_resource(Location, '/locations/<id>')
api.add_resource(Locations, '/locations')
