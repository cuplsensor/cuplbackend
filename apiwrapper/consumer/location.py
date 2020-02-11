import requests
from . import ConsumerApiWrapper, Exception401


class NoScanOnBoxException(Exception401):
    def __init__(self):
        super().__init__(message="Not authorised because the user has not scanned the parent box. ")


class LocationWrapper(ConsumerApiWrapper):
    @staticmethod
    def process_status(status_code):
        """ Raise an exception for HTTP error statuses"""
        if status_code == 401:
            raise NoScanOnBoxException
        else:
            ConsumerApiWrapper.process_status(status_code)

    def __init__(self, baseurl, tokenstr):
        super().__init__(baseurl, tokenstr)
        self.locationsurl = "{apiurl}/locations".format(apiurl=self.apiurl)

    def get(self, location_id):
        r = requests.get("{locationsurl}/{id}".format(locationsurl=self.locationsurl, id=location_id),
                         headers=self.headers)

        LocationWrapper.process_status(r.status_code)
        response = r.json()
        return response

    def delete(self, location_id):
        r = requests.delete("{locationsurl}/{id}".format(locationsurl=self.locationsurl, id=location_id),
                            headers=self.headers)

        LocationWrapper.process_status(r.status_code)
        return r.status_code

    def get_list(self, boxserial, starttime=None, endtime=None):
        queryparams = {'boxserial': boxserial}

        if starttime is not None:
            queryparams['starttime'] = starttime

        if endtime is not None:
            queryparams['endtime'] = endtime

        r = requests.get(self.locationsurl, params=queryparams, headers=self.headers)
        LocationWrapper.process_status(r.status_code)
        response = r.json()
        return response

    def post(self, capturesample_id, description):
        payload = {'capturesample_id': capturesample_id,
                   'description': description}
        r = requests.post(self.locationsurl, json=payload, headers=self.headers)
        LocationWrapper.process_status(r.status_code)
        response = r.json()
        return response

    def patch(self, location_id, description):
        payload = {'description': description}
        r = requests.patch("{locationsurl}/{id}".format(locationsurl=self.locationsurl, id=location_id),
                           json=payload,
                           headers=self.headers)
        LocationWrapper.process_status(r.status_code)
        response = r.json()
        return response

