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
from . import ConsumerApiWrapper


class TagWrapper(ConsumerApiWrapper):
    """Wraps calls to tag endpoints on the Consumer API"""

    def get(self, tagserial: str) -> dict:
        """

        Args:
            tagserial (str): Base64 serial that uniquely identifies a tag (hardware module).

        Returns: Tag dictionary as described :ref:`here <TagConsumerAPI>`.

        """
        tagurl = "{apiurl}/tag/{tagserial}".format(apiurl=self.apiurl,
                                                   tagserial=tagserial)
        r = requests.get(tagurl)
        r.raise_for_status()

        ConsumerApiWrapper.process_status(r.status_code)

        response = r.json()
        return response
