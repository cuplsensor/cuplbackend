import requests
from ..admin import AdminApiWrapper
from enum import Enum
import json

class TagFormat(Enum):
    FORMAT_HDC2021_TRH = 1
    FORMAT_HDC2021_TEMPONLY = 2

class TagWrapper(AdminApiWrapper):
    """Wraps calls to tag endpoints on the Admin API.
    """

    def __init__(self, baseurl: str, adminapi_token: str):
        """Constructor for TagWrapper

        Args:
            baseurl (str): Websensor backend URL.
            adminapi_token (str): Token for accessing the admin API.
            endpoint_one (str): Endpoint for returning one resource instance.
            endpoint_many (str): Endpoint for returning a list of resource instances.
        """
        endpoint_one = "/tag/"
        endpoint_many = "/tags"
        super().__init__(baseurl, adminapi_token, endpoint_one, endpoint_many)

    def simulate(self,
                 tagid: int,
                 frontendurl: str,
                 nsamples: int = 100,
                 smplintervalmins: int = 100,
                 tagformat: TagFormat = TagFormat.FORMAT_HDC2021_TRH,
                 usehmac: bool = False,
                 batvoltagemv: int = 3000,
                 bor: bool = False,
                 svsh: bool = False,
                 wdt: bool = False,
                 misc: bool = False,
                 lpm5wu: bool = False,
                 clockfail: bool = False,
                 tagerror: bool = False
                 ) -> str:
        """Make a GET request to the :ref:`TagAdminAPI` simulate endpoint.

        Args:
            tagid: Database ID of the tag to simulate.
            frontendurl: URL of a cuplfrontend instance that will be contained in the simulated tag URL.
            nsamples: Number of samples to put in the simulated tag URL.
            smplintervalmins: Time interval between samples in minutes.
            tagformat: Indicates the datatype for each sample.
            usehmac: Specifies whether the hash is HMAC-MD5 or just MD5.
            batvoltagemv: Battery voltage of the simulated tag in mV.
            bor: Brown-out-Reset flag.
            svsh: Supply Voltage Supervisor (high-side) reset flag.
            wdt: Watchdog reset flag.
            misc: Miscellaneous reset flag.
            lpm5wu: Low power mode wake-up flag.
            clockfail: Clock failure reset flag.
            tagerror: Specify a tag error URL where the circular buffer is omitted.

        Returns:
            str: A string containing a simulated tag URL
        """

        tagurl = "{apiurl}/tag/{tagid}/simulate".format(apiurl=self.apiurl, tagid=tagid)
        params = {'frontendurl': frontendurl,
                  'nsamples': nsamples,
                  'smplintervalmins': smplintervalmins,
                  'format': tagformat.value,
                  'usehmac': usehmac,
                  'batvoltagemv': batvoltagemv,
                  'bor': bor,
                  'svsh': svsh,
                  'wdt': wdt,
                  'misc': misc,
                  'lpm5wu': lpm5wu,
                  'clockfail': clockfail,
                  'tagerror': tagerror
                  }
        r = requests.get(tagurl, params=params, headers=self.headers)
        r.raise_for_status()
        tagresponse = r.json()
        return tagresponse

    def post(self, serial: str = None,
                secretkey: str = None,
                fwversion: str = None,
                hwversion: str = None,
                description: str = None) -> dict:
        """
        Make a POST request to the :ref:`TagAdminAPI` endpoint.

        :param serial: Tag serial string (8 characters).
        :param secretkey: Secret key (16 characters).
        :param fwversion: Tag firmware version.
        :param hwversion: Tag hardware version.
        :param description: Tag description.
        :return:
            dict: A dictionary representing the new tag object.
        """
        tagsurl = "{apiurl}/tags".format(apiurl=self.apiurl)

        payload = dict()

        if serial is not None:
            payload.update({'serial': serial})

        if secretkey is not None:
            payload.update({'secretkey': secretkey})

        if fwversion is not None:
            payload.update({'fwversion': fwversion})

        if hwversion is not None:
            payload.update({'hwversion': hwversion})

        if description is not None:
            payload.update({'description': description})

        r = requests.post(tagsurl, json=payload, headers=self.headers)
        r.raise_for_status()
        tagresponse = r.json()
        return tagresponse


