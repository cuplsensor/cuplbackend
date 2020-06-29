# -*- coding: utf-8 -*-
"""
    web.schemas
    ~~~~~~~~~

    consolidated schemas module
"""

from .tags.schemas import *
from .captures.schemas import *
from .locations.schemas import *
from .tagviews.schemas import *
from marshmallow import fields

class TagViewNestedSchema(TagViewSchema):
    tag = fields.Nested(TagSchema, only=('id', 'serial'))
