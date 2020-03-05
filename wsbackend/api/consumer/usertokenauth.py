from functools import wraps
from jose import jwt
from ..tokenauth import TokenAuthAsymmetric
from ...config import API_AUDIENCE, IDP_ORIGIN, IDP_JWKS
from flask_restful import abort
from traceback import format_exc
from requests import get
import json

jwksurl = '{idp_origin}{idp_jwks}'.format(idp_origin=IDP_ORIGIN, idp_jwks=IDP_JWKS)

usertokenauth = TokenAuthAsymmetric(issuer=IDP_ORIGIN,
                                     audience=API_AUDIENCE,
                                     jwksurl=jwksurl)


def get_userinfo(access_token):
    json_header = {'Authorization': 'Bearer {access_token}'.format(access_token=access_token)}
    userinfo_url = '{idp_origin}/userinfo'.format(idp_origin=IDP_ORIGIN)

    # Obtain userinfo from Auth0 with the access token
    userinfo_response = get(userinfo_url, headers=json_header).json()

    return userinfo_response

def requires_user_token(f):
    """Determines if the access token is valid
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            usertoken = usertokenauth.get_decoded_token()
        except jwt.JWTError as e:
            abort(401, description=format_exc(limit=1, chain=False))
        return f(usertoken, *args, **kwargs)

    return decorated