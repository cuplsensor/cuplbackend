Develop Locally
=====================
wsbackend has external dependencies such as a database and an identity provider.
It is designed to be deployed to a cloud provider. Nonetheless it is easy to test
this application locally without an internet connection.


Add / Edit an API endpoint
------------------------------------

Update Specification
^^^^^^^^^^^^^^^^^^^^^^^
The API specification should be updated first. These are contained in files named ``api.yaml``,
which conform to the Swagger OpenAPI standard. It is sometimes easier to edit these files
by copying them into and out of the Swagger web application.

Write a Test that Fails
^^^^^^^^^^^^^^^^^^^^^^^^

.. _Tavern: https://taverntesting.github.io/

Tavern_ is used for API testing. Simple tests are defined
within yaml files that reside in the tests directory.

The script conftest.py contains pytest fixtures.
These obtain access tokens or read environment variables on behalf of test scripts.

Executing ``py.test`` will run all tests against a live wsbackend server. Its address is set
by environment variables:

* WSB_PROTOCOL
* WSB_HOST
* WSB_PORT

The newly developed application must be
installed and made to serve pages at this address first! To automate this process I have created a
Docker Compose file ``docker-compose.test.yml`` for quickly running tests locally.

First build all images with::

    docker-compose build -f docker-compose.test.yml

This will take a few minutes the first time, but afterwards the docker layers will be cached so it
should copy your new files in within seconds.

Next run tests with::

    docker-compose up -f docker-compose.test.yml


Implement feature. Test until success
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Push to GitHub. Tests will run nodejs.yml. A docker image is tested and built on every pull request.
Readthedocs will execute on webookhook. If tagging the build then package is deployed to pypi.
Build docker image.

Write a Frontend Application
-----------------------------
When writing frontend applications you may want to deploy wsbackend locally. To do this I have
created ``docker-compose.yml``.