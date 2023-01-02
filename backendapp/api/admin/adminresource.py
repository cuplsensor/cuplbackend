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

from ..baseresource import SingleResource, MultipleResource
from .admintokenauth import requires_admin_token
from flask import request, jsonify
from marshmallow import ValidationError


class SingleAdminResource(SingleResource):
    """
    A :py:class:`~backendapp.api.baseresource.SingleResource` for administrators.

    All methods are decorated with :py:meth:`~backendapp.api.admin.admintokenauth.requires_admin_token`.
    """
    method_decorators = [requires_admin_token]


class MultipleAdminResource(MultipleResource):
    """
    A :py:class:`~backendapp.api.baseresource.MultipleResource` for administrators.

    All methods are decorated with :py:meth:`~backendapp.api.admin.admintokenauth.requires_admin_token`.
    """
    method_decorators = [requires_admin_token]



