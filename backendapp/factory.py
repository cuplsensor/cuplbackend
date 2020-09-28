# -*- coding: utf-8 -*-
"""
    web.factory
    ~~~~~~~~~~~

    web factory module for creating apps
"""

from flask import Flask
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
