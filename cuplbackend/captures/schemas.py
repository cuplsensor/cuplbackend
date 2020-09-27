from ..core import db
from ..baseschema import BaseSchema
from .models import Capture, CaptureSample, CaptureStatus
from flask import url_for

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

    def admin_tag_url(self, obj):
        return url_for('admintags.tag', id=obj.tag_id, _external=True)

    def admin_capture_url(self, obj):
        return url_for('admincaptures.capture', id=obj.id, _external=True)

    tag_url = fields.Method("admin_tag_url")
    url = fields.Method("admin_capture_url")
    tag_id = fields.Integer()
    status = fields.Nested(CaptureStatusSchema)
    samples = fields.Nested(CaptureSampleSchema, many=True, load_only=True)


class ConsumerCaptureSchema(CaptureSchema):
    class Meta(CaptureSchema.Meta):
        exclude = ('samples', 'tag_id', 'parent_tag')

    def consumer_tag_url(self, obj):
        return url_for('tags.tag', serial=obj.tagserial, _external=True)

    def consumer_capture_url(self, obj):
        return url_for('captures.capture', id=obj.id, _external=True)

    def consumer_capturesamples_url(self, obj):
        return url_for('samples.capturesamples', id=obj.id, _external=True)

    tagserial = fields.String()
    tag_url = fields.Method("consumer_tag_url")
    url = fields.Method("consumer_capture_url")
    samples_url = fields.Method("consumer_capturesamples_url")


class ConsumerCaptureSchemaWithSamples(ConsumerCaptureSchema):
    class Meta(CaptureSchema.Meta):
        exclude = ('tag_id', 'parent_tag')
    status = fields.Nested(CaptureStatusSchema)
    samples = fields.Nested(CaptureSampleSchema, many=True)









