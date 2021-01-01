# -*- coding: utf-8 -*-
"""
    flaskapp.api
    ~~~~~~~

    web api application package
"""

from functools import wraps
from ... import factory

from .root import bp as rootbp
from .version import bp as versionbp
from .tags import bp as tagsbp
from .captures import bp as capturesbp
from .samples import bp as samplesbp
from .webhooks import bp as webhooksbp

API_CONSUMER_PREFIX = '/api/consumer'


def create_app(settings_override=None):
    """Returns the Web API application instance"""
    (app, limiter) = factory.create_api_app(__name__, __path__, settings_override)
    app.register_blueprint(rootbp)
    app.register_blueprint(versionbp)
    app.register_blueprint(tagsbp)
    app.register_blueprint(capturesbp)
    app.register_blueprint(samplesbp)
    app.register_blueprint(webhooksbp)
    
    app.logger.info(''.join(['%s' % rule for rule in app.url_map.iter_rules()]))

    return app
