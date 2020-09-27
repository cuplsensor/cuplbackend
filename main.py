# -*- coding: utf-8 -*-
"""
    wsgi
    ~~~~
    top level module
"""
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from cuplbackend.api import admin, consumer
from otherapps.rootapp.rootapp import rootapp
from otherapps.docsapp import docsapp
import os


app = DispatcherMiddleware(rootapp, {
        '/docs/admin': docsapp.create_app(api_docs_folder=os.path.join(os.path.dirname(__file__), 'docs/api/admin')),
        '/docs/consumer': docsapp.create_app(api_docs_folder=os.path.join(os.path.dirname(__file__), 'docs/api/consumer')),
        '/api/admin': admin.create_app(),
        '/api/consumer': consumer.create_app()
    })