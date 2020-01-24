import os


class ApiWrapper:
    def auth_header(self, tokenstr):
        headers = {
        'content-type': 'application/json',
        'Authorization': 'bearer {tokenstr}'.format(tokenstr=tokenstr)
        }
        return headers

    def __init__(self):
        baseurlenv = os.environ["BASE_URL"]
        self.baseurl = "https://{baseurlenv}".format(baseurlenv=baseurlenv)
        self.consumerapiurl = "{baseurl}/api/consumer/v1".format(baseurl=self.baseurl)
        self.adminapiurl = "{baseurl}/api/admin/v1".format(baseurl=self.baseurl)
