# -*- coding: utf-8 -*-
"""
    web.captures
    ~~~~~~~~~~

    captures package
"""

from ..core import Service
from .models import Capture, CaptureSample, CaptureStatus
from wscodec.decoder import Decoder
from flask import current_app


class CaptureService(Service):
    __model__ = Capture

    def decode_and_create(self, boxobj, statb64, timeintb64, circb64, ver, userobj=None):
        """Returns a new, saved instance of the capture model class.
        :param **kwargs: instance parameters
        """
        decodedurl = Decoder(boxobj.secretkey, statb64, timeintb64, circb64, ver)
        stat = decodedurl.params.status.status

        samples = [CaptureSample(smpl['ts'], smpl['temp'], smpl['rh']) for smpl in decodedurl.params.buffer.smpls]

        status = CaptureStatus(resetsalltime=stat['resetsalltime'],
                               brownout=stat['brownout'],
                               supervisor=stat['supervisor'],
                               watchdog=stat['watchdog'],
                               misc=stat['misc'],
                               lpm5wakeup=stat['lpm5wakeup'],
                               clockfail=stat['clockfail'])

        # Call base class constructor. By committing to the db we get an id.
        if userobj is not None:
            user_id = userobj.id
        else:
            user_id = None

        capture = super().create(box_id=boxobj.id,
                                 user_id=user_id,
                                 timestamp=decodedurl.scandatetime,
                                 loopcount=decodedurl.params.status.loopcount,
                                 status=status,
                                 batvoltagemv=decodedurl.params.status.batvoltagemv,
                                 cursorpos=decodedurl.params.buffer.endmarkerpos,
                                 version=decodedurl.majorversion,
                                 timeintmins=decodedurl.params.timeintervalmins,
                                 md5=decodedurl.params.buffer.md5,
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
