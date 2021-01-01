from backendapp.api.consumer.version import versioninfo
from flask import jsonify, request, current_app, url_for
import os

f = open(os.path.join(os.path.dirname(__file__), 'logostr.txt'), 'r')
logostr = f.read()

from flask import Flask
rootapp = Flask(__name__)


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

@rootapp.errorhandler(404)
def page_not_found(e):
    links = []
    for rule in current_app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    # note that we set the 404 status explicitly
    return jsonify(error="not found (rootapp)", url=url, urlmap=links), 404

@rootapp.route('/')
def root_page():
    versiondict = versioninfo()
    codecversion = versiondict['cuplcodec']
    backendversion = versiondict['cuplbackend']
    versionstr = "<pre style='font-size:0.25em'>{}</pre>" \
                 "<a href='https://github.com/cuplsensor/cuplbackend'>cuplbackend</a> version {} running " \
                 "<a href='https://github.com/cuplsensor/cuplcodec'>cuplcodec</a> version {}" \
                 "<ul>" \
                 "<li><a href='/docs/admin'>Admin API Docs</a></li>" \
                 "<li><a href='/docs/consumer'>Consumer API Docs</a></li>" \
                 "</ul>" \
                 "<ul>" \
                 "<li><a href='api/admin'>Admin API Root</a></li>" \
                 "<li><a href='api/consumer'>Consumer API Root</a></li>" \
                 "</ul>".format(logostr, backendversion, codecversion)
    return versionstr
