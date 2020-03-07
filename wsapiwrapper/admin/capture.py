import requests
from ..admin import AdminApiWrapper
import json


class CaptureWrapper(AdminApiWrapper):
    """Wraps calls to capture endpoints on the Admin API. """
    def post(self, capturepayload):
        """Create a capture in the database directly.

        The capture is made from a dictionary. This includes a list of samples, a box_id and a user_id. This
        endpoint, used for testing, removes the need to pass capture data encoded by wscodec.

        Specifically captures can be created with a known list of samples. Then samples are collected from the box
        using the consumer API. These are compared with a vector of expected samples. If captures overlap slightly in
        time it is expected that duplicate samples are removed.

        Args:
            capturepayload: JSON dictionary following the :ref:`capture schema <CapturesConsumerAPI>`.

        Returns: HTTP response from wsbackend.

        """
        captpayload = json.dumps(capturepayload)
        capturesurl = "{apiurl}/captures".format(apiurl=self.apiurl)
        r = requests.post(capturesurl, data=captpayload, headers=self.headers)
        if r.status_code != 200:
            raise Exception('Capture Write Failed')
        captresponse = r.json()
        return captresponse