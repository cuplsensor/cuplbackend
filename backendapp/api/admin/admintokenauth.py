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
from ..tokenauth import TokenAuthSymmetric
from ...config import ADMINAPI_CLIENTID, ADMINAPI_CLIENTSERET, ADMINAPI_AUDIENCE


admintokenauth = TokenAuthSymmetric(issuer=ADMINAPI_CLIENTID,
                                    audience=ADMINAPI_AUDIENCE,
                                    secret=ADMINAPI_CLIENTSERET)


def requires_admin_token(f):
    """
    A decorator, which reads and verifies an Admin API token before calling the function :param:`f`.

    :param f: The function to decorate. This is normally bound to an HTTP method (GET, POST, PUT) for a REST Resource.
    :return: The decorated function.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        admintokenauth.get_decoded_token()
        return f(*args, **kwargs)

    return decorated
