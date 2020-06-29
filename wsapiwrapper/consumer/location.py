import requests
from . import ConsumerApiWrapper, Exception401


class NoScanOnTagException(Exception401):
    """Location data cannot be modified on tags that have not been scanned."""

    def __init__(self):
        super().__init__(message="Not authorised because the user has not scanned the parent tag. ")


class LocationWrapper(ConsumerApiWrapper):
    """Wraps location endpoints of the Consumer API. """

    @staticmethod
    def process_status(status_code: int, desc="") -> None:
        """Raise an exception in response to an HTTP error code.

        Args:
            status_code: `HTTP status code <https://en.wikipedia.org/wiki/List_of_HTTP_status_codes>`_.

        """
        if status_code == 401:
            raise NoScanOnTagException
        else:
            ConsumerApiWrapper.process_status(status_code)

    def __init__(self, baseurl: str, tokenstr: str):
        super().__init__(baseurl, tokenstr)
        self.locationsurl = "{apiurl}/locations".format(apiurl=self.apiurl)

    def get(self, location_id: int) -> dict:
        """Get one location by its ID.

        Makes a GET request to the :ref:`Location <LocationsConsumerAPI>` endpoint.

        Args:
            location_id (int): Location ID to retrieve.

        Returns:
            dict: Location dictionary returned by the API.

        """
        r = requests.get("{locationsurl}/{id}".format(locationsurl=self.locationsurl, id=location_id),
                         headers=self.headers)
        r.raise_for_status()
        LocationWrapper.process_status(r.status_code)
        response = r.json()
        return response

    def delete(self, location_id: int) -> int:
        """Delete one location by ID.

        Makes a DELETE request to the :ref:`Location <LocationsConsumerAPI>` endpoint. To delete locations the
        current user must have scanned the tag.

        Args:
            location_id (int): Location ID to delete.

        Returns:
            int: HTTP status code.

        """
        r = requests.delete("{locationsurl}/{id}".format(locationsurl=self.locationsurl, id=location_id),
                            headers=self.headers)

        LocationWrapper.process_status(r.status_code)
        return r.status_code

    def get_list(self,
                 tagserial: str,
                 starttime: str = None,
                 endtime: str = None) -> list:
        """Get a list of locations for a tag.

        Optionally a time window can be specified, so that only location timestamps within that window will be returned.

        Makes a GET request to the :ref:`Locations <LocationsConsumerAPI>` endpoint.

        Args:
            tagserial: Base64 serial identifying a tag.
            starttime: Start datetime as an ISO-8601 string.
            endtime: End datetime as an ISO-8601 string.

        Returns:
            list: A list of Location dictionaries.

        """
        queryparams = {'tagserial': tagserial}

        if starttime is not None:
            queryparams['starttime'] = starttime

        if endtime is not None:
            queryparams['endtime'] = endtime

        r = requests.get(self.locationsurl, params=queryparams, headers=self.headers)
        r.raise_for_status()
        LocationWrapper.process_status(r.status_code)
        response = r.json()
        return response

    def post(self, capturesample_id: int, description: str) -> dict:
        """Annotate a sample with location.

        The timestamp of a location corresponds to that of its parent sample. All samples can be traced back to the
        tag that created them. This must have been scanned by the current user.

        Args:
            capturesample_id (int): Capturesample ID to annotate.
            description (str): The tag location e.g. under the stairs.

        Returns:
            dict: Location dictionary returned by the API and converted from JSON.

        """
        payload = {'capturesample_id': capturesample_id,
                   'description': description}
        r = requests.post(self.locationsurl, json=payload, headers=self.headers)
        r.raise_for_status()
        LocationWrapper.process_status(r.status_code)
        response = r.json()
        return response

    def patch(self, location_id: int, description: str) -> dict:
        """Change description of an existing location.

        The current user must have scanned the tag.

        Args:
            location_id (int): Location ID to modify.
            description: New tag location (e.g. above the fireplace).

        Returns:
            dict: Location dictionary returned by the API.

        """
        payload = {'description': description}
        r = requests.patch("{locationsurl}/{id}".format(locationsurl=self.locationsurl, id=location_id),
                           json=payload,
                           headers=self.headers)
        r.raise_for_status()
        # Raise an exception in the event of a non-zero return code.
        LocationWrapper.process_status(r.status_code)
        response = r.json()
        return response

