# -*- coding: utf-8 -*-
"""
    overholt.services
    ~~~~~~~~~~~~~~~~~
    services module
"""

from .captures import CaptureService, CaptureSampleService
from .boxes import BoxService
from .users import UserService
from .locations import LocationService
from .boxviews import BoxViewService

#: An instance of the :class:`BoxService` class
boxviews = BoxViewService()

boxes = BoxService()

captures = CaptureService()
capturesamples = CaptureSampleService()

locations = LocationService()

#: An instance of the :class:`UserService` class
users = UserService()
