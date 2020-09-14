# -*- coding: utf-8 -*-
"""
    flaskapp.webhook
    ~~~~~~~~~~

    webhook package
"""

from ..core import Service
from .models import Webhook


class WebhookService(Service):
    __model__ = Webhook
