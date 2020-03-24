import requests
from ..admin import AdminApiWrapper
import json


class BoxWrapper(AdminApiWrapper):
    """Wraps calls to box endpoints on the Admin API.
    """

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

    def get_many(self, offset: int = 0, limit: int = None) -> list:
        """Make a GET request to the :ref:`BoxAdminAPI` endpoint.

        Returns:
            list: A list of box dictionaries
        """
        boxesurl = "{apiurl}/boxes".format(apiurl=self.apiurl)
        params = {'offset': offset, 'limit': limit}
        r = requests.get(boxesurl, params=params, headers=self.headers)
        boxresponse = r.json()
        return boxresponse

    def get(self, boxid: int) -> dict:
        """Make a GET request to the :ref:`BoxAdminAPI` endpoint.

        Returns:
            dict: A dictionary representing a box object.
        """

        boxurl = "{apiurl}/box/{boxid}".format(apiurl=self.apiurl, boxid=boxid)
        r = requests.get(boxurl, headers=self.headers)
        boxresponse = r.json()
        return boxresponse

    def delete(self, boxid: int):
        """Make a DELETE request to the :ref:`BoxAdminAPI` endpoint.

        Args:
            boxid (int): ID of the box to delete

        """
        boxesurl = "{apiurl}/box/{boxid}".format(apiurl=self.apiurl, boxid=boxid)
        r = requests.delete(boxesurl, headers=self.headers)
        print(r.status_code)

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


