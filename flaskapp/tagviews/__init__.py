# -*- coding: utf-8 -*-
"""
    web.logitem
    ~~~~~~~~~~

    logitem package
"""

from ..core import Service
from .models import TagView


class TagViewService(Service):
    __model__ = TagView
