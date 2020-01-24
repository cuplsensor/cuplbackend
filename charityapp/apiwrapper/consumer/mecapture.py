import requests
from . import ConsumerApiWrapper


class MeCaptureWrapper(ConsumerApiWrapper):
    def __init__(self, tokenstr):
        super().__init__(tokenstr)

    def get(self, distinct=False):
        capturesurl = "{consumerapiurl}/me/captures".format(consumerapiurl=self.consumerapiurl)
        queryparams = None

        if distinct is True:
            queryparams = {'distinctonbox': 'true'}

        r = requests.get(capturesurl, params=queryparams, headers=self.headers)
        ConsumerApiWrapper.process_status(r.status_code)
        captresponse = r.json()
        return captresponse

    def post(self, circbufb64, serial, statusb64, timeintb64, versionStr):
        capturesurl = "{consumerapiurl}/me/captures".format(consumerapiurl=self.consumerapiurl)
        payload = {'circbufb64': circbufb64,
                   'serial': serial,
                   'statusb64': statusb64,
                   'timeintb64': timeintb64,
                   'versionStr': versionStr}

        r = requests.get(capturesurl, json=payload, headers=self.headers)
        ConsumerApiWrapper.process_status(r.status_code)
        captresponse = r.json()
        return captresponse
