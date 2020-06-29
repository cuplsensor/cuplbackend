# -*- coding: utf-8 -*-
"""
    overholt.services
    ~~~~~~~~~~~~~~~~~
    services module
"""

from .captures import CaptureService, CaptureSampleService
from .tags import TagService
from .users import UserService
from .locations import LocationService
from .tagviews import TagViewService

#: An instance of the :class:`TagService` class
tagviews = TagViewService()

tags = TagService()

captures = CaptureService()
capturesamples = CaptureSampleService()

locations = LocationService()

#: An instance of the :class:`UserService` class
users = UserService()
