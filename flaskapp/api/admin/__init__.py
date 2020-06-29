# -*- coding: utf-8 -*-
"""
    flaskapp.api
    ~~~~~~~

    web api application package
"""

from functools import wraps
from flasgger import Swagger
from ... import factory

from .token import bp as tokenbp
from .tags import bp as tagsbp
from .captures import bp as capturesbp
from .users import bp as usersbp
from .tagviews import bp as tagviewsbp

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
    "https"
  ],
  "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header"
        }
  },
  "operationId": "getmyData",
  "definitions": {
                    "Capture": {
                        "title": "Capture",
                        "type": "object",
                        "properties": {
                            "id": {
                                "type": "integer",
                                "format": "int32",
                                "description": "ID of the capture"
                            },
                            "tag_id": {
                                "description": "ID of the tag from which the capture was taken",
                                "format": "int32",
                                "type": "integer",
                                "example": 1141
                            },
                            "timestamp": {
                                "description": "Time the capture was taken",
                                "format": "date-time",
                                "type": "string",
                                "example": "2019-01-13T15:08:35+00:00"
                            },
                            "loopcount": {
                                "description": "Number of times the cursor inside the circular buffer "
                                               "has wrapped from beginning to end.",
                                "example": 20,
                                "type": "integer",
                                "format": "int32"
                            },
                            "batvoltagemv": {
                                "description": "Battery voltage in mV",
                                "example": 3000,
                                "type": "integer",
                                "format": "int32"
                            },
                            "cursorpos": {
                                "description": "Cursor position in the circular buffer",
                                "format": "int32",
                                "type": "integer",
                                "example": 10
                            },
                            "version": {
                                "description": "Version parameter for the capture",
                                "format": "int32",
                                "type": "integer",
                                "example": 1
                            },
                            "timeintmins": {
                                "description": "Time interval between samples in minutes",
                                "example": 12,
                                "type": "integer"
                            },
                            "md5": {
                                "description": "MD5 or HMAC hash of the samples",
                                "example": "aseknagleksnoe",
                                "type": "string"
                            },
                            "status": {
                                "$ref": "#/definitions/CaptureStatus"
                            },
                            "samples": {
                                "type": "array",
                                "items": {
                                    "$ref": "#/definitions/CaptureSample"
                                }
                            }
                        },
                    },
                    "CaptureStatus": {
                        "title": "CaptureStatus",
                        "type": "object",
                        "properties": {
                            "resetsalltime": {
                                "description": "Resets all time divided by 8",
                                "example": 120,
                                "type": "integer",
                                "format": "int32"
                            },
                            "brownout": {
                                "description": "True if the brownout reset bit is set.",
                                "example": "false",
                                "type": "boolean",
                                "default": "false"
                            },
                            "supervisor": {
                                "description": "True if the SVSH (supply voltage supervisor) reset bit is set.",
                                "example": "false",
                                "type": "boolean",
                                "default": "false"
                            },
                            "watchdog": {
                                "description": "True if the brownout reset bit is set.",
                                "example": "false",
                                "type": "boolean",
                                "default": "false"
                            },
                            "misc": {
                                "description": "True if the miscellaneous reset bit is set.",
                                "example": "false",
                                "type": "boolean",
                                "default": "false"
                            },
                            "lpm5wakeup": {
                                "description": "True if the LPMx.5 wakeup bit is set.",
                                "example": "false",
                                "type": "boolean",
                                "default": "false"
                            },
                            "clockfail": {
                                "description": "True if the clock failure bit is set.",
                                "example": "false",
                                "type": "boolean",
                                "default": "false"
                            },
                        },
                    },
                    "CaptureSample": {
                        "title": "CaptureSample",
                        "type": "object",
                        "properties": {
                            "id": {
                                "description": "CaptureSample ID",
                                "example": 1,
                                "type": "integer",
                                "format": "int32"
                            },
                            "capture_id": {
                                "description": "ID of the parent Capture object",
                                "example": 1,
                                "type": "integer",
                                "format": "int32"
                            },
                            "timestamp": {
                                "description": "Timestamp for the sample",
                                "example": "2019-01-13T15:08:35+00:00",
                                "type": "string",
                                "format": "date-time"
                            },
                            "temp": {
                                "description": "Temperature in degrees Celsius",
                                "example": 21,
                                "type": "number",
                                "format": "double"
                            },
                            "rh": {
                                "description": "Relative Humidity in percent",
                                "example": 55,
                                "type": "number",
                                "format": "double"
                            },
                            "location": {
                                "$ref": "#/definitions/Location"
                            }
                        },
                        "required": [
                            "id",
                            "capture_id",
                            "timestamp",
                            "temp"
                        ]
                    },
                    "Location": {
                            "title": "Location",
                            "type": "object",
                            "properties": {
                                "id": {
                                    "description": "Location ID",
                                    "example": 1,
                                    "type": "integer",
                                    "format": "int32"
                                },
                                "capturesample_id": {
                                    "description": "ID of the parent CaptureSample object",
                                    "example": 1,
                                    "type": "integer",
                                    "format": "int32"
                                },
                                "timestamp": {
                                    "description": "Time the location was added",
                                    "example": "2019-01-13T15:08:35+00:00",
                                    "type": "string",
                                    "format": "date-time"
                                },
                                "description": {
                                    "description": "Description of where a tag was located at the time of a capturesample.",
                                    "example": "Cupboard under the stairs",
                                    "type": "string"
                                }
                            }
                    },
  }



}


def create_app(settings_override=None):
    """Returns the Web API application instance"""
    app = factory.create_api_app(__name__, __path__, settings_override)
    app.register_blueprint(tokenbp)
    app.register_blueprint(tagsbp)
    app.register_blueprint(capturesbp)
    app.register_blueprint(tagviewsbp)
    app.register_blueprint(usersbp)
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
