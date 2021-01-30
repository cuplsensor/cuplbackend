# -*- coding: utf-8 -*-
"""
    web.captures.models
    ~~~~~~~~~~~~~~~~~

    Capture model
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

from ..core import db
from datetime import timezone, datetime
from dateutil import parser
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.schema import UniqueConstraint
from flask import current_app


class Capture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # ID of the owning tag object.
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))

    timestamp = db.Column(db.DateTime, nullable=False)
    batvoltagemv = db.Column(db.Integer)
    loopcount = db.Column(db.Integer)
    cursorpos = db.Column(db.Integer)
    status = db.Column(db.Integer)
    format = db.Column(db.String(30))
    timeintmins = db.Column(db.Integer)
    hash = db.Column(db.String(20))
    status = db.relationship('CaptureStatus',
                             uselist=False,
                             backref=db.backref('parent_capture'),
                             cascade="all, delete-orphan")
    samples = db.relationship('CaptureSample',
                              order_by="desc(CaptureSample.timestamp)",
                              lazy='dynamic',
                              backref=db.backref('parent_capture'),
                              cascade="all, delete-orphan")
    __table_args__ = (UniqueConstraint('tag_id', 'hash', name='_tagid_md5_uc'),)

    @hybrid_property
    def tagserial(self):
        return self.parent_tag.serial

    def __init__(self,
                 tag_id,
                 timestamp,
                 loopcount,
                 format,
                 batvoltagemv,
                 cursorpos,
                 timeintmins,
                 hash,
                 status,
                 samples=[],
                 id=None):

        self.tag_id = tag_id
        self.id = id
        self.timestamp = timestamp
        self.loopcount = loopcount
        self.format = format
        self.batvoltagemv = batvoltagemv
        self.cursorpos = cursorpos
        self.timeintmins = timeintmins
        self.hash = hash
        self.status = status
        self.samples = samples


class CaptureStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # ID of the owning capture object
    capture_id = db.Column(db.Integer, db.ForeignKey('capture.id'))

    resetsalltime = db.Column(db.Integer)
    brownout = db.Column(db.Boolean)
    clockfail = db.Column(db.Boolean)
    lpm5wakeup = db.Column(db.Boolean)
    misc = db.Column(db.Boolean)
    supervisor = db.Column(db.Boolean)
    watchdog = db.Column(db.Boolean)

    def __init__(self,
                 resetsalltime,
                 brownout,
                 clockfail,
                 lpm5wakeup,
                 misc,
                 supervisor,
                 watchdog):
        self.resetsalltime = resetsalltime
        self.brownout = brownout
        self.clockfail = clockfail
        self.lpm5wakeup = lpm5wakeup
        self.misc = misc
        self.supervisor = supervisor
        self.watchdog = watchdog


class CaptureSample(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # ID of the owning capture object
    capture_id = db.Column(db.Integer, db.ForeignKey('capture.id'))

    timestamp = db.Column(db.DateTime, nullable=False)
    timestampPosix = db.Column(db.Integer, nullable=False)
    temp = db.Column(db.Float)
    rh = db.Column(db.Float, nullable=True)

    def __init__(self, timestamp: datetime, temp, rh=None, location=None):
        if type(timestamp) is str:
            timestamp = parser.isoparse(timestamp)
        self.timestamp = timestamp
        self.timestampPosix = timestamp.replace(tzinfo=timezone.utc).timestamp()
        self.temp = temp
        self.rh = rh
