from functools import wraps
from ..tokenauth import TokenAuthSymmetric
from ...config import TAGTOKEN_CLIENTID, TAGTOKEN_CLIENTSECRET


def requires_tagtoken(f):
    """Determines if the tag token is valid
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        tagtokenauth = TokenAuthSymmetric(issuer=TAGTOKEN_CLIENTID,
                                          audience=kwargs['serial'],
                                          secret=TAGTOKEN_CLIENTSECRET)
        tagtokenauth.get_decoded_token()
        return f(*args, **kwargs)

    return decorated
