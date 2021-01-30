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


class CaptureWrapper(ConsumerApiWrapper):
    """Wraps capture endpoints of the Consumer API. """

    def get_list(self,
                 serial: str,
                 offset: int = 0,
                 limit: int = None) -> list:
        """Get a list of captures for a tag ordered newest first.

        The list can be paginated so that each call returns 'limit' captures.

        Args:
            serial (str): Base64 serial that identifies the tag to read captures from.
            offset (int): Start list at the nth capture for pagination.
            limit (int): Limit the list length for pagination.

        Returns:
            list: A list of capture dictionaries.

        """
        capturesurl = "{apiurl}/captures".format(apiurl=self.apiurl)
        queryparams = {'serial': serial,
                       'offset': offset,
                       'limit': limit}

        r = requests.get(capturesurl, params=queryparams)
        r.raise_for_status()
        ConsumerApiWrapper.process_status(r.status_code)
        captresponse = r.json()
        return captresponse

    def get(self, capture_id: int) -> dict:
        """Get one capture by its ID.

        Makes a GET request to the :ref:`Capture <CaptureConsumerAPI>` endpoint.

        Args:
            capture_id (int): Capture ID to retrieve.

        Returns:
            dict: Capture dictionary returned by the API.

        """
        capturesurl = "{apiurl}/captures/{capture_id}".format(apiurl=self.apiurl,
                                                              capture_id=capture_id)

        r = requests.get(capturesurl)
        r.raise_for_status()
        ConsumerApiWrapper.process_status(r.status_code)
        captresponse = r.json()
        return captresponse

    def get_samples(self,
                    capture_id: int,
                    page: int = 1,
                    per_page: int = 1000) -> list:
        """Get a list of samples from a capture.

        Makes a GET request to the :ref:`CaptureSamples <CaptureSamplesConsumerAPI>` endpoint.

        The list can be paginated so that each call returns 'limit' samples at an 'offset' from the first.

        Args:
            capture_id (int): Capture ID to retrieve.
            offset (int): Start list at the nth sample for pagination.
            limit (int): Limit the list length for pagination.

        Returns:
            list: A list of samples.

        """
        capturesamplesurl = "{apiurl}/captures/{capture_id}/samples".format(apiurl=self.apiurl,
                                                                            capture_id=capture_id)

        queryparams = {'page': page,
                       'per_page': per_page}

        r = requests.get(capturesamplesurl, params=queryparams)
        r.raise_for_status()
        ConsumerApiWrapper.process_status(r.status_code)
        response = r.json()
        return response

    def post(self,
             circbufb64: str,
             serial: str,
             statusb64: str,
             timeintb64: str,
             vfmtb64: str) -> dict:
        """Create a new capture from parameters encoded by wscodec.

        These data are included in URL parameters passed to wsfrontend when a tag is scanned.

        Makes a POST request to the :ref:`Capture <CapturesConsumerAPI>` endpoint, which unwraps the circular
        buffer and decodes samples.

        Args:
            circbufb64 (str): Circular buffer containing base64 encoded samples. Ouptut by wscodec.
            serial (str): Base64 serial identifying the tag the capture has originated from.
            statusb64 (str): Base64 encoded status information (e.g. battery level). Output by wscodec.
            timeintb64 (str): Base64 encoded time interval between samples. Output by wscodec.
            vfmtb64 (str): Tag version string. See wscodec.

        Returns:
            dict: Capture dictionary.

        """
        capturesurl = "{apiurl}/captures".format(apiurl=self.apiurl)
        payload = {'circbufb64': circbufb64,
                   'serial': serial,
                   'statusb64': statusb64,
                   'timeintb64': timeintb64,
                   'vfmtb64': vfmtb64}

        r = requests.post(capturesurl, json=payload)
        r.raise_for_status()
        ConsumerApiWrapper.process_status(r.status_code)
        captresponse = r.json()
        return captresponse
