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
    """
    Webhooks are a means of integrating cuplbackend with a 3rd-party web application.

    These are user-defined HTTP callbacks.

    When a Tag is read via NFC and a new Capture is created, cuplbackend makes an HTTP POST request to a
    user-specified URL. The body includes Capture data (e.g. a list of timestamped samples) encoded as JSON.

    The use of webhooks obviates the need for a 3rd-party application to poll for new Capture data.

    An end-user or administrator can add one webhook to each tag.

    Webhooks have a simple authentication mechanism; a secret key shared between the cuplbackend and the
    3rd-party application. Without this, it would be possible to post fake captures to the 3rd-party application with
    knowledge of the webhook URL only.
    """
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
        """Return a serial string for the Tag that this webhook belongs to. """
        return self.parent_tag.serial

    def __init__(self,
                 tag_id: int,
                 address: str,
                 fields: str = None,
                 wh_secretkey: str = None):
        """
        Assign a webhook to a tag. A random secret key is generated if none is supplied.

        :param tag_id: ID of the Tag.
        :param address: An HTTP POST request is made to this URL when the Tag is read via NFC.
        :param fields: A list of fields in the Capture model. These will be included with the POST request payload.
        :param wh_secretkey: A string of up to 256 characters, to authenticate this application with the POST recipient.
        """
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
        """Generate a random secret key with URL-safe characters. """
        skeylenbytes = 12
        return token_urlsafe(skeylenbytes)

