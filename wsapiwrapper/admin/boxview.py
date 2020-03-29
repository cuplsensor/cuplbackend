from ..admin import AdminApiWrapper


class BoxViewWrapper(AdminApiWrapper):
    """Wraps calls to capture endpoints on the Admin API. """

    def __init__(self, baseurl: str, adminapi_client_id: str, adminapi_client_secret: str):
        """Constructor for BoxViewWrapper

        Args:
            baseurl (str): Websensor backend URL.
            adminapi_client_id (str): Client ID API access credential. A long base64 string e.g. SVpP...kO8
            adminapi_client_secret (str): Client Secret API access credential. A long base64 string e.g. CM300...1aVB
            endpoint_one (str): Endpoint for returning one resource instance.
            endpoint_many (str): Endpoint for returning a list of resource instances.
        """
        endpoint_one = "/boxview/"
        endpoint_many = "/boxviews"
        super().__init__(baseurl, adminapi_client_id, adminapi_client_secret, endpoint_one, endpoint_many)

    def get_many(self, offset: int = 0, limit: int = None, box_id: int = None) -> list:
        """Makes a GET request to endpoint_many.

        Args:
            offset (int):  Return captures with an ID greater than this number.
            limit (int): Number of captures to return.
            box_id (int): Filter by box_id (optional)

        Returns:
            list: A list of capture dictionaries
        """
        kwargs = {'offset': offset, 'limit': limit}

        if box_id is not None:
            kwargs.update({'box_id': box_id})

        return super().get_many(**kwargs)