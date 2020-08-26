# -*- coding: utf-8 -*-
"""
    web.captures
    ~~~~~~~~~~

    captures package
"""

from ..core import Service
from .models import Capture, CaptureSample, CaptureStatus
from wscodec.decoder.decoderfactory import decode
from wscodec.decoder.hdc2021 import Temp_URL, TempRH_URL


class CaptureService(Service):
    __model__ = Capture

    def decode_and_create(self, tagobj, statb64, timeintb64, circb64, vfmtb64, userobj=None):
        """Returns a new, saved instance of the capture model class.
        :param **kwargs: instance parameters
        """
        decodedurl = decode(secretkey=tagobj.secretkey,
                            statb64=statb64,
                            timeintb64=timeintb64,
                            circb64=circb64,
                            vfmtb64=vfmtb64,
                            usehmac=True)

        resetcause = decodedurl.status.resetcause

        if type(decodedurl) == TempRH_URL:
            samples = [CaptureSample(sample.timestamp, sample.temp, sample.rh) for sample in decodedurl.samples]
        else:
            samples = [CaptureSample(sample.timestamp, sample.temp) for sample in decodedurl.samples]

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
                                 version=0,
                                 timeintmins=decodedurl.timeintmins_int,
                                 md5=decodedurl.hash,
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
               version,
               timeintmins,
               md5,
               samples):



        # Call base class constructor. By committing to the db we get an id.
        capture = super().create(tag_id=tagobj.id,
                                 timestamp=timestamp,
                                 loopcount=loopcount,
                                 status=status,
                                 batvoltagemv=batvoltagemv,
                                 cursorpos=cursorpos,
                                 version=version,
                                 timeintmins=timeintmins,
                                 md5=md5,
                                 samples=samples)

        return capture


class CaptureSampleService(Service):
    __model__ = CaptureSample
