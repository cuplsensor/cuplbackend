from ..baseresource import SingleResource, MultipleResource
from .hashchecker import requires_capture_hash


class SingleProtectedResource(SingleResource):
    method_decorators = [requires_capture_hash]


class MultipleProtectedResource(MultipleResource):
    method_decorators = [requires_capture_hash]