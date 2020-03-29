from ..admin import AdminApiWrapper


class UserWrapper(AdminApiWrapper):
    """Wraps calls to capture endpoints on the Admin API. """

    def __init__(self, baseurl: str, adminapi_client_id: str, adminapi_client_secret: str):
        """Constructor for UserWrapper

        Args:
            baseurl (str): Websensor backend URL.
            adminapi_client_id (str): Client ID API access credential. A long base64 string e.g. SVpP...kO8
            adminapi_client_secret (str): Client Secret API access credential. A long base64 string e.g. CM300...1aVB
            endpoint_one (str): Endpoint for returning one resource instance.
            endpoint_many (str): Endpoint for returning a list of resource instances.
        """
        endpoint_one = "/user/"
        endpoint_many = "/users"
        super().__init__(baseurl, adminapi_client_id, adminapi_client_secret, endpoint_one, endpoint_many)