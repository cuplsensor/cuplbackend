from ..core import db
from ..baseschema import BaseSchema
from .models import Capture, CaptureSample, CaptureStatus

from marshmallow_sqlalchemy import ModelSchema
from marshmallow import Schema, fields

# http://marshmallow-sqlalchemy.readthedocs.io/en/latest/recipes.html

__all__ = ['CaptureSchema', 'ConsumerCaptureSchema', 'ConsumerCaptureSchemaWithSamples', 'CaptureStatusSchema', 'CaptureSampleSchema']


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


class CaptureSchema(ModelSchema):
    class Meta:
        model = Capture
        sqla_session = db.session
        strict = True
    tag_id = fields.Integer()
    status = fields.Nested(CaptureStatusSchema)
    samples = fields.Nested(CaptureSampleSchema, many=True, load_only=True)


class ConsumerCaptureSchemaWithSamples(CaptureSchema):
    class Meta(CaptureSchema.Meta):
        exclude = ('tag_id', 'parent_tag')
    tagserial = fields.String()
    status = fields.Nested(CaptureStatusSchema)
    samples = fields.Nested(CaptureSampleSchema, many=True)


class ConsumerCaptureSchema(CaptureSchema):
    class Meta(CaptureSchema.Meta):
        exclude = ('samples', 'tag_id', 'parent_tag')
    tagserial = fields.String()






