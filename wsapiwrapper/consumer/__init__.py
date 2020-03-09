from .. import ApiWrapper


class ConsumerApiWrapper(ApiWrapper):
    def __init__(self, baseurl: str, tokenstr: str = None):
        """Constructor for ConsumerApiWrapper

        Args:
            baseurl (str): Websensor backend base URL.
            tokenstr (str): OAuth access token.
        """
        super().__init__(baseurl)
        self.apiurl = "{baseurl}/api/consumer/v1".format(baseurl=self.baseurl)
        if tokenstr is not None:
            self.headers = self.auth_header(tokenstr)

    @staticmethod
    def process_status(status_code, desc=None):
        """ Raise an exception for HTTP error statuses"""
        if status_code == 400:
            raise Exception400
        elif status_code == 401:
            raise Exception401(message=desc)
        elif status_code == 403:
            raise Exception403
        elif status_code == 404:
            raise Exception404
        elif status_code == 409:
            raise Exception409
        elif status_code > 400:
            print(status_code)
            raise ConsumerAPIException(message=desc)


class ConsumerAPIException(Exception):
    def __init__(self, message):
        super().__init__("Consumer API Error: {}".format(message))


class Exception404(Exception):
    def __init__(self, message="404 Resource not found"):
        super().__init__(message)


class Exception409(Exception):
    def __init__(self, message="409 Resource already exists"):
        super().__init__(message)


class Exception400(Exception):
    def __init__(self, message="400 Bad input"):
        super().__init__(message)


class Exception403(Exception):
    def __init__(self, message="Forbidden."):
        super().__init__(message)


class Exception401(Exception):
    def __init__(self, message="Not authorised to access this resource. "
                               "Invalid JWT or bad HMAC."):
        super().__init__("Exception 401 " + str(message))
