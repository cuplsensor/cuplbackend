# -*- coding: utf-8 -*-
"""
    web.locations
    ~~~~~~~~~~

    locations package
"""

from ..core import Service
from .models import Location
from flask import current_app
from datetime import datetime


class LocationService(Service):
    __model__ = Location

    def create(self, capturesample, description):
        """Returns a new, saved instance of the capture model class.
        :param **kwargs: instance parameters
        """
        timestamp = datetime.utcnow()

        # Call base class constructor. By committing to the db we get an id.
        location = super().create(capturesample=capturesample,
                                  timestamp=timestamp,
                                  description=description)

        # Assign serial to the tag and commit to the db.
        return location
