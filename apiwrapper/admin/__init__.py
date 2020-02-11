import requests
from .. import ApiWrapper
from ..config import adminapi_client_id, adminapi_client_secret


class AdminApiWrapper(ApiWrapper):
    def get_admin_token(self):
        tokenurl = "{adminapiurl}/token".format(adminapiurl=self.adminapiurl)
        tokenpayload = {'client_id': adminapi_client_id, 'client_secret': adminapi_client_secret}
        jsonheader = {'content-type': 'application/json'}
        r = requests.post(tokenurl, json=tokenpayload, headers=jsonheader)
        tokenresponse = r.json()['token']
        return tokenresponse

    def __init__(self):
        super().__init__()
        tokenstr = self.get_admin_token()
        self.headers = self.auth_header(tokenstr)