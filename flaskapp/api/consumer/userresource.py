from ..baseresource import SingleResource, MultipleResource
from .usertokenauth import requires_user_token


class SingleUserResource(SingleResource):
    method_decorators = [requires_user_token]


class MultipleUserResource(MultipleResource):
    method_decorators = [requires_user_token]