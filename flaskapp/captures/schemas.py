from ..core import db
from ..baseschema import BaseSchema
from .models import Capture, CaptureSample, CaptureStatus
from ..locations.schemas import LocationSchema

from marshmallow_sqlalchemy import ModelSchema
from marshmallow import Schema, fields

# http://marshmallow-sqlalchemy.readthedocs.io/en/latest/recipes.html

__all__ = ['CaptureSchema', 'ConsumerCaptureSchema', 'CaptureStatusSchema', 'CaptureSampleSchema']


class CaptureStatusSchema(ModelSchema):
    class Meta:
        model = CaptureStatus
        sqla_session = db.session
        strict = True


class CaptureSampleSchema(ModelSchema):
    class Meta:
        model = CaptureSample
        sqla_session = db.session
        exclude = ('timestampPosix',)
        strict = True
    location = fields.Nested(LocationSchema)


class CaptureSchema(ModelSchema):
    class Meta:
        model = Capture
        sqla_session = db.session
        strict = True
    box_id = fields.Integer()
    user_id = fields.Integer(missing=None)
    status = fields.Nested(CaptureStatusSchema)
    samples = fields.Nested(CaptureSampleSchema, many=True, load_only=True)


class ConsumerCaptureSchema(CaptureSchema):
    class Meta(CaptureSchema.Meta):
        exclude = ('samples', 'box_id', 'parent_box')
    boxserial = fields.String()






