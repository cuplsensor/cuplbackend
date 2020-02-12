# -*- coding: utf-8 -*-
"""
    wsgi
    ~~~~
    overholt wsgi module
"""
import os
from tests import defaults as test_defaults
from werkzeug.serving import run_simple
from werkzeug.debug import DebuggedApplication
from werkzeug.wsgi import DispatcherMiddleware

from charityapp.api import admin, consumer


def simple(env, resp):
    resp(b'200 OK', [(b'Content-Type', b'text/plain')])
    return [b'Hello WSGI World']


app = DispatcherMiddleware(simple, {
    '/api/admin/v1': admin.create_app(),
    '/api/consumer/v1': consumer.create_app()
})
app = DebuggedApplication(app, evalex=False)

if __name__ == "__main__":
    app.debug = True
    wsb_host = os.getenv("WSB_HOST", test_defaults.WSB_HOST)
    wsb_port = os.getenv("WSB_PORT", test_defaults.WSB_PORT)
    run_simple(wsb_host, wsb_port, app, use_reloader=True, use_debugger=True)
