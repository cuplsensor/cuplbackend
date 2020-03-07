import requests
from . import ConsumerApiWrapper


class BoxScannedWrapper(ConsumerApiWrapper):
    """Wraps a Consumer API endpoint for determining if a box has been scanned by a user."""

    def get(self, boxserial: str) -> bool:
        """

        Args:
            boxserial (str):  Base64 serial that uniquely identifies a box (hardware module).

        Returns:
            bool: True if the box has been scanned a user identified in the token header. False otherwise.

        """
        boxscannedurl = "{apiurl}/box/{boxserial}/scanned".format(apiurl=self.apiurl,
                                                                  boxserial=boxserial)
        r = requests.get(boxscannedurl, headers=self.headers)

        ConsumerApiWrapper.process_status(r.status_code)

        response = r.json()
        return response