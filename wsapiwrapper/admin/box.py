import requests
from ..admin import AdminApiWrapper


class BoxWrapper(AdminApiWrapper):
    """Wraps calls to box endpoints on the Admin API.
    """

    def post(self):
        """Makes a call to :ref:`BoxConsumerAPI`

        Returns:

        """
        boxesurl = "{apiurl}/boxes".format(apiurl=self.apiurl)
        r = requests.post(boxesurl, headers=self.headers)
        boxresponse = r.json()
        return boxresponse

    def delete(self, boxid):
        boxesurl = "{apiurl}/box/{boxid}".format(apiurl=self.apiurl, boxid=boxid)
        r = requests.delete(boxesurl, headers=self.headers)
        print(r.status_code)


