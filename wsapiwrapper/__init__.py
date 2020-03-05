class ApiWrapper:
    """Wraps calls to wsbackend APIs.

    Provides a consistent way to call wsbackend web APIs.
    Uses the Requests HTTP library.
    """

    def auth_header(self, tokenstr):
        """Return an HTTP headers dictionary to be passed on API requests.

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

    def __init__(self, baseurl):
        """Constructor for ApiWrapper.

        Args:
            baseurl (str): Websensor backend base URL.
        """
        self.baseurl = baseurl