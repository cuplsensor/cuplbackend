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
    __model__ = Capture

    def decode_and_create(self, tagobj, statb64, timeintb64, circb64, vfmtb64):
        """Returns a new, saved instance of the capture model class.
        :param **kwargs: instance parameters
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

        # Assign serial to the tag and commit to the db.
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
    __model__ = CaptureSample
