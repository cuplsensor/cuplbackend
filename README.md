# cuplbackend
This is a [WSGI](https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface) web application. It wraps a REST API around [cuplcodec](https://github.com/cuplsensor/cuplcodec). 
Environmental sensor samples decoded by the latter are persisted in a [postgres](https://www.postgresql.org/) database using the [SQLAlchemy](https://www.sqlalchemy.org/) ORM.

## Tests

![GitHub Workflow Status](https://img.shields.io/github/workflow/status/cuplsensor/cuplbackend/Install%20cuplbackend%20and%20run%20tests.)

API endpoints are tested with [pytest](https://docs.pytest.org/en/stable/) with [Tavern](https://tavern.readthedocs.io/en/latest/). 

Some endpoints require a [JSON Web Token](https://jwt.io/introduction/) (JWT) from an authenticated user. This is normally supplied by a 3rd party [OAuth2 Provider](https://oauth.net/2/) such as [Auth0](https://auth0.com). To enable automatic test, this provider is mocked with [oauth2-mock-server](https://www.npmjs.com/package/oauth2-mock-server), which generates and validates JWTs. 

## Documentation 

[![Documentation Status](https://readthedocs.org/projects/wsbackend/badge/?version=latest)](https://cupl.readthedocs.io/projects/backend/en/latest/?badge=latest) 

Hosted on [ReadTheDocs](https://cupl.readthedocs.io/projects/backend/en/latest/). This includes information on how to install the software from scratch without Docker.

## Docker Image

![Docker Build Status](https://img.shields.io/docker/cloud/build/cupl/backend)

Hosted on [DockerHub](https://hub.docker.com/r/cupl/backend). Pull the image with: 
         
    docker pull cupl/backend
    
## Licence

### cuplbackend

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

If the Affero GPLv3 licence is too restrictive for your needs, a commercial licence can be purchased from Plotsensor Ltd.

### cuplapiwrapper

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) 

### Documentation

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
