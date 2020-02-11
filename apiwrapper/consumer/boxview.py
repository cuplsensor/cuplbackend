import requests
from . import ConsumerApiWrapper


class BoxViewWrapper(ConsumerApiWrapper):
    def __init__(self, tokenstr):
        super().__init__(tokenstr)
        self.boxviewsurl = "{consumerapiurl}/me/boxviews".format(consumerapiurl=self.consumerapiurl)

    def get(self, distinct=False):
        queryparams = None

        if distinct is True:
            queryparams = {'distinctonbox': 'true'}

        r = requests.get(self.boxviewsurl, params=queryparams, headers=self.headers)

        ConsumerApiWrapper.process_status(r.status_code)

        boxviewresponse = r.json()
        return boxviewresponse

    def post(self, boxserial):
        payload = {'boxserial': boxserial}
        r = requests.post(self.boxviewsurl, json=payload, headers=self.headers)

        ConsumerApiWrapper.process_status(r.status_code)

        boxviewresponse = r.json()
        return boxviewresponse

