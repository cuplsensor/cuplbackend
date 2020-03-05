.. sectnum::

Environment Variables
======================

wsbackend URL
-----------------------

``WSB_PROTOCOL``
^^^^^^^^^^^^^^^^^
Default: ``http://``

Protocol of wsbackend.

.. _wsbhost:

``WSB_HOST``
^^^^^^^^^^^^^
Default: ``localhost``

Hostname of wsbackend.

.. _wsbport:

``WSB_PORT``
^^^^^^^^^^^^^
Default: ``5000``

Port of wsbackend.

Identity Provider URL
-----------------------

.. _idpurl:

``IDP_PROTOCOL``
^^^^^^^^^^^^^^^^
Default: ``http://``

Protocol of the OpenID Connect Identity Provider.

Defaults to the protocol of the mock IdP.

``IDP_HOST``
^^^^^^^^^^^^^^^^
Default: ``localhost``

Hostname of the OpenID Connect Identity Provider.

``IDP_PORT``
^^^^^^^^^^^^^^^^
Default: ``3000``

Port of the OpenID Connect Identity Provider.

.. _idp_jwks:

``IDP_JWKS``
^^^^^^^^^^^^^^
Default: ``/jwks``

Endpoint on the IdP from which the public JSON Web Key set can be downloaded.

Defaults to the `mock IdP JWKs endpoint <https://www.npmjs.com/package/oauth2-mock-server#get-jwks>`_.

Database URI
---------------

.. _dbhost:

``DB_HOST``
^^^^^^^^^^^^^
Default: ``localhost``

Host where the database is running.

.. _dbport:

``DB_PORT``
^^^^^^^^^^^^^
Default: ``5432``

Port number to connect to the database.

.. _dbuser:

``DB_USER``
^^^^^^^^^^^^
Default: ``postgres``

Database user name.

.. _dbpass:

``DB_PASS``
^^^^^^^^^^^^^
Database password.

No default for security reasons. This variable must be set before runtime.

Consumer API
-------------
.. _apiaudience:

``API_AUDIENCE``
^^^^^^^^^^^^^^^^^^
Default: ``mock_api_audience``

Access tokens signed by the IdP must contain this audience claim. Without it, the consumer API
will reject the token and deny access to an endpoint that requires authorization.

Defaults to a value used by the mock IdP.

Admin API
----------

.. _adminapiaudience:

``ADMINAPI_AUDIENCE``
^^^^^^^^^^^^^^^^^^^^^^^
Default: ``default_adminapi_audience``

Access tokens issued using the client credentials flow will contain this audience claim.

``ADMINAPI_CLIENTID``
^^^^^^^^^^^^^^^^^^^^^^^
Default: ``default_adminapi_clientid``

A token request using the `client credentials flow <https://www.oauth.com/oauth2-servers/access-tokens/client-credentials/>`_
must contain this ``client_id``. This is a shared secret between the sender and ``wsbackend``.

``ADMINAPI_CLIENTSECRET``
^^^^^^^^^^^^^^^^^^^^^^^^^^^
A token request using the client credentials flow must contain this ``client_secret``.
This is a shared secret between the sender and ``wsbackend``.

No default for security reasons. This variable must be set before runtime.

