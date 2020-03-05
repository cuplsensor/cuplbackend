# -*- coding: utf-8 -*-
"""
Created on 29 July 2012
@author: Lisa Simpson
"""

"""
    web.boxes
    ~~~~~~~~~~

    boxes package
"""

from ..core import Service
from .models import Box

from hashids import Hashids
from flask import current_app

from random import getrandbits
import base64

class BoxDecodeFailedError(Exception):
    """ Box Decode Failed Error

    The box serial number did not decode to the box id
    """
    def __init__(self, boxid, serial, decoded):
        self.description = "Box serial number {} for box id {} decodes to {}".format(serial, boxid, decoded)
    def __str__(self):
        return self.description

class BoxService(Service):
    __model__ = Box
    hashids = Hashids(min_length=8, salt="this is my salt")

    def get_by_serial(self, serial):
        """Return the first instance of a box in the database with
        with the given serial.
        There will only be one because because serial is unique.
        :param serial: 6 character base 32 serial number
        """
        return self.first_or_404(serial=serial)

    def gen_secret_key(self):
        """Generate a random secret key.
        """
        bitsperbyte = 8
        skeyintlenbytes = 6
        # Generate a random integer of 6 bytes * 8 bits.
        skeyint = getrandbits(bitsperbyte*skeyintlenbytes)
        # Convert the random integer into a bytes object
        skeybytes = skeyint.to_bytes(skeyintlenbytes, byteorder='big')
        # Convert the bytes object into a base 64 string.
        skeyb64 = base64.urlsafe_b64encode(skeybytes)
        return skeyb64.decode("utf-8")

    def create(self, **kwargs):
        """Returns a new, saved instance of the box model class.
        :param **kwargs: instance parameters
        """
        # Call base class constructor. By committing to the db we get an id.
        box = super().create(**kwargs)
        # Generate a serial from the id.
        serial = self.hashids.encode(box.id)
        # Make sure that the serial decodes back to the id
        serialdecoded = self.hashids.decode(serial)[0]
        if (box.id != serialdecoded):
            raise BoxDecodeFailedError(box.id, serial, serialdecoded)

        if 'serial' in kwargs:
            serialb64 = kwargs['serial']
        else:
            serialb64 = serial

        # Generate a secret key base64 string.
        if 'secretkey' in kwargs:
            seckeyb64 = kwargs['secretkey']
        else:
            seckeyb64 = self.gen_secret_key()

        # Assign serial to the box and commit to the db.
        return super().update(box, serial=serialb64, secretkey=seckeyb64)
