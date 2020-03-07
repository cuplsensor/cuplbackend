import requests
from . import ConsumerApiWrapper


class BoxWrapper(ConsumerApiWrapper):
    """Wraps calls to box endpoints on the Consumer API"""

    def get(self, boxserial):
        """

        Args:
            boxserial (str): 8 character alphanumeric serial string.

        Returns: Box object. Converted from a JSON dictionary described :ref:`here <BoxConsumerAPI>`.

        """
        boxurl = "{apiurl}/box/{boxserial}".format(apiurl=self.apiurl,
                                                   boxserial=boxserial)
        r = requests.get(boxurl)

        ConsumerApiWrapper.process_status(r.status_code)

        response = r.json()
        return response
