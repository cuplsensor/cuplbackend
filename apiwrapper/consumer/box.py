import requests
from . import ConsumerApiWrapper


class BoxWrapper(ConsumerApiWrapper):
    def __init__(self, baseurl):
        super().__init__(baseurl)

    def get(self, boxserial):
        boxurl = "{apiurl}/box/{boxserial}".format(apiurl=self.apiurl,
                                                   boxserial=boxserial)
        r = requests.get(boxurl)

        ConsumerApiWrapper.process_status(r.status_code)

        response = r.json()
        return response
