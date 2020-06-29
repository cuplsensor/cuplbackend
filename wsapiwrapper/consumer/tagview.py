import requests
from . import ConsumerApiWrapper


class TagViewWrapper(ConsumerApiWrapper):
    def __init__(self, baseurl: str, tokenstr: str):
        super().__init__(baseurl, tokenstr)
        self.tagviewsurl = "{apiurl}/me/tagviews".format(apiurl=self.apiurl)

    def get(self, distinct: bool = False) -> list:
        """Get a list of tag views by the current user.

        Current user is identified by an API access token passed to the :py:func:`constructor <__init__>`.

        Args:
            distinct (bool): When true only the most recent TagView for each tag will be returned.

        Returns:
            list: A list of timestamped tag views.

        """
        queryparams = None

        if distinct is True:
            queryparams = {'distinctontag': 'true'}

        try:
            r = requests.get(self.tagviewsurl, params=queryparams, headers=self.headers)
            r.raise_for_status()
            tagviewresponse = r.json()
        except requests.exceptions.RequestException as e:
            TagViewWrapper.process_status(e.response.status_code, str(e))

        return tagviewresponse

    def post(self, tagserial: str) -> dict:
        """Record that the current user has viewed a tag.

        Makes a POST request to the :ref:`TagView <TagViewConsumerAPI>` Consumer API endpoint.

        Current user is identified by the API access token passed to the
        :py:func:`constructor <wsapiwrapper.consumer.ConsumerApiWrapper.__init__>`.

        Args:
            tagserial (str): Base64 serial that uniquely identifies a tag (hardware module).

        Returns:
            dict: API representation of the newly created tag view.

        """
        payload = {'tagserial': tagserial}
        try:
            r = requests.post(self.tagviewsurl, json=payload, headers=self.headers)
            r.raise_for_status()
            tagviewresponse = r.json()
        except requests.exceptions.RequestException as e:
            TagViewWrapper.process_status(e.response.status_code, str(e))

        return tagviewresponse

