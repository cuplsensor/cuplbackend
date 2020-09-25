import requests
from .. import ApiWrapper


def api_url(baseurl: str) -> str:
    return "{baseurl}/api/admin".format(baseurl=baseurl)


def request_admin_token(baseurl: str, adminapi_client_id: str, adminapi_client_secret: str) -> str:
    """Request a token from the token endpoint.

    A client_id and client_secret are exchanged for a token. This uses
    the OAuth Client Credentials flow:

    1. A POST request is made to the token endpoint of wsbackend.
    2. Client ID and Client Secret are validated.
    3. Access token is returned.

    Returns:
        str: token received from wsbackend.
    """
    apiurl = api_url(baseurl)
    tokenurl = "{apiurl}/token".format(apiurl=apiurl)
    tokenpayload = {'client_id': adminapi_client_id, 'client_secret': adminapi_client_secret}
    jsonheader = {'content-type': 'application/json'}
    r = requests.post(tokenurl, json=tokenpayload, headers=jsonheader)
    r.raise_for_status()
    tokenresponse = r.json()['token']
    return tokenresponse


class AdminApiWrapper(ApiWrapper):
    """Wraps calls to the wsbackend Admin API

    The Admin API is intended for administrators.
    """
    def auth_header(self, tokenstr):
        """Get a dictionary of headers. One contains an API access token.
        This is needed for some API requests to be authorized.

        Args:
            tokenstr (str): API access token

        Returns:
            dict: a dictionary containing two HTTP headers.
        """
        headers = {
        'content-type': 'application/json',
        'Authorization': 'bearer {tokenstr}'.format(tokenstr=tokenstr)
        }
        return headers

    def get(self, id: int) -> dict:
        """Make a GET request to endpoint_single.

        Returns:
            dict: A dictionary representing a tag object.
        """
        url_one = "{apiurl}{endpoint_one}{id}".format(apiurl=self.apiurl, endpoint_one=self.endpoint_one, id=id)
        r = requests.get(url_one, headers=self.headers)
        r.raise_for_status()
        response = r.json()
        return response

    def get_many(self, offset: int = 0, limit: int = None, **kwargs) -> list:
        """Makes a GET request to endpoint_many.

        Args:
            offset (int):  Return captures with an ID greater than this number.
            limit (int): Number of captures to return.

        Returns:
            list: A list of resource dictionaries
        """
        url_many = "{apiurl}{endpoint_many}".format(apiurl=self.apiurl, endpoint_many=self.endpoint_many)
        params = {'offset': offset, 'limit': limit}
        params.update(kwargs) # Add extra key/value pairs to the params dictionary
        r = requests.get(url_many, params=params, headers=self.headers)
        r.raise_for_status()
        response = r.json()
        return response

    def delete(self, id: int):
        """Make a DELETE request to the :ref:`TagAdminAPI` endpoint.

        Args:
            id (int): ID of the resource to delete

        """
        url_one = "{apiurl}{endpoint_one}{id}".format(apiurl=self.apiurl, endpoint_one=self.endpoint_one, id=id)
        r = requests.delete(url_one, headers=self.headers)
        r.raise_for_status()
        print(r.status_code)

    def __init__(self, baseurl: str, tokenstr: str, endpoint_one: str, endpoint_many: str):
        """Constructor for AdminApiWrapper

        Args:
            baseurl (str): Websensor backend URL.
            adminapi_client_id (str): Client ID API access credential. A long base64 string e.g. SVpP...kO8
            adminapi_client_secret (str): Client Secret API access credential. A long base64 string e.g. CM300...1aVB
            endpoint_one (str): Endpoint for returning one resource instance.
            endpoint_many (str): Endpoint for returning a list of resource instances.
        """
        super().__init__(baseurl)
        self.headers = self.auth_header(tokenstr)
        self.endpoint_one = endpoint_one
        self.endpoint_many = endpoint_many
        self.apiurl = api_url(baseurl)
