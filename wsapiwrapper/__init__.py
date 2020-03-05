class ApiWrapper:
    """Wraps calls to wsbackend web APIs.

    Provides a consistent and tested way to use wsbackend web APIs.
    Uses the Requests HTTP library.
    """

    def auth_header(self, tokenstr):
        headers = {
        'content-type': 'application/json',
        'Authorization': 'bearer {tokenstr}'.format(tokenstr=tokenstr)
        }
        return headers

    def __init__(self, baseurl):
        self.baseurl = baseurl