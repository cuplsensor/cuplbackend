# -*- coding: utf-8 -*-
"""
    wsgi
    ~~~~
    overholt wsgi module
"""

from werkzeug.serving import run_simple
from werkzeug.debug import DebuggedApplication
from werkzeug.wsgi import DispatcherMiddleware

from charityapp.api import consumer

app = DispatcherMiddleware(consumer.create_app())
app = DebuggedApplication(app, evalex=False)

if __name__ == "__main__":
    app.debug = True
    run_simple('0.0.0.0', 80, app, use_reloader=True, use_debugger=True)
