from ..core import db
from .models import Webhook
from flask import url_for
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

# http://marshmallow-sqlalchemy.readthedocs.io/en/latest/recipes.html

__all__ = ['WebhookSchema', 'ConsumerWebhookSchemaWithKey', 'ConsumerWebhookSchema']


class WebhookSchema(ModelSchema):
    class Meta:
        model = Webhook
        sqla_session = db.session
        strict = True

    def admin_tag_url(self, obj):
        return url_for('admintags.tag', id=obj.tag_id, _external=True)

    def admin_webhook_url(self, obj):
        return url_for('adminwebhooks.webhook', id=obj.id, _external=True)

    tag_url = fields.Method("admin_tag_url")
    url = fields.Method("admin_webhook_url")
    tag_id = fields.Integer()
    created_on = fields.DateTime(dump_only=True)


class ConsumerWebhookSchemaWithKey(WebhookSchema):
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
    class Meta(WebhookSchema.Meta):
        exclude = ('parent_tag', 'wh_secretkey',)




