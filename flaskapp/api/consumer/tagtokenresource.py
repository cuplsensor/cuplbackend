from ..baseresource import SingleResource, MultipleResource
from .tagtokenauth import requires_tagtoken


class TagTokenSingleResource(SingleResource):
    method_decorators = [requires_tagtoken]


class TagTokenMultipleResource(MultipleResource):
    method_decorators = [requires_tagtoken]