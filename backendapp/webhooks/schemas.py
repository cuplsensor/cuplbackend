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
from .models import Webhook
from flask import url_for
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

# http://marshmallow-sqlalchemy.readthedocs.io/en/latest/recipes.html

__all__ = ['WebhookSchema', 'ConsumerWebhookSchemaWithKey', 'ConsumerWebhookSchema']


class WebhookSchema(ModelSchema):
    """
    Schema for serialising a :py:class:`Webhook` read from the database.

    This is intended for administrators only.
    """
    class Meta:
        model = Webhook
        sqla_session = db.session
        strict = True

    def admin_tag_url(self, obj):
        """Produce an absolute URL for the parent tag in the Admin API. """
        return url_for('admintags.tag', id=obj.tag_id, _external=True)

    def admin_webhook_url(self, obj):
        """Produce an absolute URL for this webhook in the Admin API. """
        return url_for('adminwebhooks.webhook', id=obj.id, _external=True)

    tag_url = fields.Method("admin_tag_url")
    url = fields.Method("admin_webhook_url")
    tag_id = fields.Integer()
    created_on = fields.DateTime(dump_only=True)


class ConsumerWebhookSchemaWithKey(WebhookSchema):
    """
    Schema for serialising a :py:class:`Webhook`, which excludes the ID of the parent tag, but includes the
    serial string (as used in consumer API endpoints).

    The webhook secret key is part of this schema. It must only be used for POSTing a new webhook.
    """
    class Meta(WebhookSchema.Meta):
        exclude = ('parent_tag',)

    def consumer_tag_url(self, obj):
        return url_for('tags.tag', serial=obj.tagserial, _external=True)

    def consumer_webhook_url(self, obj):
        return url_for('webhooks.webhook', serial=obj.tagserial, _external=True)

    tag_url = fields.Method("consumer_tag_url")
    url = fields.Method("consumer_webhook_url")
    tagserial = fields.String()
    created_on = fields.DateTime(dump_only=True)
    load_only = ('tag_id',)


class ConsumerWebhookSchema(ConsumerWebhookSchemaWithKey):
    """
    A schema identical to :py:class:`ConsumerWebhookSchemaWithKey` but with the webhook secret key omitted.

    This is used for API endpoints that GET information about existing webhooks.
    """
    class Meta(WebhookSchema.Meta):
        exclude = ('parent_tag', 'wh_secretkey',)




