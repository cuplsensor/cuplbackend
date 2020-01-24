import os
from functools import wraps
from ..tokenauth import TokenAuthSymmetric


admin_clientid = os.environ["ADMINAPI_CLIENTID"]
admin_clientsecret = os.environ["ADMINAPI_CLIENTSECRET"]
baseurl = os.environ["BASE_URL"]

audience = '{baseurl}'.format(baseurl=baseurl)

admintokenauth = TokenAuthSymmetric(issuer=admin_clientid,
                                    audience=audience,
                                    secret=admin_clientsecret)

def requires_admin_token(f):
    """Determines if the access token is valid
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        admintokenauth.get_decoded_token()
        return f(*args, **kwargs)

    return decorated
