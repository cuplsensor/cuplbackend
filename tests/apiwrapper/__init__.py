class ApiWrapper:
    """Wraps calls to wsbackend APIs.

    Uses the Requests HTTP library to call wsbackend web APIs.
    """

    def __init__(self, baseurl: str):
        """Constructor for ApiWrapper.

        Args:
            baseurl (str): Websensor backend base URL.
        """
        self.baseurl = baseurl


