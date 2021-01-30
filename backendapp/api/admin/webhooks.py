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

# Inspired by overholt
"""
    flaskapp.api.admin.webhooks
    ~~~~~~~~~~~~~~

    Webhook endpoints
"""

from flask import Blueprint, request, jsonify, current_app
from flask_restful import Api, abort, reqparse
from sqlalchemy.exc import IntegrityError
from ...services import webhooks
from ...webhooks.schemas import WebhookSchema
from .adminresource import SingleAdminResource, MultipleAdminResource


bp = Blueprint('adminwebhooks', __name__)
api = Api(bp)


class Webhook(SingleAdminResource):
    """Get or delete one webhook by ID """
    def __init__(self):
        super().__init__(WebhookSchema, webhooks)


class Webhooks(MultipleAdminResource):
    def __init__(self):
        super().__init__(WebhookSchema, webhooks)

    def get(self):
        """
        Get a list of all webhooks.
        Returns:

        """
        return super().get_filtered()

    def post(self):
        """
        Post a webhook
        :return:
            The newly created webhook or an error code.
        """
        try:
            return super().post()
        except IntegrityError as err:
            return str(err), 409


api.add_resource(Webhook, '/webhook/<id>')
api.add_resource(Webhooks, '/webhooks')
