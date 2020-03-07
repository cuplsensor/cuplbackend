import requests
from ..admin import AdminApiWrapper


class BoxWrapper(AdminApiWrapper):
    """Wraps calls to box endpoints on the Admin API.
    """

    def post(self):
        """Make a POST request to the :ref:`BoxAdminAPI` endpoint.

        Returns: A new box object.

        """
        boxesurl = "{apiurl}/boxes".format(apiurl=self.apiurl)
        r = requests.post(boxesurl, headers=self.headers)
        boxresponse = r.json()
        return boxresponse

    def delete(self, boxid):
        """Make a DELETE request to the :ref:`BoxAdminAPI` endpoint.

        Args:
            boxid: ID of the box to delete

        """
        boxesurl = "{apiurl}/box/{boxid}".format(apiurl=self.apiurl, boxid=boxid)
        r = requests.delete(boxesurl, headers=self.headers)
        print(r.status_code)


