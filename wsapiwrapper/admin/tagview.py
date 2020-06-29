from ..admin import AdminApiWrapper


class TagViewWrapper(AdminApiWrapper):
    """Wraps calls to capture endpoints on the Admin API. """

    def __init__(self, baseurl: str, adminapi_client_id: str, adminapi_client_secret: str):
        """Constructor for TagViewWrapper

        Args:
            baseurl (str): Websensor backend URL.
            adminapi_client_id (str): Client ID API access credential. A long base64 string e.g. SVpP...kO8
            adminapi_client_secret (str): Client Secret API access credential. A long base64 string e.g. CM300...1aVB
            endpoint_one (str): Endpoint for returning one resource instance.
            endpoint_many (str): Endpoint for returning a list of resource instances.
        """
        endpoint_one = "/tagview/"
        endpoint_many = "/tagviews"
        super().__init__(baseurl, adminapi_client_id, adminapi_client_secret, endpoint_one, endpoint_many)

    def get_many(self, offset: int = 0, limit: int = None, tag_id: int = None) -> list:
        """Makes a GET request to endpoint_many.

        Args:
            offset (int):  Return captures with an ID greater than this number.
            limit (int): Number of captures to return.
            tag_id (int): Filter by tag_id (optional)

        Returns:
            list: A list of capture dictionaries
        """
        kwargs = {'offset': offset, 'limit': limit}

        if tag_id is not None:
            kwargs.update({'tag_id': tag_id})

        return super().get_many(**kwargs)