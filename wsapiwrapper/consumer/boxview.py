import requests
from . import ConsumerApiWrapper


class BoxViewWrapper(ConsumerApiWrapper):
    def __init__(self, baseurl: str, tokenstr: str):
        super().__init__(baseurl, tokenstr)
        self.boxviewsurl = "{apiurl}/me/boxviews".format(apiurl=self.apiurl)

    def get(self, distinct: bool = False):
        """Get a list of box views by the current user.

        Current user is identified by an API access token. This must be passed to the :py:func:`constructor <__init__>`.

        Args:
            distinct (bool): When true only the most recent BoxView for each box will be returned.

        Returns: A list of boxes that the user has recently viewed.

        """
        queryparams = None

        if distinct is True:
            queryparams = {'distinctonbox': 'true'}

        try:
            r = requests.get(self.boxviewsurl, params=queryparams, headers=self.headers)
            boxviewresponse = r.json()
        except requests.exceptions.RequestException as e:
            BoxViewWrapper.process_status(e.response.status_code, str(e))

        return boxviewresponse

    def post(self, boxserial: str):
        """Record that the current user has viewed a box.

        Makes a POST request to the :ref:`BoxView <BoxViewConsumerAPI>` Consumer API endpoint.

        Current user is identified by the API access token (required).

        Args:
            boxserial (str): Base64 serial that uniquely identifies a box (hardware module).

        Returns:

        """
        payload = {'boxserial': boxserial}
        try:
            r = requests.post(self.boxviewsurl, json=payload, headers=self.headers)
            boxviewresponse = r.json()
        except requests.exceptions.RequestException as e:
            BoxViewWrapper.process_status(e.response.status_code, str(e))

        return boxviewresponse

