# -*- coding: utf-8 -*-

#  A web application that stores samples from a collection of NFC sensors.
#
#  https://github.com/cuplsensor/cuplbackend
#
#  Original Author: Malcolm Mackay
#  Email: malcolm@plotsensor.com
#  Website: https://cupl.co.uk
#
#  Copyright (c) 2021. Plotsensor Ltd.
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License
#  as published by the Free Software Foundation, either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the
#  GNU Affero General Public License along with this program.
#  If not, see <https://www.gnu.org/licenses/>.

from ..core import Service
from .models import Tag

from hashids import Hashids
from .simsamples import trhsamples
from wscodec.encoder.pyencoder.encoderfactory import encode
from wscodec.decoder.status import BOR_BIT, SVSH_BIT, WDT_BIT, MISC_BIT, LPM5WU_BIT, CLOCKFAIL_BIT
from ..config import HASHIDS_SALT, HASHIDS_OFFSET


class TagDecodeFailedError(Exception):
    """ Tag Decode Failed Error

    The tag serial number did not decode to the tag id
    """

    def __init__(self, tagid, serial, decoded):
        self.description = "Tag serial number {} for tag id {} decodes to {}".format(serial, tagid, decoded)

    def __str__(self):
        return self.description


class TagService(Service):
    """Create, find, simulate and delete tags. """
    __model__ = Tag
    hashids = Hashids(min_length=8, salt=HASHIDS_SALT)

    def get_by_serial(self, serial: str) -> Tag:
        """
        Find a :py:class:`Tag` in the database. Raise a 404 :py:exc:`HTTPException` if none exists.

        :param serial: 8 character alphanumeric string.
        :return: The tag.
        """
        return self.first_or_404(serial=serial)

    def create(self, **kwargs) -> Tag:
        """
        Return a new :py:class:`Tag` instance, which is saved into the database.

        :param **kwargs: instance parameters
        :return: The newly created tag.
        """
        # Call base class constructor. By committing to the db we get an id.
        tag = super().create(**kwargs)

        if tag.serial is None:
            # Generate a serial from the id.
            serial = self.hashids.encode(HASHIDS_OFFSET + tag.id)

            # Assign serial to the tag and commit to the db.
            tag = super().update(tag, serial=serial)

        return tag

    def simulate(self,
                 id,
                 frontendurl,
                 nsamples=100,
                 smplintervalmins=10,
                 format=1,
                 usehmac=True,
                 batvoltagemv=3000,
                 bor=False,
                 svsh=False,
                 wdt=False,
                 misc=False,
                 lpm5wu=False,
                 clockfail=False,
                 tagerror=False):
        """ Get URL that would be generated by a tag. """
        # Get tag from the database so we can obtain its serial and secretkey
        tag = self.get(id=id)

        # Disable https if necessary
        spliturl = frontendurl.split('://')
        httpsdisable = False  # Assume https by default

        if spliturl[0] == "http":
            httpsdisable = True
            frontendurl = spliturl[1]  # Remove protocol from the URL
        elif spliturl[0] == "https":
            frontendurl = spliturl[1]   # Remove protocol from the URL

        # Convert battery voltage to an ADC reading
        batteryadc = (256 * 1500) / batvoltagemv
        batteryadc = int(batteryadc)  # It is vital to convert from float to integer. No type checking is done yet.

        # Assemble reset cause bitfield
        resetcause = 0
        if bor:
            resetcause |= BOR_BIT

        if svsh:
            resetcause |= SVSH_BIT

        if wdt:
            resetcause |= WDT_BIT

        if misc:
            resetcause |= MISC_BIT

        if lpm5wu:
            resetcause |= LPM5WU_BIT

        if clockfail:
            resetcause |= CLOCKFAIL_BIT

        # Initialise encoder
        virtualsensor = encode(format=format,
                               baseurl=frontendurl,
                               serial=tag.serial,
                               secretkey=tag.secretkey,
                               smplintervalmins=smplintervalmins,
                               usehmac=usehmac,
                               resetcause=resetcause,
                               resetsalltime=59,
                               batteryadc=batteryadc,
                               httpsdisable=httpsdisable,
                               tagerror=tagerror)

        # Produce a list of simulated samples. Each is a dictionary with temp and rh keys.
        # Also store the time offset from UTC now to the most recent sample.
        trhlist, timeoffsetmins = trhsamples(smplintervalmins=smplintervalmins, nsamples=nsamples)

        # Load samples into wscodec
        virtualsensor.pushsamplelist(trhlist)

        # Update time offset on the virtual sensor in minutes
        virtualsensor.updateendstop(timeoffsetmins)

        # Obtain URL
        urlstr = virtualsensor.get_url()

        return urlstr
