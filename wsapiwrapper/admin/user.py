from ..admin import AdminApiWrapper


class UserWrapper(AdminApiWrapper):
    """Wraps calls to capture endpoints on the Admin API. """

    def __init__(self, baseurl: str, adminapi_token: str):
        """Constructor for UserWrapper

        Args:
            baseurl (str): Websensor backend URL.
            adminapi_token (str): Token for accessing the admin API.
            endpoint_one (str): Endpoint for returning one resource instance.
            endpoint_many (str): Endpoint for returning a list of resource instances.
        """
        endpoint_one = "/user/"
        endpoint_many = "/users"
        super().__init__(baseurl, adminapi_token, endpoint_one, endpoint_many)