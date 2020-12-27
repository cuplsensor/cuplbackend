from backendapp.api.consumer.version import versioninfo
import os

f = open(os.path.join(os.path.dirname(__file__), 'logostr.txt'), 'r')
logostr = f.read()


def rootapp(env, resp):
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
    resp('200 OK', [('Content-Type', 'text/html')])
    return [versionstr.encode('utf-8')]
