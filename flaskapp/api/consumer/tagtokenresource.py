from functools import wraps
from ..baseresource import SingleResource, MultipleResource
from .tagtokenauth import requires_tagtoken
from ...services import tags


def lookup_webhook_id(f):
    """Get id of the webhook attached to this tag.
    """
    @wraps(f)
    def decorated(serial, *args, **kwargs):
        tagobj = tags.get_by_serial(serial)
        webhook_id = tagobj.webhook.id
        return f(webhook_id, *args, **kwargs)

    return decorated


class TagTokenSingleResource(SingleResource):
    method_decorators = [requires_tagtoken, lookup_webhook_id]


class TagTokenMultipleResource(MultipleResource):
    method_decorators = [requires_tagtoken]