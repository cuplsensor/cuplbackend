# -*- coding: utf-8 -*-
"""
    flaskapp.api
    ~~~~~~~

    web api application package
"""

from functools import wraps
from ... import factory

from .token import bp as tokenbp
from .tags import bp as tagsbp
from .captures import bp as capturesbp
from .webhooks import bp as webhooksbp


def create_app(settings_override=None):
    """Returns the Web API application instance"""
    (app, limiter) = factory.create_api_app(__name__, __path__, settings_override)
    app.register_blueprint(tokenbp)
    app.register_blueprint(tagsbp)
    app.register_blueprint(capturesbp)
    app.register_blueprint(webhooksbp)
    limiter.exempt(tagsbp)
    limiter.exempt(capturesbp)
    limiter.exempt(webhooksbp)

    return app


def route(bp, *args, **kwargs):
    def decorator(f):
        @bp.route(*args, **kwargs)
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)
        return f

    return decorator
