# -*- coding: utf-8 -*-
"""
    wsgi
    ~~~~
    top level module
"""
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from backendapp.api import admin, consumer
from otherapps.rootapp.rootapp import rootapp
from docs.api.admin.docsapp import docsapp as admin_docsapp
from docs.api.consumer.docsapp import docsapp as consumer_docsapp
import os


app = DispatcherMiddleware(rootapp, {
        '/docs/admin': admin_docsapp,
        '/docs/consumer': consumer_docsapp,
        '/api/admin': admin.create_app(),
        '/api/consumer': consumer.create_app()
    })
