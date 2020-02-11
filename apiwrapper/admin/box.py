import requests
from ..admin import AdminApiWrapper


class BoxWrapper(AdminApiWrapper):
    def __init__(self, baseurl, adminapi_client_id, adminapi_client_secret):
        super().__init__(baseurl, adminapi_client_id, adminapi_client_secret)

    def post(self):
        boxesurl = "{apiurl}/boxes".format(apiurl=self.apiurl)
        r = requests.post(boxesurl, headers=self.headers)
        boxresponse = r.json()
        return boxresponse

    def delete(self, boxid):
        boxesurl = "{apiurl}/box/{boxid}".format(apiurl=self.apiurl, boxid=boxid)
        r = requests.delete(boxesurl, headers=self.headers)
        print(r.status_code)


