# -*- coding: utf-8 -*-
"""
    flaskapp.api
    ~~~~~~~

    web api application package
"""

#  A web application that stores samples from a collection of NFC sensors.
#
#  https://github.com/cuplsensor/cuplbackend
#
#  Original Author: Malcolm Mackay
#  Email: malcolm@plotsensor.com
#  Website: https://cupl.co.uk
#
#  Copyright (c) 2021. Plotsensor Ltd.
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License
#  as published by the Free Software Foundation, either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the
#  GNU Affero General Public License along with this program.
#  If not, see <https://www.gnu.org/licenses/>.

from functools import wraps
from flask import jsonify, request, current_app, url_for
from ... import factory

from .root import bp as rootbp
from .token import bp as tokenbp
from .tags import bp as tagsbp
from .captures import bp as capturesbp
from .webhooks import bp as webhooksbp

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)    
    
def page_not_found(e):
    links = []
    for rule in current_app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    # links is now a list of url, endpoint tuples
    # note that we set the 404 status explicitly
    url = request.url
    return jsonify(error=str(e), url=url, urlmap=links), 404


def create_app(settings_override=None):
    """Returns the Web API application instance"""
    (app, limiter) = factory.create_api_app(__name__, __path__, settings_override)
    app.register_blueprint(rootbp)
    app.register_blueprint(tokenbp)
    app.register_blueprint(tagsbp)
    app.register_blueprint(capturesbp)
    app.register_blueprint(webhooksbp)
    app.register_error_handler(404, page_not_found)
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
