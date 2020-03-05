import requests
from . import ConsumerApiWrapper


class BoxViewWrapper(ConsumerApiWrapper):
    def __init__(self, baseurl, tokenstr):
        super().__init__(baseurl, tokenstr)
        self.boxviewsurl = "{apiurl}/me/boxviews".format(apiurl=self.apiurl)

    def get(self, distinct=False):
        queryparams = None

        if distinct is True:
            queryparams = {'distinctonbox': 'true'}

        try:
            r = requests.get(self.boxviewsurl, params=queryparams, headers=self.headers)
            boxviewresponse = r.json()
        except requests.exceptions.RequestException as e:
            BoxViewWrapper.process_status(e.response.status_code, str(e))

        return boxviewresponse

    def post(self, boxserial):
        payload = {'boxserial': boxserial}
        try:
            r = requests.post(self.boxviewsurl, json=payload, headers=self.headers)
            boxviewresponse = r.json()
        except requests.exceptions.RequestException as e:
            BoxViewWrapper.process_status(e.response.status_code, str(e))

        return boxviewresponse

