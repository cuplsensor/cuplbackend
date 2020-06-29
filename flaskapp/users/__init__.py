# -*- coding: utf-8 -*-
"""
    web.users
    ~~~~~~~~~~

    users package
"""

from ..core import Service, db
from .models import User
from datetime import datetime


class UserNotFoundError(Exception):
    """ User Not Found Error

    This is raised when there is no User with a given shortname in the database
    """
    def __init__(self):
        self.description = "No user in the Users table "

    def __str__(self):
        return self.description


class UserService(Service):
    __model__ = User

    def create(self, oauth_id, timeregistered=None):
        # Populate time registered with the time now if none is provided
        if timeregistered is None:
            timeregistered = datetime.utcnow()
        # Call base class constructor. By committing to the db we get an id.
        user = super().create(oauth_id=oauth_id,
                              timeregistered=timeregistered)

        # Assign serial to the tag and commit to the db.
        return user

    def identity(self, token):
        """Find a user object from the credentials inside a decoded token."""
        oauthid = token['oauth_id']
        userquery = db.session.query(User).filter(User.oauth_id == oauthid)
        userobj = userquery.scalar()
        if userobj is None:
            raise UserNotFoundError()
        return userobj

    def authenticate(self, username, password):
        """We do not use the authentication feature of Flask JWT.

        but this is required anyway.
        """
        return None

    def get_by_oauth_id(self, oauth_id):
        """Return the first instance of a tag in the database with
        with the given serial.
        There will only be one because because serial is unique.
        :param serial: 6 character base 32 serial number
        """
        return self.first_or_404(oauth_id=oauth_id)