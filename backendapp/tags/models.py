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
from ..captures.models import Capture, CaptureSample
from ..webhooks.models import Webhook
from flask import current_app
from secrets import token_urlsafe
import datetime

SERIAL_LEN_BYTES = 8    # Length of the serial string.
SECKEY_LEN_BYTES = 16   # Length of the secret key string.


class Tag(db.Model):
    """
    Each Tag instance represents one cuplTag device.

    Columns fall into the categories below.

    These scalars must be copied to a cuplTag (by serial or NFC):

        Tags are identified with an 8-character alphanumeric serial string.

        A secret key is used for authentication. This string is stored only in this table and on the tag itself.
        Authentication is enabled with usehmac. When disabled, the secret key is ignored.

    These scalars can be populated by read from the programmed cuplTag:

        Tag firmware and hardware versions. These are not otherwise used by this software.

    The remainder are for information only:

        The time registered column stores the date and time an instance was created.

        Description can be populated by the end-user, with strings such as "in the downstairs bathroom".

    Each Tag contains a list of captures and webhooks.
    """
    id = db.Column(db.Integer, primary_key=True)

    serial = db.Column(db.String(SERIAL_LEN_BYTES), unique=True)
    secretkey = db.Column(db.String(SECKEY_LEN_BYTES))
    usehmac = db.Column(db.Boolean, default=True)
    fwversion = db.Column(db.String(16))
    hwversion = db.Column(db.String(16))
    description = db.Column(db.String(280))
    timeregistered = db.Column(db.DateTime, nullable=False)

    # Create a one-to-many relationship with captures
    captures = db.relationship('Capture',
                               lazy="dynamic",
                               order_by="desc(Capture.timestamp)",
                               backref=db.backref('parent_tag'),
                               cascade="all, delete-orphan")

    # Create a one-to-one relationship with a webhook
    webhook = db.relationship('Webhook',
                              lazy="joined",
                              uselist=False,
                              backref=db.backref('parent_tag'),
                              cascade="all, delete-orphan")

    def uniquesampleswindow(self, starttime: datetime.datetime, endtime: datetime.datetime):
        """Return the set of samples collected from this tag within a time window. Duplicate samples are removed.

        Consecutive captures, taken a short time apart, will contain a large number of duplicate samples.
        These have identical sensor readings, but slightly different timestamps. All
        samples are timestamped relative to that of the capture, which has a margin of error of +/- 1 minute.

        This software does not use a time series database, so an algorithm had to be written.

        :param starttime: Start of the time window.
        :param endtime: End of the time window.
        :return: A query on the CaptureSample table, bounded by the starttime and endtime.
        """
        # Maximum time difference between the oldest and newest duplicate samples. Equivalent to +/- 1 minute.
        threshold_in_seconds = 120

        # Select all samples belonging to this tag, between the start time and the end time.
        # Samples are returned in chronological order.
        stmt = CaptureSample.query.join(Capture).filter((Capture.parent_tag == self) &
                                                        (CaptureSample.timestamp >= starttime) &
                                                        (CaptureSample.timestamp <= endtime)).order_by(
            CaptureSample.timestamp.asc()).subquery()

        # Calculate the time difference in seconds between successive samples
        # using the lag function (https://www.postgresql.org/docs/current/functions-window.html)
        # Append this as a new column named tdiffseconds.
        # It is easiest to calculate time differences using timestampPosix.
        # It is an integer (the number of seconds since the Unix epoch).
        defdiff = 9999      # Default to a very large time difference when there is no previous row.
        rowoffset = 1       # Subtract timestamp of the previous row from the current one.
        stmt2 = db.session.query(stmt,
                                 (stmt.c.timestampPosix - db.func.lag(stmt.c.timestampPosix, rowoffset, defdiff).over()
                                  ).label('tdiffseconds')).subquery()

        # Mark rows where the time difference between samples exceeds threshold_in_seconds.
        # All samples with a time difference less than the threshold are duplicates.
        # Append as a new column named groupstart.
        #   1 indicates the start a new group.
        #   0 indicates samples inside a group. These are the duplicates.
        # For example, when looking at samples from
        #   4 overlapping captures, expect: 1, 0, 0, 0, 1, 0, 0, 0 ... (one new sample for every four).
        #   2 overlapping captures, expect: 1, 0, 1, 0, 1, 0 ... (one new sample for every two).
        stmt2a = db.session.query(stmt2, db.case([(stmt2.c.tdiffseconds > threshold_in_seconds, 1), ], else_=0).label(
            'groupstart')).subquery()

        # Make the group markers contiguous, so that one number identifies all members.
        # Append as a new column named groupid.
        # For example the samples from
        #   4 overlapping captures are marked: 1, 1, 1, 1, 2, 2, 2, 2 ...
        #   2 overlapping captures are marked: 1, 1, 2, 2, 3, 3 ...
        # To do this, for each row
        #   Calculate the cumulative sum of groupstart between 'rows unbounded preceding' and the current row.
        # https://docs.sqlalchemy.org/en/latest/core/sqlelement.html#sqlalchemy.sql.expression.over
        stmt2b = db.session.query(stmt2a,
                                  db.func.sum(stmt2a.c.groupstart).over(rows=(None, 0)).label('groupid')).subquery()

        # When a new captures is taken, there must be no change to the timestamps of any samples returned previously
        # for the same time window. The output of this function must be consistent.
        # Find the minimum (oldest) capture_id for samples within each group of duplicates.
        # Append as a new column named mincaptid.
        stmt3 = db.session.query(stmt2b, db.func.min(stmt2b.c.capture_id).over(partition_by=stmt2b.c.groupid).label(
            'mincaptid')).subquery()

        # Select capture samples from the list above.
        # From each group of duplicates, only return samples that match the minimum capture_id.
        stmt4 = db.session.query(CaptureSample).join(stmt3,
                                                     ((stmt3.c.id == CaptureSample.id) &
                                                      (stmt3.c.capture_id == stmt3.c.mincaptid))).order_by(
            CaptureSample.timestamp.desc()
        )

        return stmt4

    def __repr__(self) -> str:
        """Return the string representation of a tag for debug purposes. """
        return '<Tag id=%s with serial=%s and secret key=%s>' % (self.id, self.serial, self.secretkey)

    def __init__(self, serial: str = None, secretkey: str = None, usehmac: bool = True, fwversion: str = "", hwversion: str = "", description: str = "", **kwargs):
        """Create a new instance of the Tag model.

        All parameters are optional. The serial and secret key strings are automatically generated when not supplied.

        :param serial: An URL-safe string of length SERIAL_LEN_BYTES, which uniquely identifies a tag.
        :param secretkey: An URL-safe string of length SECKEY_LEN_BYTES, used for tag authentication.
        :param usehmac: When true (default), the checksum received from a tag is assumed to be a
                        Hash-Based Message Authentication Code. Captures are verified with knowledge
                        of the secret key. When false, the checksum is a (weak) MD5 message integrity check only.

        :param fwversion: Tag firmware version string (e.g. F1.5_C2_HT07)
        :param hwversion: Tag hardware version string (e.g. HT07)
        :param description: A user-editable description of the tag, which normally pertains to location.
        :param kwargs:
        """
        super(Tag, self).__init__(**kwargs)

        # Verify that the serial parameter is of type string and has the correct length.
        # BUG: URL-safeness is not checked.
        if isinstance(serial, str) and (len(serial) == SERIAL_LEN_BYTES):
            self.serial = serial
        else:
            self.serial = None

        # Verify that the secret key is of type string and has the correct length.
        # BUG: URL-safeness is not checked.
        if isinstance(secretkey, str) and (len(secretkey) == SECKEY_LEN_BYTES):
            self.secretkey = secretkey
        else:
            self.secretkey = self.__class__.gen_secret_key()

        self.usehmac = usehmac
        self.fwversion = fwversion
        self.hwversion = hwversion
        self.description = description

        # Set the time registered to the current UTC date and time. This datetime object is naive, because it
        # has no timezone information. This can be risky. Some software will interpret this as a
        # local datetime object. https://docs.python.org/3/library/datetime.html#datetime.datetime.utcnow
        self.timeregistered = datetime.datetime.utcnow()

    @staticmethod
    def gen_secret_key() -> str:
        """Generate a random secret key, containing 16 URL-safe base64 characters. """
        skeylenbytes = 12
        return token_urlsafe(skeylenbytes)
