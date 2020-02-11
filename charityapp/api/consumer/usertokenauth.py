from functools import wraps
from jose import jwt
from ..tokenauth import TokenAuthAsymmetric
from ...config import API_AUDIENCE, AUTH0_URL, JWKS_ENDPOINT
from flask_restful import abort
from traceback import format_exc
from requests import post
import json

jwksurl = '{auth0_url}{jwks_endpoint}'.format(auth0_url=AUTH0_URL, jwks_endpoint=JWKS_ENDPOINT)

usertokenauth = TokenAuthAsymmetric(issuer=AUTH0_URL,
                                     audience=API_AUDIENCE,
                                     jwksurl=jwksurl)

def get_userinfo(access_token):
    json_header = {'content-type': 'application/json'}
    userinfo_url = '{auth0url}/userinfo'.format(auth0url=AUTH0_URL)

    userinfo_params = {
        'access_token': access_token
    }

    # Obtain userinfo from Auth0 with the access token
    userinfo_response = post(userinfo_url,
                             data=json.dumps(userinfo_params),
                             headers=json_header).json()

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