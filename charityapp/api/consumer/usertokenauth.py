import os
from functools import wraps
from jose import jwt
from ..tokenauth import TokenAuthAsymmetric
from flask_restful import abort
from traceback import format_exc
from requests import post
import json


baseurl = os.environ["BASE_URL"]
auth0url = os.environ["AUTH0_URL"]

jwksurl = 'https://{auth0url}/.well-known/jwks.json'.format(auth0url=auth0url)
audience = 'https://api.{baseurl}'.format(baseurl=baseurl)
issuer = 'https://{auth0url}/'.format(auth0url=auth0url)

usertokenauth = TokenAuthAsymmetric(issuer=issuer,
                                     audience=audience,
                                     jwksurl=jwksurl)

def get_userinfo(access_token):
    json_header = {'content-type': 'application/json'}
    userinfo_url = 'https://{auth0url}/userinfo'.format(auth0url=auth0url)

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