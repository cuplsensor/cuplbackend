# -*- coding: utf-8 -*-
"""
    web.factory
    ~~~~~~~~~~~

    web factory module for creating apps
"""

from flask import Flask

from .core import db

def create_api_app(package_name, package_path, settings_override=None):
    app = create_app(package_name, settings_override)

    # Configure the database
    db.init_app(app)

    # Drop all uses a tip from http://piotr.banaszkiewicz.org/blog/2012/06/29/flask-sqlalchemy-init_app/
    with app.test_request_context():
        db.drop_all()
        db.create_all()
    # Register all blueprints to the application
    # register_blueprints(app, package_name, package_path.api)

    return app

def create_app(package_name, package_path, settings_override=None):
    """Return a Flask application instance configured with common
    functionality for the web platform.

    :param package_name: application package name
    :param package_path: application package package_path
    :param settings_override: a dictionary of settings to override
    """
    app = Flask(package_name, instance_relative_config=True)

    #app.config.from_pyfile('settings.cfg', silent=True)
    app.config.from_object('flaskapp.config')
    app.config.from_object(settings_override)

    # Drop all uses a tip from http://piotr.banaszkiewicz.org/blog/2012/06/29/flask-sqlalchemy-init_app/
    #with app.test_request_context():
    #    db.drop_all()
    #    db.create_all()
    # Register all blueprints to the application
    #register_blueprints(app, package_name, package_path.api)

    return app
