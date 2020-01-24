# -*- coding: utf-8 -*-
"""
    web.boxes.models
    ~~~~~~~~~~~~~~~~~

    Box model
"""

from ..core import db
from ..captures.models import Capture, CaptureSample
from ..boxviews.models import BoxView
from ..locations.models import Location
from flask import current_app
import datetime


# Define the Box data model.
class Box(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Box identity is unique. It will correspond to the BLE MAC address.
    # See MAC_BLE_0 and MAC_BLE_1 to read this 48-bit (6 byte) address.
    serial = db.Column(db.String(8), unique=True)
    secretkey = db.Column(db.String(8))
    timeregistered = db.Column(db.DateTime, nullable=False)

    # ID of the owning user object
    captures = db.relationship('Capture',
                               order_by="desc(Capture.timestamp)",
                               backref=db.backref('parent_box'),
                               cascade="all, delete-orphan")

    boxviews = db.relationship('BoxView',
                               order_by="desc(BoxView.timestamp)",
                               backref=db.backref('parent_box'),
                               cascade="all, delete-orphan")

    def locations_in_window(self,
                            starttime=datetime.datetime(year=1970, month=1, day=1),
                            endtime=datetime.datetime.utcnow()):

        stmt = Location.query.join(CaptureSample).join(Capture).filter((Capture.parent_box == self) &
                                                                       (CaptureSample.timestamp >= starttime) &
                                                                       (CaptureSample.timestamp <= endtime)).order_by(
                                                                        CaptureSample.timestamp.desc())

        return stmt.all()

    def uniquesampleswindow(self, starttime, endtime, offset=0, limit=None):
        threshold_in_seconds = 120
        # Select all capture samples belonging to this box, between the start time and the end time.
        # Crucially all samples must be ordered by timestamp for the grouping to work.
        stmt = CaptureSample.query.join(Capture).filter((Capture.parent_box == self) &
                                                        (CaptureSample.timestamp >= starttime) &
                                                        (CaptureSample.timestamp <= endtime)).order_by(CaptureSample.timestamp.asc()).subquery()
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
        stmt2a = db.session.query(stmt2, db.case([(stmt2.c.tdiffseconds > threshold_in_seconds, 1), ], else_=0).label('groupstart')).subquery()
        # Make the group markers contiguous i.e. all members of a group should share the same number.
        # To do this iterate through all rows and
        # calculate the sum of groupstart over rows
        # between unbounded preceeding and the current row.
        # See the documentation for rows over unbounded preceeding here:
        # https://docs.sqlalchemy.org/en/latest/core/sqlelement.html#sqlalchemy.sql.expression.over
        stmt2b = db.session.query(stmt2a, db.func.sum(stmt2a.c.groupstart).over(rows=(None, 0)).label('groupid')).subquery()
        # Calculate the minimum capture_id in each group. Append this as a new column.
        stmt3 = db.session.query(stmt2b, db.func.min(stmt2b.c.capture_id).over(partition_by=stmt2b.c.groupid).label('mincaptid')).subquery()
        # Select capture samples from the list above. Only return samples that have the minimum capture_id.
        stmt4 = db.session.query(CaptureSample).join(stmt3,
                                                     ((stmt3.c.id == CaptureSample.id) &
                                                      (stmt3.c.capture_id == stmt3.c.mincaptid))).order_by(
            CaptureSample.timestamp.desc()
        ).offset(offset).limit(limit).options(db.joinedload(CaptureSample.location))
        capturesamplelist = stmt4.all()
        current_app.logger.info(stmt4)
        current_app.logger.info("statement 2a")
        current_app.logger.info(db.session.query(stmt2a).all())
        current_app.logger.info("statement 3")
        current_app.logger.info(db.session.query(stmt3).all())
        current_app.logger.info("---")
        current_app.logger.info(stmt4.all())
        return capturesamplelist

    def get_all_locations(self):
        # Select all capturesamples to this one
        stmta = db.session.query(CaptureSample).join(Capture).filter(Capture.parent_box == self).subquery()
        # Only select capturesamples with a location element and pick the last one.
        stmtb = db.session.query(Location, stmta.c.timestamp).filter(Location.capturesample_id==stmta.c.id).order_by(stmta.c.timestamp.desc())
        return stmtb.all()

    def __repr__(self):
        return '<Box id=%s with serial=%s and secret key=%s>' % (self.id, self.serial, self.secretkey)

    def __init__(self, serial=None, secretkey=None):
    	# Initialise the box object
        self.serial = serial
        self.secretkey = secretkey
        self.timeregistered = datetime.datetime.utcnow()
        self.user_id = None
