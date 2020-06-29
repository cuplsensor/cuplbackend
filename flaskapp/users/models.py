# -*- coding: utf-8 -*-
"""
    web.users.models
    ~~~~~~~~~~~~~~~~~

    User model
"""

from ..models import Capture, TagView, Tag
from ..core import db


# Define the User data model. Make sure to add the flask_user.UserMixin !!
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # OAuth ID field
    oauth_id = db.Column(db.String(255), nullable=False, unique=True)

    timeregistered = db.Column(db.DateTime, nullable=False)

    captures = db.relationship('Capture',
                               collection_class=list,
                               backref=db.backref('scanned_by_user'),
                               lazy='dynamic')

    tagviews = db.relationship('TagView',
                               collection_class=list,
                               backref=db.backref('parent_user'),
                               cascade="all, delete-orphan",
                               lazy='dynamic')

    def has_scanned_tag(self, tagserial):
        # Returns true if this user has a capture on a tag.
        stmt = Capture.query.join(Tag).filter((Capture.scanned_by_user == self) & (Tag.serial == tagserial))

        nresults = stmt.count()
        return nresults > 0

    def latest_tagview_by_tag(self):
        stmt = TagView.query.filter((TagView.parent_user == self)).subquery()
        # Rank the tagviews of each tag by timestamp.
        stmt2 = db.session.query(stmt, db.func.rank().over(
            order_by=stmt.c.timestamp.desc(),
            partition_by=stmt.c.tag_id
        ).label('rnk')).subquery()
        # Only select rank 1 i.e. the tagview with the most recent timestamp for each tag. We want the tag with the
        # latest timestamp first.
        stmt3 = TagView.query.join(stmt2, ((stmt2.c.id == TagView.id) & (stmt2.c.rnk == 1))).order_by(TagView.timestamp.desc())

        return stmt3.all()

    def latest_capture_by_tag(self):
        # Select all capture samples belonging to this tag, between the start time and the end time.
        # Crucially all samples must be ordered by timestamp for the grouping to work.
        # https://stackoverflow.com/questions/40635099/convert-rank-and-partition-query-to-sqlalchemy
        stmt = Capture.query.filter((Capture.scanned_by_user == self)).subquery()
        stmt2 = db.session.query(stmt, db.func.rank().over(
            order_by=stmt.c.timestamp.desc(),
            partition_by=stmt.c.tag_id
        ).label('rnk')).subquery()

        stmt3 = Capture.query.join(stmt2, ((stmt2.c.id == Capture.id) & (stmt2.c.rnk == 1))).order_by(Capture.timestamp.desc())

        return stmt3.all()

    def __init__(self, oauth_id, timeregistered):
        # Initialise the user object
        self.oauth_id = oauth_id
        self.timeregistered = timeregistered



