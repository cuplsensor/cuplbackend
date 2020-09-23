# Inspired by overholt
"""
    flaskapp.api.consumer.samples
    ~~~~~~~~~~~~~~

    Samples endpoints
"""

from flask import Blueprint, request, jsonify, current_app
from flask_restful import Api, abort
from ...models import CaptureSample
from sqlalchemy import desc
from ...services import tags, captures, capturesamples
from ...captures.schemas import CaptureSampleSchema
from ..baseresource import BaseResource, SingleResource
from dateutil.parser import parse

bp = Blueprint('consumersamples', __name__)
api = Api(bp)


class CaptureSamples(SingleResource):
    """Get, modify or delete one tag. """

    def __init__(self):
        super().__init__(CaptureSampleSchema, None)

    def get(self, id):
        """
        Get samples for a capture.
        """
        capt = captures.get_or_404(id)
        parsedargs = CaptureSamples.parse_body_args(request.args.to_dict(),
                                                    optlist=['page', 'per_page'])

        page = int(parsedargs.get('page', 1))
        per_page = int(parsedargs.get('per_page', 100))
        samplesquery = capturesamples.find(capture_id=capt.id).order_by(desc(CaptureSample.timestamp))
        samplespages = samplesquery.paginate(page=page, per_page=per_page, max_per_page=3000)
        sampleslist = samplespages.items

        schema = self.Schema()
        result = schema.dump(sampleslist, many=True)

        return jsonify(result)

    def delete(self, id):
        abort(404)


class Samples(BaseResource):
    """Get, modify or delete one tag. """

    def __init__(self):
        super().__init__(CaptureSampleSchema, None)

    def get(self, serial):
        """
        Get unique samples for a tag in a given time range
        """
        parsedargs = Samples.parse_body_args(request.args.to_dict(),
                                             requiredlist=['starttimestr', 'endtimestr'],
                                             optlist=['page', 'per_page'])

        starttimestr = parsedargs['starttimestr']
        endtimestr = parsedargs['endtimestr']
        page = int(parsedargs.get('page', 1))
        per_page = int(parsedargs.get('per_page', 100))

        tagobj = tags.get_by_serial(serial)
        starttime = parse(starttimestr)
        endtime = parse(endtimestr)

        samplesquery = tagobj.uniquesampleswindow(starttime, endtime)
        samplespages = samplesquery.paginate(page=page, per_page=per_page, max_per_page=20000)
        sampleslist = samplespages.items

        schema = self.Schema()
        result = schema.dump(sampleslist, many=True)

        return jsonify(result)


api.add_resource(CaptureSamples, '/captures/<id>/samples')
api.add_resource(Samples, '/tag/<serial>/samples')
