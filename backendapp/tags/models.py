# -*- coding: utf-8 -*-
"""
    web.tags.models
    ~~~~~~~~~~~~~~~~~

    Tag model
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
from ..captures.models import Capture, CaptureSample
from ..webhooks.models import Webhook
from flask import current_app
from secrets import token_urlsafe
import datetime

SERIAL_LEN_BYTES = 8
SECKEY_LEN_BYTES = 16


# Define the Tag data model.
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Tag identity is unique. It will correspond to the BLE MAC address.
    # See MAC_BLE_0 and MAC_BLE_1 to read this 48-bit (6 byte) address.
    serial = db.Column(db.String(SERIAL_LEN_BYTES), unique=True)
    secretkey = db.Column(db.String(SECKEY_LEN_BYTES))
    usehmac = db.Column(db.Boolean, default=True)
    fwversion = db.Column(db.String(16))
    hwversion = db.Column(db.String(16))
    description = db.Column(db.String(280))
    timeregistered = db.Column(db.DateTime, nullable=False)

    # ID of the owning user object
    captures = db.relationship('Capture',
                               lazy="dynamic",
                               order_by="desc(Capture.timestamp)",
                               backref=db.backref('parent_tag'),
                               cascade="all, delete-orphan")

    # Specify a one-to-one relationship with a webhook
    webhook = db.relationship('Webhook',
                              lazy="joined",
                              uselist=False,
                              backref=db.backref('parent_tag'),
                              cascade="all, delete-orphan")

    def uniquesampleswindow(self, starttime, endtime):
        threshold_in_seconds = 120
        # Select all capture samples belonging to this tag, between the start time and the end time.
        # Crucially all samples must be ordered by timestamp for the grouping to work.
        stmt = CaptureSample.query.join(Capture).filter((Capture.parent_tag == self) &
                                                        (CaptureSample.timestamp >= starttime) &
                                                        (CaptureSample.timestamp <= endtime)).order_by(
            CaptureSample.timestamp.asc()).subquery()
        # Calculate the time difference between successive samples using the lag function.
        # Append this as a new column named tdiffseconds.
        stmt2 = db.session.query(stmt,
                                 (stmt.c.timestampPosix - db.func.lag(stmt.c.timestampPosix, 1, 9999).over()
                                  ).label('tdiffseconds')).subquery()
        # Mark rows where the time difference between successive samples exceeds the threshold
        # 1 indicates the start a new group.
        # 0 indicates (duplicate) samples inside a group.
        # It is assumed that all samples with a time difference less than the threshold
        # must be duplicates.
        stmt2a = db.session.query(stmt2, db.case([(stmt2.c.tdiffseconds > threshold_in_seconds, 1), ], else_=0).label(
            'groupstart')).subquery()
        # Make the group markers contiguous i.e. all members of a group should share the same number.
        # To do this iterate through all rows and
        # calculate the sum of groupstart over rows
        # between unbounded preceeding and the current row.
        # See the documentation for rows over unbounded preceeding here:
        # https://docs.sqlalchemy.org/en/latest/core/sqlelement.html#sqlalchemy.sql.expression.over
        stmt2b = db.session.query(stmt2a,
                                  db.func.sum(stmt2a.c.groupstart).over(rows=(None, 0)).label('groupid')).subquery()
        # Calculate the minimum capture_id in each group. Append this as a new column.
        stmt3 = db.session.query(stmt2b, db.func.min(stmt2b.c.capture_id).over(partition_by=stmt2b.c.groupid).label(
            'mincaptid')).subquery()
        # Select capture samples from the list above. Only return samples that have the minimum capture_id.
        stmt4 = db.session.query(CaptureSample).join(stmt3,
                                                     ((stmt3.c.id == CaptureSample.id) &
                                                      (stmt3.c.capture_id == stmt3.c.mincaptid))).order_by(
            CaptureSample.timestamp.desc()
        )

        return stmt4

    def __repr__(self):
        return '<Tag id=%s with serial=%s and secret key=%s>' % (self.id, self.serial, self.secretkey)

    def __init__(self, serial: str = None, secretkey: str = None, usehmac: bool = True, fwversion: str = "", hwversion: str = "", description: str = "", **kwargs):
        # Initialise the tag object
        super(Tag, self).__init__(**kwargs)
        if isinstance(serial, str) and (len(serial) == SERIAL_LEN_BYTES):
            self.serial = serial
        else:
            self.serial = None

        if isinstance(secretkey, str) and (len(secretkey) == SECKEY_LEN_BYTES):
            self.secretkey = secretkey
        else:
            self.secretkey = self.__class__.gen_secret_key()

        self.usehmac = usehmac
        self.fwversion = fwversion
        self.hwversion = hwversion
        self.description = description
        self.timeregistered = datetime.datetime.utcnow()

    @staticmethod
    def gen_secret_key():
        """Generate a random secret key.
        """
        skeylenbytes = 12
        return token_urlsafe(skeylenbytes)
