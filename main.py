# -*- coding: utf-8 -*-
"""
    wsgi
    ~~~~
    overholt wsgi module
"""
from werkzeug.serving import run_simple
from werkzeug.debug import DebuggedApplication
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from flaskapp.api import admin, consumer


def simple(env, resp):
    resp('200 OK', [('Content-Type', 'text/plain')])
    return [b'Hello WSGI World']


app = DispatcherMiddleware(simple, {
        '/api/admin': admin.create_app(),
        '/api/consumer': consumer.create_app()
    })

if __name__ == "__main__":
    app = DebuggedApplication(app, evalex=False)
    app.debug = True
    app.run()