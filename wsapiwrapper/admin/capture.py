import requests
from ..admin import AdminApiWrapper
import json


class CaptureWrapper(AdminApiWrapper):
    """Wraps calls to capture endpoints on the Admin API. """

    def __init__(self, baseurl: str, adminapi_client_id: str, adminapi_client_secret: str):
        """Constructor for CaptureWrapper

        Args:
            baseurl (str): Websensor backend URL.
            adminapi_client_id (str): Client ID API access credential. A long base64 string e.g. SVpP...kO8
            adminapi_client_secret (str): Client Secret API access credential. A long base64 string e.g. CM300...1aVB
            endpoint_one (str): Endpoint for returning one resource instance.
            endpoint_many (str): Endpoint for returning a list of resource instances.
        """
        endpoint_one = "/capture/"
        endpoint_many = "/captures"
        super().__init__(baseurl, adminapi_client_id, adminapi_client_secret, endpoint_one, endpoint_many)

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