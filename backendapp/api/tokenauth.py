#  A web application that stores samples from a collection of NFC sensors.
#
#  https://github.com/cuplsensor/cuplbackend
#
#  Original Author: Malcolm Mackay
#  Email: malcolm@plotsensor.com
#  Website: https://cupl.co.uk
#
#  Copyright (c) 2021. Plotsensor Ltd.
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License
#  as published by the Free Software Foundation, either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the
#  GNU Affero General Public License along with this program.
#  If not, see <https://www.gnu.org/licenses/>.

from flask import request
import json
from jose import jwt
from flask_restful import abort
from urllib.request import urlopen
import traceback

class NoRSAError(Exception):
    pass

class TokenAuth():
    def __init__(self, issuer, audience):
        self.issuer = issuer
        self.audience = audience

    # Format error response and append status code
    def get_token_auth_header(self):
        """Obtains the access token from the Authorization Header
        """
        auth = request.headers.get("Authorization", None)
        if not auth:
            abort(401, description="authorization_header_missing")

        parts = auth.split()

        if parts[0].lower() != "bearer":
            abort(401, description="Authorization header must start with bearer")
        elif len(parts) == 1:
            abort(401, description="Token not found")
        elif len(parts) > 2:
            abort(401, description="Authorization header must be bearer token")

        token = parts[1]
        return token

    def verify_token(self, token, key):
        try:
            decoded = jwt.decode(
                token,
                key,
                algorithms=self.algorithms,
                audience=self.audience,
                issuer=self.issuer
            )
        except jwt.ExpiredSignatureError:
            abort(401, description="token is expired")

        except jwt.JWTClaimsError:
            abort(401, description="incorrect claims please check the audience and issuer")

        except jwt.JWTError:
            abort(401, description="bad token")

        except Exception:
            abort(400, description=traceback.format_exc())

        return {'decoded': decoded, 'token': token}


class TokenAuthSymmetric(TokenAuth):
    def __init__(self, issuer, audience, secret):
        super().__init__(issuer, audience)
        self.secret = secret
        self.algorithms = ["HS256"]

    def get_decoded_token(self):
        unverified_token = self.get_token_auth_header()
        return self.verify_token(token=unverified_token, key=self.secret)


class TokenAuthAsymmetric(TokenAuth):
    def __init__(self, issuer, audience, jwksurl):
        super().__init__(issuer, audience)
        self.jwksurl = jwksurl
        self.algorithms = ["RS256"]

    def get_rsa_key(self, token):
        jwksurlresponse = urlopen(self.jwksurl)
        jwks = json.loads(jwksurlresponse.read())
        unverified_header = jwt.get_unverified_header(token)
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if rsa_key == None:
            raise NoRSAError('No RSA key found')

        return rsa_key

    def get_decoded_token(self):
        unverified_token = self.get_token_auth_header()
        rsa_key = self.get_rsa_key(token=unverified_token)
        return self.verify_token(token=unverified_token, key=rsa_key)
