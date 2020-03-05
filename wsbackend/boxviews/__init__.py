# -*- coding: utf-8 -*-
"""
    web.logitem
    ~~~~~~~~~~

    logitem package
"""

from ..core import Service
from .models import BoxView


class BoxViewService(Service):
    __model__ = BoxView
