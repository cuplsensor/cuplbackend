from functools import wraps
from ..tokenauth import TokenAuthSymmetric
from ...config import ADMINAPI_CLIENTID, ADMINAPI_CLIENTSERET, ADMINAPI_AUDIENCE


admintokenauth = TokenAuthSymmetric(issuer=ADMINAPI_CLIENTID,
                                    audience=ADMINAPI_AUDIENCE,
                                    secret=ADMINAPI_CLIENTSERET)


def requires_admin_token(f):
    """Determines if the access token is valid
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        admintokenauth.get_decoded_token()
        return f(*args, **kwargs)

    return decorated
