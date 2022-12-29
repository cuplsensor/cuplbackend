#  A web application that stores samples from a collection of NFC sensors.
#
#  https://github.com/cuplsensor/cuplbackend
#
#  Original Author: Malcolm Mackay
#  Email: malcolm@plotsensor.com
#  Website: https://cupl.co.uk
#
#  Copyright (c) 2021. Plotsensor Ltd.
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License
#  as published by the Free Software Foundation, either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the
#  GNU Affero General Public License along with this program.
#  If not, see <https://www.gnu.org/licenses/>.

from ..core import db
from ..baseschema import BaseSchema
from .models import Capture, CaptureSample, CaptureStatus
from flask import url_for

from marshmallow_sqlalchemy import ModelSchema
from marshmallow import Schema, fields

# http://marshmallow-sqlalchemy.readthedocs.io/en/latest/recipes.html

__all__ = ['CaptureSchema', 'ConsumerCaptureSchema', 'ConsumerCaptureSchemaWithSamples', 'CaptureStatusSchema', 'CaptureSampleSchema']


class CaptureStatusSchema(ModelSchema):
    """
    Schema for serialising a :py:class:`CaptureStatus` model instance.
    """
    class Meta:
        model = CaptureStatus
        sqla_session = db.session
        strict = True


class CaptureSampleSchema(ModelSchema):
    """
    Schema for serialising a :py:class:`CaptureSample` model instance.

    The POSIX timestamp is excluded.
    """
    class Meta:
        model = CaptureSample
        sqla_session = db.session
        exclude = ('timestampPosix',)
        strict = True


class CaptureSchema(ModelSchema):
    """
    Schema for serialising a :py:class:`Capture` read from the database.

    This is intended for administrators. Links to other Admin API endpoints are included.
    """
    class Meta:
        model = Capture
        sqla_session = db.session
        strict = True

    def admin_tag_url(self, obj):
        """Produce an absolute URL for the parent tag in the Admin API. """
        return url_for('admintags.tag', id=obj.tag_id, _external=True)

    def admin_capture_url(self, obj):
        """Produce an absolute URL for this capture in the Admin API. """
        return url_for('admincaptures.capture', id=obj.id, _external=True)

    tag_url = fields.Method("admin_tag_url")
    url = fields.Method("admin_capture_url")
    tag_id = fields.Integer()
    status = fields.Nested(CaptureStatusSchema)
    samples = fields.Nested(CaptureSampleSchema, many=True, load_only=True)


class ConsumerCaptureSchema(CaptureSchema):
    """
    Schema for serialising a :py:class:`Capture`, which excludes the ID of the parent tag.

    Includes a link to download samples for this capture, which saves bandwidth.
    """
    class Meta(CaptureSchema.Meta):
        exclude = ('samples', 'tag_id', 'parent_tag')

    def consumer_tag_url(self, obj):
        """Produce an absolute URL for the parent tag in the Consumer API. """
        return url_for('tags.tag', serial=obj.tagserial, _external=True)

    def consumer_capture_url(self, obj):
        """Produce an absolute URL for this capture in the Consumer API. """
        return url_for('captures.capture', id=obj.id, _external=True)

    def consumer_capturesamples_url(self, obj):
        """Produce an absolute URL for the list of samples associated with this capture. """
        return url_for('samples.capturesamples', id=obj.id, _external=True)

    tagserial = fields.String()
    tag_url = fields.Method("consumer_tag_url")
    url = fields.Method("consumer_capture_url")
    samples_url = fields.Method("consumer_capturesamples_url")


class ConsumerCaptureSchemaWithSamples(ConsumerCaptureSchema):
    """
    Schema for serialising a :py:class:`Capture`, including tag status information and a list of samples.
    """
    class Meta(CaptureSchema.Meta):
        exclude = ('tag_id', 'parent_tag')
    status = fields.Nested(CaptureStatusSchema)
    samples = fields.Nested(CaptureSampleSchema, many=True)









