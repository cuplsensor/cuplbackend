from flaskapp.api.consumer.version import versioninfo


def rootapp(env, resp):
    versiondict = versioninfo()
    codecversion = versiondict['cuplcodec']
    backendversion = versiondict['cuplbackend']
    versionstr = "<a href='https://github.com/cuplsensor/cuplbackend'>cuplbackend</a> version {} running " \
                 "<a href='https://github.com/cuplsensor/cuplcodec'>cuplcodec</a> version {}" \
                 "<ul>" \
                 "<li><a href='/docs/admin'>Admin API Docs</a></li>" \
                 "<li><a href='/docs/consumer'>Consumer API Docs</a></li>" \
                 "</ul>" \
                 "<ul>" \
                 "<li><a href='/api/admin'>Admin API Root</a></li>" \
                 "<li><a href='/api/consumer'>Consumer API Root</a></li>" \
                 "</ul>".format(backendversion, codecversion)
    resp('200 OK', [('Content-Type', 'text/html')])
    return [versionstr.encode('utf-8')]