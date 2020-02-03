.. sectnum::

Authorization
=======================

Some API endpoints require authorization. Only users with a third party account
(e.g. Google or Facebook) are granted access. Such accounts
cannot be set up without some human interaction. The requirement
for user authentication guards against bots filling the wsbackend database with rubbish.

The websensor Web Application
uses the `Open ID Connect <https://auth0.com/docs/protocols/oidc>`_ (OIDC) protocol to communicate
with a third-party identity provider (IdP). When a user authenticates, the IdP produces
an `access token <https://www.oauth.com/oauth2-servers/access-tokens/>`_. This token is
unique to a user and decodes to a number of claims. These include:

    * User name.
    * Audience (URL of the websensor API for which access has been granted).
    * Issuer (URL of the identity provider).
    * Issued timestamp.
    * Expiry timestamp.
    * Scope (granular API permissions).

Tokens are not encrypted. They **must** always be transmitted through a
secure channel (HTTPS). The value of tokens is they include a `digital signature <https://en.wikipedia.org/wiki/Digital_signature>`_.
If signature verification is successful then the claims can be trusted. In this way access
tokens are used to access protected API resources.

The access token also grants the Web Application permission to read some **personal data** about
a user (e.g. name and profile picture). Crucially these data are not stored in the Web Application itself.
They are requested by making an
API call to ``/userinfo`` API endpoint of the IdP. It can be assumed that the IdP handles these data
in a secure and GDPR compliant way.

Production
-------------
In a production environment, the IdP is `Auth0.com <https://auth0.com>`_. Others can be used
if they adhere to the OIDC protocol.

Auth0.com acts as an intermediary. It allows users to authenticate with a large
number of OAuth2 providers such as Google, GitHub and Facebook.

Obtain an API Access Token
^^^^^^^^^^^^^^^^^^^^^^^^^^^
wsfrontend :ref:`obtains <wsfrontend:Authorization-Grant-Flow>` an access token fom the identify provider using the `Authorization Code Grant Flow <https://auth0.com/docs/api-auth/tutorials/authorization-code-grant>`_.

Protected API Resource Called
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
wsfrontend calls wsbackend endpoints with the access token::

    curl -X GET "https://websensor.io/api/consumer/v1/me" -H "accept: application/json" -H "Authorization: Bearer eyJhbGciOiJS... ZOA4t7Q"

Access Token Validated
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The access token signature is generated asymetrically (RS-256).
A private key (on Auth0.com) generates the signature. A public key
(hosted by Auth0.com) is used for validation.

wsbackend downloads the ``public_key`` (JWKs) from Auth0.com::

    GET {AUTH0_URL}/.well-known/jwks.json

Signature verification and decoding are performed using `PyJWT <https://pyjwt.readthedocs.io/en/latest/>`_::

    decoded = jwt.decode(
                token,
                public_key,
                algorithms=self.algorithms,
                audience={API_AUDIENCE},
                issuer={AUTH0_URL}
                )

An exception is raised if validation fails. The token is rejected, authorization fails and the API
responds with an error ``403: Forbidden``.

Protected Resource Content are Served
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If validation succeeeds, wsbackend transmits a ``200 OK`` response to the wsfrontend, along with the requested resource data.

Testing
--------
For test, the OIDC provider is substituted with a mock https://www.npmjs.com/package/oauth2-mock-server
Access tokens are obtained from this using the client-creditials OAuth2 flow. Userinfo can also be mocked up.
Access tokens are verified by downloading the JSON Web Key set from the mock OIDC provider.