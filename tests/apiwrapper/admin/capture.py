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

import requests
from ..admin import AdminApiWrapper
import json


class CaptureWrapper(AdminApiWrapper):
    """Wraps calls to capture endpoints on the Admin API. """

    def __init__(self, baseurl: str, adminapi_token: str):
        """Constructor for CaptureWrapper

        Args:
            baseurl (str): Websensor backend URL.
            adminapi_token (str): Token for accessing the admin API.
            endpoint_one (str): Endpoint for returning one resource instance.
            endpoint_many (str): Endpoint for returning a list of resource instances.
        """
        endpoint_one = "/capture/"
        endpoint_many = "/captures"
        super().__init__(baseurl, adminapi_token, endpoint_one, endpoint_many)

    def get_many(self, offset: int = 0, limit: int = None, tag_id: int = None) -> list:
        """Makes a GET request to endpoint_many.

        Args:
            offset (int):  Return captures with an ID greater than this number.
            limit (int): Number of captures to return.
            tag_id (int): Filter by tag_id (optional)

        Returns:
            list: A list of capture dictionaries
        """
        kwargs = {'offset': offset, 'limit': limit}

        if tag_id is not None:
            kwargs.update({'tag_id': tag_id})

        return super().get_many(**kwargs)

    def post(self, capturepayload: dict):
        """Create a capture in the database directly.

        The is made from a dictionary including a list of samples, a tag_id and a user_id. The
        endpoint is used for testing. It removes the need to encode test vectors with wscodec (introduces
        a second point of failure in an external library).

        Captures can be created with a known list of samples. Then samples are collected from the tag
        using the consumer API. These are compared with a vector of expected samples. If captures overlap slightly in
        time it is expected that duplicate samples are removed.

        Args:
            capturepayload (dict): Dictionary following the :ref:`capture schema <CapturesConsumerAPI>`.

        Returns: HTTP response from wsbackend.

        """
        captpayload = json.dumps(capturepayload)
        capturesurl = "{apiurl}/captures".format(apiurl=self.apiurl)
        r = requests.post(capturesurl, data=captpayload, headers=self.headers)
        r.raise_for_status()
        captresponse = r.json()
        return captresponse