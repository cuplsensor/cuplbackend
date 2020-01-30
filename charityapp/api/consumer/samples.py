# Inspired by overholt
"""
    charityapp.api.consumer.samples
    ~~~~~~~~~~~~~~

    Samples endpoints
"""

from flask import Blueprint, request, jsonify, current_app
from flask_restful import Api, abort
from ...services import boxes, captures, capturesamples
from ...captures.schemas import CaptureSampleSchema
from ..baseresource import BaseResource, MultipleResource
from dateutil.parser import parse

bp = Blueprint('consumersamples', __name__)
api = Api(bp)


class CaptureSamples(MultipleResource):
    """Get, modify or delete one box. """

    def __init__(self):
        super().__init__(CaptureSampleSchema, None)

    def get(self, id):
        """
        Get samples for a capture.
        """
        capt = captures.get_or_404(id)
        parsedargs = CaptureSamples.parse_body_args(request.args.to_dict(),
                                                    optlist=['offset', 'limit'])

        offset = parsedargs.get('offset', 0)
        limit = parsedargs.get('limit', None)
        samples = capturesamples.find(capture_id=capt.id).order_by("timestamp desc").offset(offset).limit(limit)

        schema = self.Schema()
        result = schema.dump(samples, many=True).data

        return jsonify(result)


class Samples(BaseResource):
    """Get, modify or delete one box. """

    def __init__(self):
        super().__init__(CaptureSampleSchema, None)

    def get(self):
        """
        Get unique samples for a box in a given time range
        """
        parsedargs = Samples.parse_body_args(request.args.to_dict(),
                                             requiredlist=['serial', 'starttimestr', 'endtimestr'],
                                             optlist=['offset', 'limit'])

        serial = parsedargs['serial']
        starttimestr = parsedargs['starttimestr']
        endtimestr = parsedargs['endtimestr']
        offset = parsedargs.get('offset', 0)
        limit = parsedargs.get('limit', None)

        if offset is None:
            offset = 0

        boxobj = boxes.get_by_serial(serial)
        starttime = parse(starttimestr)
        endtime = parse(endtimestr)

        samples = boxobj.uniquesampleswindow(starttime, endtime, offset, limit)

        current_app.logger.info(samples)

        schema = self.Schema()
        result = schema.dump(samples, many=True).data

        return jsonify(result)


api.add_resource(CaptureSamples, '/captures/<id>/samples')
api.add_resource(Samples, '/samples')
