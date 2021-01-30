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

from ..core import ma
from .models import Tag
from marshmallow import fields
from flask import url_for
from ..webhooks.schemas import WebhookSchema

__all__ = ['TagSchema', 'ConsumerTagSchema']


class TagSchema(ma.ModelSchema):
    class Meta:
        model = Tag
        exclude = ('captures',)

    def admin_tag_url(self, obj):
        return url_for('admintags.tag', id=obj.id, _external=True)

    def admin_captures_url(self, obj):
        return url_for('admincaptures.captures', tag_id=obj.id, _external=True)

    def admin_simulate_url(self, obj):
        return url_for('admintags.tagsimulate', id=obj.id, _external=True)

    url = fields.Method("admin_tag_url")
    captures_url = fields.Method("admin_captures_url")
    simulate_url = fields.Method("admin_simulate_url")
    webhook = fields.Nested(WebhookSchema)


class ConsumerTagSchema(ma.ModelSchema):
    class Meta:
        model = Tag
        exclude = ('secretkey', 'captures', 'id',)
        dump_only = ('timeregistered', 'id', 'secretkey', 'usehmac', 'serial')

    def consumer_tag_url(self, obj):
        return url_for('tags.tag', serial=obj.serial, _external=True)

    def consumer_captures_url(self, obj):
        return url_for('captures.captures', serial=obj.serial, _external=True)

    def consumer_samples_url(self, obj):
        return url_for('samples.samples', serial=obj.serial, _external=True)

    def consumer_webhook_url(self, obj):
        return url_for('webhooks.webhook', serial=obj.serial, _external=True)

    url = fields.Method("consumer_tag_url")
    captures_url = fields.Method("consumer_captures_url")
    samples_url = fields.Method("consumer_samples_url")
    webhook_url = fields.Method("consumer_webhook_url")
