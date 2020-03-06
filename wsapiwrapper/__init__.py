class ApiWrapper:
    """Wraps calls to wsbackend APIs.

    Uses the Requests HTTP library to call wsbackend web APIs.
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

    def __init__(self, baseurl):
        """Constructor for ApiWrapper.

        Args:
            baseurl (str): Websensor backend base URL.
        """
        self.baseurl = baseurl