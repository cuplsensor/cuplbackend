# -*- coding: utf-8 -*-
"""
    web.captures
    ~~~~~~~~~~

    captures package
"""

from ..core import Service
from .models import Capture, CaptureSample, CaptureStatus
from wscodec.decoder.decoderfactory import decode


class CaptureService(Service):
    __model__ = Capture

    def decode_and_create(self, boxobj, statb64, timeintb64, circb64, ver, userobj=None):
        """Returns a new, saved instance of the capture model class.
        :param **kwargs: instance parameters
        """
        decodedurl = decode(secretkey=boxobj.secretkey,
                            statb64=statb64,
                            timeintb64=timeintb64,
                            circb64=circb64,
                            ver=ver,
                            usehmac=True)

        resetcause = decodedurl.status.resetcause

        samples = [CaptureSample(sample.timestamp, sample.temp, sample.rh) for sample in decodedurl.samples]

        status = CaptureStatus(resetsalltime=decodedurl.status.resetsalltime,
                               brownout=resetcause['brownout'],
                               supervisor=resetcause['supervisor'],
                               watchdog=resetcause['watchdog'],
                               misc=resetcause['misc'],
                               lpm5wakeup=resetcause['lpm5wakeup'],
                               clockfail=resetcause['clockfail'])

        # Call base class constructor. By committing to the db we get an id.
        if userobj is not None:
            user_id = userobj.id
        else:
            user_id = None

        capture = super().create(box_id=boxobj.id,
                                 user_id=user_id,
                                 timestamp=decodedurl.scantimestamp,
                                 loopcount=decodedurl.status.loopcount,
                                 status=status,
                                 batvoltagemv=decodedurl.status.get_batvoltagemv(),
                                 cursorpos=decodedurl.endmarkerpos,
                                 version=0,
                                 timeintmins=decodedurl.timeintmins_int,
                                 md5=decodedurl.hash,
                                 samples=samples)

        # Assign serial to the box and commit to the db.
        return capture

    def create(self,
               boxobj,
               timestamp,
               loopcount,
               status,
               batvoltagemv,
               cursorpos,
               version,
               timeintmins,
               md5,
               samples,
               userobj=None):

        if userobj is not None:
            user_id = userobj.id
        else:
            user_id = None

        # Call base class constructor. By committing to the db we get an id.
        capture = super().create(box_id=boxobj.id,
                                 user_id=user_id,
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
