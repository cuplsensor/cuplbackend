import requests
from . import ConsumerApiWrapper


class BoxScannedWrapper(ConsumerApiWrapper):
    def __init__(self, tokenstr):
        super().__init__(tokenstr)

    def get(self, boxserial):
        boxscannedurl = "{consumerapiurl}/box/{boxserial}/scanned".format(consumerapiurl=self.consumerapiurl,
                                                                          boxserial=boxserial)
        r = requests.get(boxscannedurl, headers=self.headers)

        ConsumerApiWrapper.process_status(r.status_code)

        response = r.json()
        return response