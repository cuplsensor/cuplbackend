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
