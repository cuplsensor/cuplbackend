import requests
from . import ConsumerApiWrapper


class MeCaptureWrapper(ConsumerApiWrapper):
    """Create and retrieve captures linked to the current user. """

    def get(self, distinct: bool = False):
        """Get a list of captures made by the current user.

        Makes a GET request to the :ref:`MeCaptures <MeCapturesConsumerAPI>` endpoint.

        Args:
            distinct (bool): When true, only the most recent capture is returned for each box.

        Returns:
            list: A list of capture dictionaries.

        """
        capturesurl = "{apiurl}/me/captures".format(apiurl=self.apiurl)
        queryparams = None

        if distinct is True:
            queryparams = {'distinctonbox': 'true'}

        try:
            r = requests.get(capturesurl, params=queryparams, headers=self.headers)
            captresponse = r.json()
        except requests.exceptions.RequestException as e:
            ConsumerApiWrapper.process_status(e.response.status_code, str(e))

        return captresponse

    def post(self,
             circbufb64: str,
             serial: str,
             statusb64: str,
             timeintb64: str,
             versionStr: str) -> dict:
        """Create a new capture. Record that it was made by the current user.

        See :py:meth:`wsapiwrapper.consumer.capture.CaptureWrapper.post`.

        """
        capturesurl = "{apiurl}/me/captures".format(apiurl=self.apiurl)
        payload = {'circbufb64': circbufb64,
                   'serial': serial,
                   'statusb64': statusb64,
                   'timeintb64': timeintb64,
                   'versionStr': versionStr}

        try:
            r = requests.get(capturesurl, json=payload, headers=self.headers)
            captresponse = r.json()
        except requests.exceptions.RequestException as e:
            ConsumerApiWrapper.process_status(e.response.status_code, str(e))

        return captresponse
