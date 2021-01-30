# -*- coding: utf-8 -*-
"""
    flaskapp.webhook.models
    ~~~~~~~~~~~~~~~~~

    Webhook model
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
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from secrets import token_urlsafe


class Webhook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # ID of the owning tag object. By setting unique to True, an IntegrityError will be raised
    # when 2 webhooks with the same parent_tag are inserted.
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), unique=True)
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

