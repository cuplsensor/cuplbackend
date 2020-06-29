# -*- coding: utf-8 -*-
"""
    flaskapp.api
    ~~~~~~~

    web api application package
"""

from functools import wraps
from ..core import OverholtError, OverholtFormError
from ..helpers import JSONEncoder
from .. import factory


from .admin.token import bp as tokenbp
from .admin.tags import bp as tagsbp


def create_app(settings_override=None):
    """Returns the Web API application instance. No longer used."""
    app = factory.create_app(__name__, __path__, settings_override)
    app.register_blueprint(tokenbp)
    app.register_blueprint(tagsbp)

    return app

def route(bp, *args, **kwargs):
    def decorator(f):
        @bp.route(*args, **kwargs)
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)
        return f

    return decorator
