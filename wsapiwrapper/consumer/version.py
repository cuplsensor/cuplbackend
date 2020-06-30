import requests
from . import ConsumerApiWrapper


class Version(ConsumerApiWrapper):
    def get(self) -> dict:
        versionurl = "{apiurl}/version".format(apiurl=self.apiurl)
        r = requests.get(versionurl)
        r.raise_for_status()
        return r.json()