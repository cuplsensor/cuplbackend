# -*- coding: utf-8 -*-
"""
    charityapp.api
    ~~~~~~~

    web api application package
"""

from functools import wraps
from flasgger import Swagger
from ... import factory
from os import environ

from .users import bp as usersbp
from .boxes import bp as boxesbp
from .captures import bp as capturesbp
from .samples import bp as samplesbp
from .accesstoken import bp as accesstokenbp
from .boxviews import bp as boxviewsbp
from .locations import bp as locationsbp

baseurl = environ["BASE_URL"]

swaggertemplate = {
    "swagger": "2.0",
    "info": {
        "title": "Plotsensor consumer API",
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
    "host": "{baseurl}".format(baseurl=baseurl),  # overrides localhost:500
    "basePath": "/api/consumer/v1",  # base bash for blueprint registration
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header"
        }
    },
    "schemes": [
        "https"
    ],
    "operationId": "getmyData",
    "definitions": {
        "UserInfo": {
            "title": "UserInfo",
            "type": "object",
            "properties": {
                "family_name": {
                    "example": "Bruce",
                    "type": "string"
                },
                "given_name": {
                    "example": "Almighty",
                    "type": "string"
                },
                "name": {
                    "example": "Bruce Almighty",
                    "type": "string"
                },
                "locale": {
                    "example": "en-GB",
                    "type": "string"
                },
                "nickname": {
                    "example": "bruce.almighty",
                    "type": "string"
                },
                "picture": {
                    "example": "https://lh5.googleusercontent.com/--nU_M9gooPA/AAAAAAAAAAI/AAAAAAAAAAA/AKxrwcZvgYJFq7AjYyLe6fih5f20MbPU0Q/mo/photo.jpg",
                    "type": "string"
                },
                "sub": {
                    "example": "google-oauth2|115758583297709853721",
                    "type": "string"
                },
                "updated_at": {
                    "example": "2019-01-06T22:43:33.196Z",
                    "type": "string",
                    "format": "date-time"

                }

            }
        },
        "User": {
            "title": "User",
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "format": "int32"
                },
                "oauth_id": {
                    "type": "string",
                    "format": "uuid"
                },
                "timeregistered": {
                    "example": "2019-01-06T22:43:33.196Z",
                    "type": "date-time",
                    "format": "uuid"
                },
                "userinfo": {
                    "$ref": "#/definitions/UserInfo"
                },
                "roles": {
                    "example": "end-user",
                    "type": "string"
                }
            },
            "required": [
                "oauth_id",
                "email",
                "first_name",
                "last_name",
                "locale",
                "roles"
            ]
        },
        "EncodedCapture": {
            "title": "Base64 Encoded Capture",
            "type": "object",
            "properties": {
                "statusb64": {
                    "description": "12 character status string",
                    "example": "AAAAAAAA",
                    "type": "string",
                    "writeOnly": "true"
                },
                "timeintb64": {
                    "description": "Time interval in minutes in base64",
                    "example": "Awg=",
                    "type": "string",
                    "writeOnly": "true"
                },
                "circbufb64": {
                    "description": "Circular buffer including samples encoded as base64.",
                    "example": "Add example here",
                    "type": "string",
                    "writeOnly": "true"
                },
                "serial": {
                    "description": "Serial of the box that made the capture",
                    "example": "YWJjZGVM",
                    "type": "string"
                },
                "versionStr": {
                    "example": "0001",
                    "type": "string"
                }
            }
        },
        "Capture": {
            "title": "Capture",
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "format": "int32",
                    "readOnly": "true",
                    "example": 232
                },
                "boxserial": {
                    "description": "Serial of the box that made the capture",
                    "example": "YWJjZGVM",
                    "type": "string",
                },
                "timestamp": {
                    "example": "2019-01-15T13:09:52.456Z",
                    "type": "string",
                    "format": "date-time",
                    "readOnly": "true"
                },
                "loopcount": {
                    "example": 2,
                    "type": "integer",
                    "description": "Number of times the circular"
                                   "buffer pointer has wrapped from "
                                   "the end to the beginning",
                    "readOnly": "true"
                },
                "version": {
                    "example": 1,
                    "type": "integer"
                },
                "batvoltagemv": {
                    "example": 3000,
                    "type": "integer",
                    "readOnly": "true"
                },
                "cursorpos": {
                    "example": 20,
                    "type": "integer",
                    "readOnly": "true"
                },
                "timeintmins": {
                    "example": 12,
                    "type": "integer",
                    "readOnly": "true"
                },
                "md5": {
                    "example": "2f324022a223",
                    "type": "string",
                    "readOnly": "true"
                },
                "status": {
                    "$ref": "#/definitions/CaptureStatus"
                }
            }
        },
        "CaptureStatus": {
            "title": "CaptureStatus",
            "type": "object",
            "readOnly": "true",
            "properties": {
                "id": {
                    "description": "CaptureStatus ID",
                    "example": 1,
                    "type": "integer",
                    "format": "int32"
                },
                "parent_capture": {
                    "description": "Parent Capture ID",
                    "example": 232,
                    "type": "integer",
                    "format": "int32"
                },
                "resetsalltime": {
                    "example": 20,
                    "type": "integer"
                },
                "brownout": {
                    "description": "True if the cause of the most recent"
                                   "reset was a brown out condition.",
                    "example": "false",
                    "type": "boolean"
                },
                "clockfail": {
                    "description": "True if the most recent reset "
                                   "was caused by an MCU clock failure.",
                    "example": "false",
                    "type": "boolean"
                },
                "lpm5wakeup": {
                    "description": "True if the MCU has woken up from "
                                   "LPM (Low Power Mode) x.5",
                    "example": "false",
                    "type": "boolean"
                },
                "misc": {
                    "description": "True if a reset has occured for "
                                   "miscellaneous reasons",
                    "example": "false",
                    "type": "boolean"
                },
                "supervisor": {
                    "description": "True if the supply voltage "
                                   "supervisor caused the most "
                                   "recent reset",
                    "example": "false",
                    "type": "boolean"
                },
                "watchdog": {
                    "description": "True if the MCU watchdog "
                                   "caused the most recent reset.",
                    "example": "false",
                    "type": "boolean"
                }

            }
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
                    "description": "Unix timestamp in seconds since January 1st 1970",
                    "example": "2019-01-15T13:09:52.456Z",
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
        "BoxView": {
            "title": "Box View",
            "type": "object",
            "properties": {
                "id": {
                    "description": "Unique ID of the Boxview item",
                    "example": 20,
                    "type": "integer",
                    "readOnly": "true"
                },
                "boxserial": {
                    "description": "Serial of box that was viewed",
                    "example": "YWJjZGVM",
                    "type": "string"
                },
                "timestamp": {
                    "description": "Timestamp the box was viewed in seconds since January 1st 1970",
                    "example": "2019-01-15T13:09:52.456Z",
                    "type": "string",
                    "format": "date-time",
                    "readOnly": "true"
                },
            }
        },
        "Location": {
            "title": "Location",
            "type": "object",
            "properties": {
                "id": {
                    "description": "Location ID",
                    "example": 1,
                    "type": "integer",
                    "format": "int32",
                    "readOnly": "true"
                },
                "capturesample_id": {
                    "description": "ID of the parent CaptureSample object",
                    "example": 1,
                    "type": "integer",
                    "format": "int32"
                },
                "timestamp": {
                    "description": "Unix timestamp in seconds since January 1st 1970",
                    "example": "2019-01-15T13:09:52.456Z",
                    "type": "string",
                    "format": "date-time",
                    "readOnly": "true"
                },
                "description": {
                    "description": "Description of where a box was located at the time of a capturesample.",
                    "example": "Cupboard under the stairs",
                    "type": "string"
                }
            }
        },
        "Box": {
            "title": "Box",
            "type": "object",
            "properties": {
                "serial": {
                    "description": "Serial of the box that made the capture",
                    "example": "YWJjZGVM",
                    "type": "string"
                },
                "timeregistered": {
                    "description": "Time the box was created",
                    "format": "date-time",
                    "type": "string",
                    "example": "2019-01-15T13:09:52.456Z"
                },
            },
        },
    }
}


def create_app(settings_override=None):
    """Returns the Web API application instance"""

    app = factory.create_api_app(__name__, __path__, settings_override)
    app.register_blueprint(usersbp)
    app.register_blueprint(boxesbp)
    app.register_blueprint(capturesbp)
    app.register_blueprint(samplesbp)
    app.register_blueprint(accesstokenbp, url_prefix='/accesstoken')
    app.register_blueprint(boxviewsbp)
    app.register_blueprint(locationsbp)
    swagger = Swagger(app, template=swaggertemplate)

    return app
