from ..baseresource import SingleResource, MultipleResource
from .admintokenauth import requires_admin_token

class SingleAdminResource(SingleResource):
    method_decorators = [requires_admin_token]

class MultipleAdminResource(MultipleResource):
    method_decorators = [requires_admin_token]