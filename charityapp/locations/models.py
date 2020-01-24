# -*- coding: utf-8 -*-
"""
    web.captures.models
    ~~~~~~~~~~~~~~~~~

    Capture model
"""

from ..core import db

# Define the Location data model.
class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # ID of the owning box object.
    capturesample_id = db.Column(db.Integer, db.ForeignKey('capture_sample.id'), nullable=False)

    timestamp = db.Column(db.DateTime, nullable=False) # Entry timestamp
    description = db.Column(db.String(50), nullable=False)

    def __init__(self, capturesample, timestamp, description):
        self.parent_capturesample = capturesample
        self.timestamp = timestamp
        self.description = description
