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

from . import ConsumerApiWrapper
import requests


class SampleWrapper(ConsumerApiWrapper):
    """Wraps samples endpoint of the Consumer API."""

    def get_samples(self,
                    serial: str,
                    starttime: str,
                    endtime: str,
                    page: int = 1,
                    per_page: int = 10000) -> list:
        """Get a list of temperature/humidity samples collected by a tag.

        A time window can be specified so that only samples that fall between starttime and endtime are returned.

        Makes a GET request to the :ref:`Samples <SamplesConsumerAPI>` endpoint.

        Args:
            serial (str): Base64 string. Identifies a tag to return samples from.
            starttime (str): Start datetime as an ISO-8601 string.
            endtime (str): End datetime as an ISO-8601 string.
            offset (int): Start list at the nth sample for pagination.
            limit (int): Limit the list length for pagination.

        Returns:
            list: A list of samples. Each is a dictionary.

        """
        samplesurl = "{apiurl}/tag/{serial}/samples".format(apiurl=self.apiurl,
                                                            serial=serial)

        payload = {
            'starttimestr': starttime,
            'endtimestr': endtime,
            'page': page,
            'per_page': per_page
        }

        # Using urlencode is important to remove the '+' and convert it to %2B. Date decode does
        # not work without it.
        r = requests.get(samplesurl, params=payload)
        r.raise_for_status()
        ConsumerApiWrapper.process_status(r.status_code)
        sample_response = r.json()
        return sample_response
