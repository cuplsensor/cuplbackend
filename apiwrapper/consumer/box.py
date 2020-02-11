import requests
from . import ConsumerApiWrapper


class BoxWrapper(ConsumerApiWrapper):
    def __init__(self):
        super().__init__()

    def get(self, boxserial):
        boxurl = "{consumerapiurl}/box/{boxserial}".format(consumerapiurl=self.consumerapiurl,
                                                           boxserial=boxserial)
        r = requests.get(boxurl)

        ConsumerApiWrapper.process_status(r.status_code)

        response = r.json()
        return response
