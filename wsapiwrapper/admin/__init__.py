import requests
from .. import ApiWrapper


class AdminApiWrapper(ApiWrapper):
    """Wraps calls to the wsbackend Admin API

    The Admin API is intended for administrators.
    """

    def get_admin_token(self):
        """Request a token from the token endpoint.

        A client_id and client_secret (similar to username and password) are exchanged
        for a token. To do this a POST request is made to wsbackend.

        Returns:
            str: token received from wsbackend.
        """
        tokenurl = "{apiurl}/token".format(apiurl=self.apiurl)
        tokenpayload = {'client_id': self.adminapi_client_id, 'client_secret': self.adminapi_client_secret}
        jsonheader = {'content-type': 'application/json'}
        r = requests.post(tokenurl, json=tokenpayload, headers=jsonheader)
        tokenresponse = r.json()['token']
        return tokenresponse

    def __init__(self, baseurl, adminapi_client_id, adminapi_client_secret):
        super().__init__(baseurl)
        self.adminapi_client_id = adminapi_client_id
        self.adminapi_client_secret = adminapi_client_secret
        self.apiurl = "{baseurl}/api/admin/v1".format(baseurl=baseurl)
        tokenstr = self.get_admin_token()
        self.headers = self.auth_header(tokenstr)
