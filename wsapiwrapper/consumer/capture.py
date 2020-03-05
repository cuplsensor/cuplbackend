import requests
from . import ConsumerApiWrapper


class CaptureWrapper(ConsumerApiWrapper):
    def __init__(self, baseurl):
        super().__init__(baseurl)

    def get_list(self, serial, offset=0, limit=None):
        capturesurl = "{apiurl}/captures".format(apiurl=self.apiurl)
        queryparams = {'serial': serial,
                       'offset': offset,
                       'limit': limit}

        r = requests.get(capturesurl, params=queryparams)
        ConsumerApiWrapper.process_status(r.status_code)
        captresponse = r.json()
        return captresponse

    def get(self, capture_id):
        capturesurl = "{apiurl}/captures/{capture_id}".format(apiurl=self.apiurl,
                                                              capture_id=capture_id)

        r = requests.get(capturesurl)
        ConsumerApiWrapper.process_status(r.status_code)
        captresponse = r.json()
        return captresponse

    def get_samples(self, capture_id, offset=0, limit=None):
        capturesamplesurl = "{apiurl}/captures/{capture_id}/samples".format(apiurl=self.apiurl,
                                                                            capture_id=capture_id)

        queryparams = {'offset': offset,
                       'limit': limit}

        r = requests.get(capturesamplesurl, params=queryparams)
        ConsumerApiWrapper.process_status(r.status_code)
        response = r.json()
        return response

    def post(self, circbufb64, serial, statusb64, timeintb64, versionStr):
        capturesurl = "{apiurl}/captures".format(apiurl=self.apiurl)
        payload = {'circbufb64': circbufb64,
                   'serial': serial,
                   'statusb64': statusb64,
                   'timeintb64': timeintb64,
                   'ver': versionStr}

        r = requests.post(capturesurl, json=payload)
        ConsumerApiWrapper.process_status(r.status_code)
        captresponse = r.json()
        return captresponse
