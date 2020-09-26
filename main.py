# -*- coding: utf-8 -*-
"""
    wsgi
    ~~~~
    overholt wsgi module
"""
from werkzeug.debug import DebuggedApplication
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from flaskapp.api import admin, consumer
from rootapp import rootapp
from docsapp import docsapp
import os


app = DispatcherMiddleware(rootapp, {
        '/docs/admin': docsapp.create_app(api_docs_folder=os.path.join(os.path.dirname(__file__), 'docs/api/admin')),
        '/docs/consumer': docsapp.create_app(api_docs_folder=os.path.join(os.path.dirname(__file__), 'docs/api/consumer')),
        '/api/admin': admin.create_app(),
        '/api/consumer': consumer.create_app()
    })

if __name__ == "__main__":
    app = DebuggedApplication(app, evalex=False)
    app.debug = False
    app.run()