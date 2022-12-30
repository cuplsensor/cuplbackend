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

from ..core import db
from datetime import timezone, datetime
from dateutil import parser
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.schema import UniqueConstraint
from flask import current_app


class Capture(db.Model):
    """
    A cuplTag is read by an NFC reader (such as a phone). Encoded data
    are stored within URL parameters, as part of an NDEF URL record.

    Parameters are decoded by the API within this application.

    The resultant data (a list of timestamped temperature+humidity
    samples and status information) are stored inside the database as a Capture.

    No two captures for a given tag can have the same MD5 or HMAC checksum. A database
    constraint guarantees this. Identical captures would otherwise occur for 3 reasons:
        1) Insufficient time between reads.
        2) The device has run out of battery.
        3) An attacker intends to fill up the database.

    The constraint produces an error message, which is fed back to the frontend web
    application with the API.
    """
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

    # One-to-one reference to a CaptureStatus object.
    status = db.relationship('CaptureStatus',
                             uselist=False,
                             backref=db.backref('parent_capture'),
                             cascade="all, delete-orphan")

    # One-to-many reference to CaptureSample objects.
    samples = db.relationship('CaptureSample',
                              order_by="desc(CaptureSample.timestamp)",
                              lazy='dynamic',
                              backref=db.backref('parent_capture'),
                              cascade="all, delete-orphan")

    # No two captures the same is enforced by a unique constraint.
    __table_args__ = (UniqueConstraint('tag_id', 'hash', name='_tagid_md5_uc'),)

    @hybrid_property
    def tagserial(self):
        """Return a serial string for the Tag that data has been read."""
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
        """
        Create a new instance of the Capture model.

        Stores the output from cuplCodec.

        :param tag_id: ID of the Tag read to make this capture.
        :param timestamp: Datetime object for when the capture was decoded. The timezone should be UTC.
        :param loopcount: Number of times the circular buffer cursor has wrapped around from the end to the start.
        :param format: Indicates how to decode parameters in the cupl URL.
        :param batvoltagemv: Voltage in milliVolts of the battery powering cuplTag.
        :param cursorpos: Position of the circular buffer cursor relative to the start of the string.
        :param timeintmins: Time interval between samples in minutes.
        :param hash: MD5 or HMAC of Capture data.
        :param status: Reference to a CaptureStatus object.
        :param samples: A list of CaptureSamples objects.
        :param id: ID of this capture.
        """

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
    """
    Status information for the cuplTag device.

    Includes the number of resets since the tag was programmed and
    the cause of the most recent reset.
    """
    # ID of this row in the CaptureStatus table.
    id = db.Column(db.Integer, primary_key=True)
    # ID of the parent Capture.
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
        """
        Create a new instance of the CaptureStatus model.

        This stores information from the MSP430 on cuplTag.

        :param resetsalltime: The number of times the MSP430 has reset for any reason.
        :param brownout: True if the most recent reset was caused by a brownout condition.
        :param clockfail: True if a clock failure has occurred.
        :param lpm5wakeup: True if the MSP430 has woken up from low power mode LPMx.5. This is normal, not an error.
        :param misc: True if the MSP430 reset cause is miscellaneous.
        :param supervisor: True if the MSP430 Supply Voltage Supervisor has triggered a reset. Implies a low battery.
        :param watchdog: True if the MSP430 watchdog has timed out. Indicative of a firmware bug or hardware failure.
        """
        self.resetsalltime = resetsalltime
        self.brownout = brownout
        self.clockfail = clockfail
        self.lpm5wakeup = lpm5wakeup
        self.misc = misc
        self.supervisor = supervisor
        self.watchdog = watchdog


class CaptureSample(db.Model):
    """
    A timestamped environmental sensor sample. Includes temperature (required) and humidity (optional).

    The timestamp is stored as a datetime object and converted to an integer (the POSIX timestamp). The latter is
    the number of seconds since the 1st January 1970. Some SQL window functions (lag and lead) only operate on integers.
    """
    id = db.Column(db.Integer, primary_key=True)
    # ID of the parent capture object
    capture_id = db.Column(db.Integer, db.ForeignKey('capture.id'))

    timestamp = db.Column(db.DateTime, nullable=False)
    timestampPosix = db.Column(db.Integer, nullable=False)
    temp = db.Column(db.Float)
    rh = db.Column(db.Float, nullable=True)

    def __init__(self, timestamp: datetime, temp, rh=None, location=None):
        """
        Create a new sample instance.

        :param timestamp: The time the sample was recorded, estimated to the nearest minute by this application.
        :param temp: Temperature in degrees C.
        :param rh: Relative humidity in percent.
        :param location: Unused.
        """
        if type(timestamp) is str:
            timestamp = parser.isoparse(timestamp)
        self.timestamp = timestamp
        self.timestampPosix = timestamp.replace(tzinfo=timezone.utc).timestamp()
        self.temp = temp
        self.rh = rh
