import requests
from . import ConsumerApiWrapper


class TagWrapper(ConsumerApiWrapper):
    """Wraps calls to tag endpoints on the Consumer API"""

    def get(self, tagserial: str) -> dict:
        """

        Args:
            tagserial (str): Base64 serial that uniquely identifies a tag (hardware module).

        Returns: Tag dictionary as described :ref:`here <TagConsumerAPI>`.

        """
        tagurl = "{apiurl}/tag/{tagserial}".format(apiurl=self.apiurl,
                                                   tagserial=tagserial)
        r = requests.get(tagurl)
        r.raise_for_status()

        ConsumerApiWrapper.process_status(r.status_code)

        response = r.json()
        return response
