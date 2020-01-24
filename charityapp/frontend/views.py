from flask import Blueprint, redirect, render_template, \
request, url_for, session, abort, flash, Response, jsonify, current_app
from flask_login import login_user, current_user
from ..core import sec
from ..schemas import BoxViewSchema, BoxViewNestedSchema
from werkzeug.exceptions import NotFound
from ..apiwrapper.consumer.user import UserWrapper, UserNotFoundException
from ..apiwrapper.consumer.capture import CaptureWrapper

# For GET and POST
import requests
import json
import os
from .defs import auth0_template, requires_auth, optional_auth, route
import datetime

auth0clientid = os.environ["AUTH0_CLIENTID"]
auth0clientsecret = os.environ["AUTH0_CLIENTSECRET"]
auth0apiuniqueid = os.environ["AUTH0_API_UNIQUEID"]
auth0url = os.environ["AUTH0_URL"]

# static_url_path needed because of http://stackoverflow.com/questions/22152840/flask-blueprint-static-directory-does-not-work
bp = Blueprint('dashboard', __name__, template_folder='templates', static_folder='static', static_url_path=os.environ['STATIC_URL'])

callbackurl = "https://{baseurl}/callback".format(baseurl=os.environ['BASE_URL'])

@route(bp, '/.well-known/acme-challenge/<token_value>')
def letsencrpyt(token_value):
    with open('.well-known/acme-challenge/{}'.format(token_value)) as f:
        answer = f.readline().strip()
    return answer


@bp.route('/')
@optional_auth
def home_page(**kwargs):
    """ Home page is accessible to all."""
    serial = request.args.get('s')
    statusb64 = request.args.get('x')
    timeintb64 = request.args.get('t')
    circbufb64 = request.args.get('q')
    versionStr = request.args.get('v')

    if serial is not None:
        capturewrapper = CaptureWrapper()

        capt = capturewrapper.post(circbufb64, serial, statusb64, timeintb64, versionStr)
        response = redirect(url_for('captureview.capture', captid=capt['id']))
    else:
        response = auth0_template('pages/home_page.html', **kwargs)

    return response

@route(bp, '/user/<int:user_id>')
def user(**kwargs):
    #userobj = users.get_or_404(user_id)
    return render_template('pages/user_page.html', **kwargs)

@route(bp, '/user')
@requires_auth
def currentuser(userobj, **kwargs):
    vlogitems = userobj.recent_boxviews
    vlschema = BoxViewNestedSchema(many=True)
    vlogitemsjson = vlschema.dump(vlogitems).data
    return auth0_template('pages/currentuser_page.html', userobj=userobj, vlogitems=vlogitems, vlogitemsjson=vlogitemsjson, **kwargs)

@route(bp, '/signin')
def signin():
    nexturl = request.args.get('next')
    if nexturl is None:
        returl = request.referrer or '/'
    else:
        returl = nexturl

    callbackurl = url_for('dashboard.callback', _external=True)
    authorizeurl = "https://{auth0url}/authorize?" \
                   "response_type=code&" \
                   "client_id={auth0clientid}&" \
                   "redirect_uri={callbackurl}&" \
                   "scope=openid%20profile&" \
                   "audience={auth0apiuniqueid}&" \
                   "state={returl}".format(auth0url=auth0url,
                                         auth0clientid=auth0clientid,
                                         callbackurl=callbackurl,
                                         auth0apiuniqueid=auth0apiuniqueid,
                                         returl=returl)

    return redirect(authorizeurl)

@route(bp, '/signout')
def signout():
    session.pop("access_token", None)
    session.pop("user", None)
    return auth0_template('pages/signout_page.html')

# Here we're using the /callback route.
@route(bp, '/callback')
def callback():
    # Extract the authorization code from the request URL
    code = request.args.get('code')
    state = request.args.get('state')

    json_header = {'content-type': 'application/json'}
    token_url = "https://{auth0url}/oauth/token".format(auth0url=auth0url)
    callbackurl = url_for('dashboard.callback', _external=True)

    token_payload = {
        'client_id': auth0clientid,
        'client_secret': auth0clientsecret,
        'redirect_uri': callbackurl,
        'code': code,
        'grant_type': 'authorization_code'
    }

    tokenresponse = requests.post(token_url, data=json.dumps(token_payload), headers=json_header).json()
    access_token = tokenresponse["access_token"]
    session["access_token"] = access_token

    userwrapper = UserWrapper(access_token)

    try:
        usr = userwrapper.get()
    except UserNotFoundException:
        usr = userwrapper.post()

    session['user'] = usr

    if state is not None:
        response = redirect(state)
    else:
        response = redirect(url_for('dashboard.currentuser'))

    return response
