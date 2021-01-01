from backendapp.api.consumer.version import versioninfo
import os

f = open(os.path.join(os.path.dirname(__file__), 'logostr.txt'), 'r')
logostr = f.read()

from flask import Flask
rootapp = Flask(__name__)

@rootapp.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return "Page not found (rootapp)", 404

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
