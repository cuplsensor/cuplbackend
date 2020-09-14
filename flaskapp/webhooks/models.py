# -*- coding: utf-8 -*-
"""
    flaskapp.webhook.models
    ~~~~~~~~~~~~~~~~~

    Webhook model
"""

from ..core import db
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from secrets import token_urlsafe


class Webhook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # ID of the owning tag object.
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
    address = db.Column(db.String(2048), nullable=False)
    fields = db.Column(db.String(100))
    wh_secretkey = db.Column(db.String(256))
    created_on = db.Column(db.DateTime, nullable=False)

    @hybrid_property
    def tagserial(self):
        return self.parent_tag.serial

    def __init__(self,
                 tag_id: int,
                 address: str,
                 fields: str = None,
                 wh_secretkey: str = None):

        if isinstance(wh_secretkey, str):
            self.wh_secretkey = wh_secretkey
        else:
            self.wh_secretkey = self.__class__.gen_secret_key()

        self.tag_id = tag_id
        self.address = address
        self.fields = fields
        self.created_on = datetime.utcnow()

    @staticmethod
    def gen_secret_key():
        """Generate a random secret key.
        """
        skeylenbytes = 12
        return token_urlsafe(skeylenbytes)

