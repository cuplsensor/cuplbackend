import requests
from . import ConsumerApiWrapper


class TagScannedWrapper(ConsumerApiWrapper):
    """Wraps a Consumer API endpoint for determining if a tag has been scanned by a user."""

    def get(self, tagserial: str) -> bool:
        """Makes a GET request to the :ref:`TagScanned <TagScannedConsumerAPI>` Consumer API endpoint.

        Current user is identified by an access token passed to the
        :py:func:`constructor <wsapiwrapper.consumer.ConsumerApiWrapper.__init__>`.

        Args:
            tagserial (str):  Base64 serial that uniquely identifies a tag (hardware module).

        Returns:
            bool: True if the tag has been scanned a user identified in the token header. False otherwise.

        """
        tagscannedurl = "{apiurl}/tag/{tagserial}/scanned".format(apiurl=self.apiurl,
                                                                  tagserial=tagserial)
        r = requests.get(tagscannedurl, headers=self.headers)
        r.raise_for_status()

        ConsumerApiWrapper.process_status(r.status_code)

        response = r.json()
        return response