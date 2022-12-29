# -*- coding: utf-8 -*-
"""
    web.captures
    ~~~~~~~~~~

    captures package
"""

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
from .models import Capture, CaptureSample, CaptureStatus
from wscodec.decoder.decoderfactory import decode
from wscodec.decoder.hdc2021 import Temp_URL, TempRH_URL


class CaptureService(Service):
    """Create and find captures for a tag. """
    __model__ = Capture

    def decode_and_create(self, tagobj, statb64, timeintb64, circb64, vfmtb64) -> Capture:
        """
        Decode the URL parameters read from a Tag and use these to create a Capture.

        :param tagobj: The Tag that the cupl URL parameters were read from.
        :param statb64: Base64 encoded tag status information.
        :param timeintb64: Base64 encoded time interval between samples.
        :param circb64: Base64 encoded circular buffer containing temperature and humidity samples.
        :param vfmtb64: Base64 encoded format code.
        :return: A new Capture made from decoded URL parameters.
        """
        decodedurl = decode(secretkey=tagobj.secretkey,
                            usehmac=tagobj.usehmac,
                            statb64=statb64,
                            timeintb64=timeintb64,
                            circb64=circb64,
                            vfmtb64=vfmtb64)

        resetcause = decodedurl.status.resetcause

        typestr = decodedurl.__class__.__name__
        typestrsplit = [a for a in typestr.split('.') if a]
        format = '.'.join(typestrsplit[-2:])
        if format == "TempRH_URL":
            samples = [CaptureSample(sample.timestamp, sample.temp, sample.rh) for sample in decodedurl.samples]
        elif format == "Temp_URL":
            samples = [CaptureSample(sample.timestamp, sample.temp) for sample in decodedurl.samples]
        else:
            raise ValueError(format)

        status = CaptureStatus(resetsalltime=decodedurl.status.resetsalltime,
                               brownout=resetcause['brownout'],
                               supervisor=resetcause['supervisor'],
                               watchdog=resetcause['watchdog'],
                               misc=resetcause['misc'],
                               lpm5wakeup=resetcause['lpm5wakeup'],
                               clockfail=resetcause['clockfail'])

        capture = super().create(tag_id=tagobj.id,
                                 timestamp=decodedurl.scantimestamp,
                                 loopcount=decodedurl.status.loopcount,
                                 status=status,
                                 batvoltagemv=decodedurl.status.get_batvoltagemv(),
                                 cursorpos=decodedurl.endmarkerpos,
                                 format=format,
                                 timeintmins=decodedurl.timeintmins_int,
                                 hash=decodedurl.hash,
                                 samples=samples)

        return capture

    def create(self,
               tagobj,
               timestamp,
               loopcount,
               status,
               batvoltagemv,
               cursorpos,
               format,
               timeintmins,
               hash,
               samples):
        """
        Create a new Capture from unencoded data that are not part of a URL.

        :param tagobj: The Capture will be assigned to this Tag instance.
        :param timestamp: When this capture was created.
        :param loopcount: Number of times the circular buffer cursor has wrapped around from the end to the start.
        :param status: Reference to a CaptureStatus object.
        :param batvoltagemv: Voltage in milliVolts of the battery powering cuplTag.
        :param cursorpos: Position of the circular buffer cursor relative to the start of the string.
        :param format: Indicates how to decode parameters in the cupl URL.
        :param timeintmins: Time interval between samples in minutes.
        :param hash: MD5 or HMAC of Capture data.
        :param samples: A list of CaptureSamples objects.
        :return: A new Capture made from decoded URL parameters.
        """

        # Call base class constructor. By committing to the db we get an id.
        capture = super().create(tag_id=tagobj.id,
                                 timestamp=timestamp,
                                 loopcount=loopcount,
                                 status=status,
                                 batvoltagemv=batvoltagemv,
                                 cursorpos=cursorpos,
                                 format=format,
                                 timeintmins=timeintmins,
                                 hash=hash,
                                 samples=samples)

        return capture


class CaptureSampleService(Service):
    """Create and find timestamped environmental sensor samples. """
    __model__ = CaptureSample
