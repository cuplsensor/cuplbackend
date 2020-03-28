import requests
from ..admin import AdminApiWrapper
import json


class BoxWrapper(AdminApiWrapper):
    """Wraps calls to box endpoints on the Admin API.
    """

    def __init__(self, baseurl: str, adminapi_client_id: str, adminapi_client_secret: str):
        """Constructor for BoxWrapper

        Args:
            baseurl (str): Websensor backend URL.
            adminapi_client_id (str): Client ID API access credential. A long base64 string e.g. SVpP...kO8
            adminapi_client_secret (str): Client Secret API access credential. A long base64 string e.g. CM300...1aVB
            endpoint_one (str): Endpoint for returning one resource instance.
            endpoint_many (str): Endpoint for returning a list of resource instances.
        """
        endpoint_one = "/box/"
        endpoint_many = "/boxes"
        super().__init__(baseurl, adminapi_client_id, adminapi_client_secret, endpoint_one, endpoint_many)

    def simulate(self, boxid: int, frontendurl: str, nsamples: int = 100) -> str:
        """Make a GET request to the :ref:`BoxAdminAPI` simulate endpoint.

        Returns:
            str: A string containing a simulated box URL
        """

        boxurl = "{apiurl}/box/{boxid}/simulate".format(apiurl=self.apiurl, boxid=boxid)
        params = {'frontendurl': frontendurl, 'nsamples': nsamples}
        r = requests.get(boxurl, params=params, headers=self.headers)
        boxresponse = r.json()
        return boxresponse

    def post(self, boxid: int = None) -> dict:
        """Make a POST request to the :ref:`BoxAdminAPI` endpoint.

        Returns:
            dict: A dictionary representing the new box object.

        """
        boxesurl = "{apiurl}/boxes".format(apiurl=self.apiurl)
        if boxid is not None:
            payload = {'id': boxid}
        else:
            payload = None
        r = requests.post(boxesurl, data=payload, headers=self.headers)
        boxresponse = r.json()
        return boxresponse


