# -*- coding: utf-8 -*-
"""
    overholt.frontend
    ~~~~~~~~~~~~~~~~~~
    launchpad frontend application package
"""

from .. import factory
from .defs import auth0_template
from .views import bp as viewsbp
from .boxviews import bp as boxviewsbp
from .captureviews import bp as captureviewsbp
from .calviews import bp as calviewsbp

def create_app(settings_override=None):
    """Returns the Overholt dashboard application instance"""
    app = factory.create_app(__name__, __path__, settings_override)

    app.register_blueprint(viewsbp)
    app.register_blueprint(boxviewsbp)
    app.register_blueprint(calviewsbp)
    app.register_blueprint(captureviewsbp)

    app.errorhandler(404)(handle_error)
    app.errorhandler(401)(handle_error)

    return app

def handle_error(e):
    return auth0_template('errors/%s.html' % e.code, code=e.code, desc=str(e)), e.code
