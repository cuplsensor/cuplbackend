import requests
from ..admin import AdminApiWrapper
import json


class CaptureWrapper(AdminApiWrapper):
    def post(self, capturepayload):
        captpayload = json.dumps(capturepayload)
        capturesurl = "{adminapiurl}/captures".format(adminapiurl=self.adminapiurl)
        r = requests.post(capturesurl, data=captpayload, headers=self.headers)
        if r.status_code != 200:
            raise Exception('Capture Write Failed')
        captresponse = r.json()
        return captresponse