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

"""
    backendapp.api.tokenauth
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Access to some API resources is controlled via token-based authentication.

    https://www.okta.com/uk/identity-101/what-is-token-based-authentication/

    For the Admin API, nearly all resources require an admintoken. This can only be obtained with knowledge of a secret key.
    It is read from an environment variable known only to a system administrator.

    For the Consumer API, some resources require a tagtoken. These prove that an end-user has recently
    captured a tag and therefore has physical access to a device.
"""

from flask import request
from jose import jwt
from flask_restful import abort
from typing import Union
import traceback


def get_token_auth_header() -> str:
    """
    Obtains an access token from the Authorization HTTP Header.

    The value of the authorization header must be in the format: Bearer <token> where token is a JSON Web Token.

    https://swagger.io/docs/specification/authentication/bearer-authentication/
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


class TokenAuth:
    """
    Token authenticator base class.
    """
    def __init__(self, issuer: str, audience: str):
        """
        Instantiate a token authenticator. A JSON Web Token includes a header, a payload and a signature. For more
        information see https://jwt.io/.

        A token is rejected if the payload does not include a set of claims. Each is a key-value pair.

        Specify the expected values of two standard claims: issuer and audience.

        https://en.wikipedia.org/wiki/JSON_Web_Token#Standard_fields

        :param issuer: Identifies the principal that issued the token (this application).
        :param audience: Identifies the audience that the token is intended for.
        """
        self.issuer = issuer
        self.audience = audience

    def verify_token(self, token: str, key: Union[str, dict]) -> dict:
        """
        Decode a JSON Web Token and verify its signature with a key. Confirm that the received token
        has expected values for the audience and issuer claims in its payload.

        If verification fails, :py:func:`abort` is called. This raises an HTTP Exception with
        the 401 unauthorized status.

        :param token: The JSON Web Token.
        :param key: Either an individual JSON Web Key or a JWK set.
        :return: The decoded JSON Web Token.
        """
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
    """
    An authenticator for tokens with signatures that are encrypted and decrypted with the same key.
    """
    def __init__(self, issuer: str, audience: str, secret: str):
        """
        Instantiate an authenticator for tokens with symmetrically encrypted signatures. Verification fails
        when the signature is not decrypted with the same secret key used for encryption.

        :param issuer: The principal that issued the token (this application).
        :param audience: The audience that the token is intended for.
        :param secret: Used to generate and verify the token signature. Must not be shared outside this application.
        """
        super().__init__(issuer, audience)
        self.secret = secret
        self.algorithms = ["HS256"]

    def get_decoded_token(self) -> dict:
        """
        Obtain a JSON Web Token from the authorization HTTP header and verify that it was issued by this
        application, using a secret known only to this application.

        :return: The decoded token.
        """
        unverified_token = get_token_auth_header()
        return self.verify_token(token=unverified_token, key=self.secret)
