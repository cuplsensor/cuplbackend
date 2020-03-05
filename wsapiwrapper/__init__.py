class ApiWrapper:
    def auth_header(self, tokenstr):
        headers = {
        'content-type': 'application/json',
        'Authorization': 'bearer {tokenstr}'.format(tokenstr=tokenstr)
        }
        return headers

    def __init__(self, baseurl):
        self.baseurl = baseurl