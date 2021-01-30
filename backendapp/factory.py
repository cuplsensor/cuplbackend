# -*- coding: utf-8 -*-

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


from flask import Flask, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from .core import db


def create_api_app(package_name, package_path, settings_override=None):
    app = create_app(package_name, settings_override)

    # Configure the database
    db.init_app(app)

    # Drop all uses a tip from http://piotr.banaszkiewicz.org/blog/2012/06/29/flask-sqlalchemy-init_app/
    with app.test_request_context():
        if app.config.get('DROP_ON_INIT') is True:
            db.drop_all()
        db.create_all()

    # Enable CORS. An API is unlikely to work without this.
    CORS(app)

    # Enable rate limiting.
    limiter = Limiter(
        app,
        key_func=get_remote_address
    )

    # Do not apply a limit to OPTIONS. If the OPTIONS pre-flight returns 429
    # then the browser displays a CORS error and the underlying API error is hidden
    # behind a 'fetch failed' message. Many thanks to tkrajca at
    # https://github.com/alisaifee/flask-limiter/issues/70
    limiter.request_filter(lambda: request.method.upper() == 'OPTIONS')

    return app, limiter


def create_app(package_name, package_path, settings_override=None):
    """Return a Flask application instance configured with common
    functionality for the web platform.

    :param package_name: application package name
    :param package_path: application package package_path
    :param settings_override: a dictionary of settings to override
    """
    app = Flask(package_name, instance_relative_config=True)

    app.config.from_object('backendapp.config')
    app.config.from_object(settings_override)

    return app
