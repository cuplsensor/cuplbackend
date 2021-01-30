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

from functools import wraps
from flask import abort
from ..baseresource import SingleResource, MultipleResource
from .tagtokenauth import requires_tagtoken
from ...services import tags


def lookup_webhook_id(f):
    """Get id of the webhook attached to this tag.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        tagobj = tags.get_by_serial(kwargs['serial'])
        del kwargs['serial']
        try:
            webhook_id = tagobj.webhook.id
        except AttributeError:
            abort(404)
        return f(*args, id=webhook_id, **kwargs)

    return decorated


class TagTokenSingleResource(SingleResource):
    method_decorators = [requires_tagtoken]


class TagTokenMultipleResource(MultipleResource):
    method_decorators = [requires_tagtoken]