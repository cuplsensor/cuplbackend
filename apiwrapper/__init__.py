from .config import baseurl


class ApiWrapper:
    def auth_header(self, tokenstr):
        headers = {
        'content-type': 'application/json',
        'Authorization': 'bearer {tokenstr}'.format(tokenstr=tokenstr)
        }
        return headers

    def __init__(self):
        self.consumerapiurl = "{baseurl}/api/consumer/v1".format(baseurl=baseurl)
        self.adminapiurl = "{baseurl}/api/admin/v1".format(baseurl=baseurl)
