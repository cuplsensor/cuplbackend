from functools import wraps
from ..baseresource import SingleResource, MultipleResource
from .tagtokenauth import requires_tagtoken
from ...services import tags


def lookup_webhook_id(f):
    """Get id of the webhook attached to this tag.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        tagobj = tags.get_by_serial(kwargs['serial'])
        del kwargs['serial']
        webhook_id = tagobj.webhook.id
        return f(*args, id=webhook_id, **kwargs)

    return decorated


class TagTokenSingleResource(SingleResource):
    method_decorators = [requires_tagtoken]


class TagTokenMultipleResource(MultipleResource):
    method_decorators = [requires_tagtoken]