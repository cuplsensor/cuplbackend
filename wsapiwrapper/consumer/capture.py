import requests
from . import ConsumerApiWrapper


class CaptureWrapper(ConsumerApiWrapper):
    """Wraps capture endpoints of the Consumer API. """

    def get_list(self,
                 serial: str,
                 offset: int = 0,
                 limit: int = None) -> list:
        """Get a list of captures for a box ordered newest first.

        The list can be paginated so that each call returns 'limit' captures.

        Args:
            serial: Base64 serial that identifies the box to read captures from.
            offset: For pagination, drop captures from the start of the list.
            limit: For pagination, constraint the number of elements in a list.

        Returns:
            list: A list of capture elements.

        """
        capturesurl = "{apiurl}/captures".format(apiurl=self.apiurl)
        queryparams = {'serial': serial,
                       'offset': offset,
                       'limit': limit}

        r = requests.get(capturesurl, params=queryparams)
        ConsumerApiWrapper.process_status(r.status_code)
        captresponse = r.json()
        return captresponse

    def get(self, capture_id: int) -> dict:
        """

        Args:
            capture_id:

        Returns:

        """
        capturesurl = "{apiurl}/captures/{capture_id}".format(apiurl=self.apiurl,
                                                              capture_id=capture_id)

        r = requests.get(capturesurl)
        ConsumerApiWrapper.process_status(r.status_code)
        captresponse = r.json()
        return captresponse

    def get_samples(self, capture_id, offset=0, limit=None):
        capturesamplesurl = "{apiurl}/captures/{capture_id}/samples".format(apiurl=self.apiurl,
                                                                            capture_id=capture_id)

        queryparams = {'offset': offset,
                       'limit': limit}

        r = requests.get(capturesamplesurl, params=queryparams)
        ConsumerApiWrapper.process_status(r.status_code)
        response = r.json()
        return response

    def post(self, circbufb64, serial, statusb64, timeintb64, versionStr):
        capturesurl = "{apiurl}/captures".format(apiurl=self.apiurl)
        payload = {'circbufb64': circbufb64,
                   'serial': serial,
                   'statusb64': statusb64,
                   'timeintb64': timeintb64,
                   'ver': versionStr}

        r = requests.post(capturesurl, json=payload)
        ConsumerApiWrapper.process_status(r.status_code)
        captresponse = r.json()
        return captresponse
