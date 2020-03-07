import requests
from . import ConsumerApiWrapper


class BoxWrapper(ConsumerApiWrapper):
    """Wraps calls to box endpoints on the Consumer API"""

    def get(self, boxserial: str) -> dict:
        """

        Args:
            boxserial (str): Base64 serial that uniquely identifies a box (hardware module).

        Returns: Box dictionary. Converted from a JSON dictionary described :ref:`here <BoxConsumerAPI>`.

        """
        boxurl = "{apiurl}/box/{boxserial}".format(apiurl=self.apiurl,
                                                   boxserial=boxserial)
        r = requests.get(boxurl)

        ConsumerApiWrapper.process_status(r.status_code)

        response = r.json()
        return response
