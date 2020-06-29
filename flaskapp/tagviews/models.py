# -*- coding: utf-8 -*-
"""
    web.logitem.models
    ~~~~~~~~~~~~~~~~~

    Logitem model
"""

from ..core import db
import datetime
from sqlalchemy.ext.hybrid import hybrid_property


# Define the TagView data model.
class TagView(db.Model):
    # Unique ID of the logitem
    id = db.Column(db.Integer, primary_key=True)
    # Optional ID of the owning user object
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # ID and relationship to the child tag
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), nullable=False)
    # Timestamp of the log event
    timestamp = db.Column(db.DateTime, nullable=False)

    @hybrid_property
    def tagserial(self):
        return self.parent_tag.serial

    def __init__(self, parent_tag, parent_user):
        self.parent_tag = parent_tag
        self.parent_user = parent_user
        self.timestamp = datetime.datetime.utcnow()
