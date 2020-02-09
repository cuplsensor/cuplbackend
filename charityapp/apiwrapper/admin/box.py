import requests
from ..admin import AdminApiWrapper
import json


class BoxWrapper(AdminApiWrapper):
    def post(self):
        boxesurl = "{adminapiurl}/boxes".format(adminapiurl=self.adminapiurl)
        r = requests.post(boxesurl, headers=self.headers)
        boxresponse = r.json()
        return boxresponse

    def delete(self, boxid):
        boxesurl = "{adminapiurl}/box/{boxid}".format(adminapiurl=self.adminapiurl, boxid=boxid)
        r = requests.delete(boxesurl, headers=self.headers)
        print(r.status_code)


