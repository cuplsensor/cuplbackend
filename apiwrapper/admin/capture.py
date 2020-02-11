import requests
from ..admin import AdminApiWrapper
import json


class CaptureWrapper(AdminApiWrapper):
    def __init__(self, baseurl, adminapi_client_id, adminapi_client_secret):
        super().__init__(baseurl, adminapi_client_id, adminapi_client_secret)

    def post(self, capturepayload):
        captpayload = json.dumps(capturepayload)
        capturesurl = "{apiurl}/captures".format(apiurl=self.apiurl)
        r = requests.post(capturesurl, data=captpayload, headers=self.headers)
        if r.status_code != 200:
            raise Exception('Capture Write Failed')
        captresponse = r.json()
        return captresponse