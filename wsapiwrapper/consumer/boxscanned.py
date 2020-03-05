import requests
from . import ConsumerApiWrapper


class BoxScannedWrapper(ConsumerApiWrapper):
    def __init__(self, baseurl, tokenstr):
        super().__init__(baseurl, tokenstr)

    def get(self, boxserial):
        boxscannedurl = "{apiurl}/box/{boxserial}/scanned".format(apiurl=self.apiurl,
                                                                  boxserial=boxserial)
        r = requests.get(boxscannedurl, headers=self.headers)

        ConsumerApiWrapper.process_status(r.status_code)

        response = r.json()
        return response