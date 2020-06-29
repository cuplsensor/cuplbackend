import requests
from ..admin import AdminApiWrapper
import json


class TagWrapper(AdminApiWrapper):
    """Wraps calls to tag endpoints on the Admin API.
    """

    def __init__(self, baseurl: str, adminapi_client_id: str, adminapi_client_secret: str):
        """Constructor for TagWrapper

        Args:
            baseurl (str): Websensor backend URL.
            adminapi_client_id (str): Client ID API access credential. A long base64 string e.g. SVpP...kO8
            adminapi_client_secret (str): Client Secret API access credential. A long base64 string e.g. CM300...1aVB
            endpoint_one (str): Endpoint for returning one resource instance.
            endpoint_many (str): Endpoint for returning a list of resource instances.
        """
        endpoint_one = "/tag/"
        endpoint_many = "/tags"
        super().__init__(baseurl, adminapi_client_id, adminapi_client_secret, endpoint_one, endpoint_many)

    def simulate(self, tagid: int, frontendurl: str, nsamples: int = 100) -> str:
        """Make a GET request to the :ref:`TagAdminAPI` simulate endpoint.

        Returns:
            str: A string containing a simulated tag URL
        """

        tagurl = "{apiurl}/tag/{tagid}/simulate".format(apiurl=self.apiurl, tagid=tagid)
        params = {'frontendurl': frontendurl, 'nsamples': nsamples}
        r = requests.get(tagurl, params=params, headers=self.headers)
        tagresponse = r.json()
        return tagresponse

    def post(self, tagid: int = None) -> dict:
        """Make a POST request to the :ref:`TagAdminAPI` endpoint.

        Returns:
            dict: A dictionary representing the new tag object.

        """
        tagsurl = "{apiurl}/tags".format(apiurl=self.apiurl)
        if tagid is not None:
            payload = {'id': tagid}
        else:
            payload = None
        r = requests.post(tagsurl, data=payload, headers=self.headers)
        tagresponse = r.json()
        return tagresponse


