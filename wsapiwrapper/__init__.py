class ApiWrapper:
    """Wraps calls to wsbackend web APIs.

    Provides a consistent and tested way to use wsbackend web APIs.
    Uses the Requests HTTP library.
    """

    def auth_header(self, tokenstr):
        """Return an HTTP header that includes the API access token.

        Args:
            tokenstr (str): API access token

        Returns:
            headers: a dictionary containing two HTTP headers.
        """
        headers = {
        'content-type': 'application/json',
        'Authorization': 'bearer {tokenstr}'.format(tokenstr=tokenstr)
        }
        return headers

    def __init__(self, baseurl):
        self.baseurl = baseurl