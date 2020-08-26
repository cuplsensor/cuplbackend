# -*- coding: utf-8 -*-
"""
    overholt.services
    ~~~~~~~~~~~~~~~~~
    services module
"""

from .captures import CaptureService, CaptureSampleService
from .tags import TagService

tags = TagService()
captures = CaptureService()
capturesamples = CaptureSampleService()
