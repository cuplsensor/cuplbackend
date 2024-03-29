# cuplbackend
This is a [WSGI](https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface) web application. It wraps a REST API around [cuplcodec](https://github.com/cuplsensor/cuplcodec). 
Environmental sensor samples decoded by the latter are persisted in a [postgres](https://www.postgresql.org/) database using the [SQLAlchemy](https://www.sqlalchemy.org/) ORM.

![cuplbackend screenshot](cuplbackend_screenshot.png)

## Tests

![GitHub Workflow Status](https://img.shields.io/github/workflow/status/cuplsensor/cuplbackend/Install%20cuplbackend%20and%20run%20tests.)

API endpoints are tested with [pytest](https://docs.pytest.org/en/stable/) with [Tavern](https://tavern.readthedocs.io/en/latest/). 

## Documentation 

Hosted on [ReadTheDocs](https://cupl.readthedocs.io/projects/backend/en/latest/). This includes information on how to install the software from scratch without Docker. Work is in progress on the documentation for cuplbackend. For now, refer to [cupldeploy](https://github.com/cuplsensor/cupldeploy) for more information.

## Docker Image

Hosted on [GitHub Packages](https://github.com/cuplsensor/cuplbackend/pkgs/container/cuplbackend). Pull the image with: 
         
    docker pull ghcr.io/cuplsensor/cuplbackend:master
    
## Licence

### cuplbackend

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

### Documentation

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
