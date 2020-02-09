import os
import requests
from .. import ApiWrapper


class AdminApiWrapper(ApiWrapper):
    def get_admin_token(self):
        tokenurl = "{adminapiurl}/token".format(adminapiurl=self.adminapiurl)
        client_id = os.environ['ADMINAPI_CLIENTID']
        client_secret = os.environ['ADMINAPI_CLIENTSECRET']
        tokenpayload = {'client_id': client_id, 'client_secret': client_secret}
        jsonheader = {'content-type':'application/json'}
        r = requests.post(tokenurl, json=tokenpayload, headers=jsonheader)
        tokenresponse = r.json()['token']
        return tokenresponse

    def __init__(self):
        super().__init__()
        tokenstr = self.get_admin_token()
        self.headers = self.auth_header(tokenstr)