# -*- coding: utf-8 -*-
"""
    web.schemas
    ~~~~~~~~~

    consolidated schemas module
"""

from .boxes.schemas import *
from .captures.schemas import *
from .locations.schemas import *
from .boxviews.schemas import *
from marshmallow import fields

class BoxViewNestedSchema(BoxViewSchema):
    box = fields.Nested(BoxSchema, only=('id', 'serial'))
