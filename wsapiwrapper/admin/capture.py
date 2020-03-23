import requests
from ..admin import AdminApiWrapper
import json


class CaptureWrapper(AdminApiWrapper):
    """Wraps calls to capture endpoints on the Admin API. """

    def post(self, capturepayload: dict):
        """Create a capture in the database directly.

        The is made from a dictionary including a list of samples, a box_id and a user_id. The
        endpoint is used for testing. It removes the need to encode test vectors with wscodec (introduces
        a second point of failure in an external library).

        Captures can be created with a known list of samples. Then samples are collected from the box
        using the consumer API. These are compared with a vector of expected samples. If captures overlap slightly in
        time it is expected that duplicate samples are removed.

        Args:
            capturepayload (dict): Dictionary following the :ref:`capture schema <CapturesConsumerAPI>`.

        Returns: HTTP response from wsbackend.

        """
        captpayload = json.dumps(capturepayload)
        capturesurl = "{apiurl}/captures".format(apiurl=self.apiurl)
        r = requests.post(capturesurl, data=captpayload, headers=self.headers)
        if r.status_code != 200:
            raise Exception('Capture Write Failed')
        captresponse = r.json()
        return captresponse