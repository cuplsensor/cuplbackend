# -*- coding: utf-8 -*-
"""
    charityapp.api
    ~~~~~~~

    web api application package
"""

from functools import wraps
from flasgger import Swagger
from ..core import OverholtError, OverholtFormError
from ..helpers import JSONEncoder
from .. import factory


from .admin.token import bp as tokenbp
from .admin.boxes import bp as boxesbp

swaggertemplate = {
  "swagger": "2.0",
  "info": {
    "title": "Plotsensor admin API",
    "description": "API for my data",
    "contact": {
      "responsibleOrganization": "ME",
      "responsibleDeveloper": "Me",
      "email": "me@me.com",
      "url": "www.me.com",
    },
    "termsOfService": "http://me.com/terms",
    "version": "0.0.1"
  },
  "host": "mysite.com",  # overrides localhost:500
  "basePath": "/api",  # base bash for blueprint registration
  "schemes": [
    "http",
    "https"
  ],
  "operationId": "getmyData"



}


def create_app(settings_override=None):
    """Returns the Web API application instance"""

    app = factory.create_app(__name__, __path__, settings_override)
    app.register_blueprint(tokenbp)
    app.register_blueprint(boxesbp)
    swagger = Swagger(app, template=swaggertemplate)

    return app

def route(bp, *args, **kwargs):
    def decorator(f):
        @bp.route(*args, **kwargs)
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)
        return f

    return decorator
