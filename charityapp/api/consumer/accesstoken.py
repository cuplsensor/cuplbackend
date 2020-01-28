"""
    charityapp.api.admin.token
    ~~~~~~~~~~~~~~

    Token endpoints
"""

from flask import Flask, Blueprint, request, current_app, url_for, render_template, app, send_file
import os
import requests
import json
from ...core import db
#from eralchemy import render_er

baseurl = os.environ["BASE_URL"]
auth0clientid = os.environ["AUTH0_CLIENTID"]
auth0clientsecret = os.environ["AUTH0_CLIENTSECRET"]
auth0apiuniqueid = os.environ["AUTH0_API_UNIQUEID"]
auth0url = os.environ["AUTH0_URL"]

bp = Blueprint('accesstoken', __name__, template_folder='templates/accesstoken')

# https://auth0.com/docs/flows/guides/regular-web-app-login-flow/
# add-login-using-regular-web-app-login-flow
@bp.route('/')
def hello_world():
    callbackurl = url_for('accesstoken.callback', _external=True)
    authorizeurl = "https://{auth0url}/authorize?"\
                   "response_type=code&"\
                   "client_id={auth0clientid}&"\
                   "redirect_uri={callbackurl}&"\
                   "scope=openid%20profile&"\
                   "audience={auth0apiuniqueid}&"\
                   "state=xyzabc".format(auth0url=auth0url,
                                         auth0clientid=auth0clientid,
                                         callbackurl=callbackurl,
                                         auth0apiuniqueid=auth0apiuniqueid)
    return render_template('index.html', authorizeurl=authorizeurl)

@bp.route('/callback')
def callback():
    # Extract the authorization code from the request URL
    code = request.args.get('code')

    json_header = {'content-type': 'application/json'}
    token_url = "https://{auth0url}/oauth/token".format(auth0url=auth0url)
    callbackurl = url_for('accesstoken.callback', _external=True)

    token_payload = {
        'client_id': auth0clientid,
        'client_secret': auth0clientsecret,
        'redirect_uri': callbackurl,
        'code': code,
        'grant_type': 'authorization_code'
    }

    tokenresponse = requests.post(token_url, data=json.dumps(token_payload), headers=json_header).json()
    current_app.logger.info(tokenresponse)

    return tokenresponse['access_token']


# Create an entity relation diagram from the SQL database.
# Normally disable this endpoint.
#@bp.route('/erdiagram')
#def erdiagram():
    # https://stackoverflow.com/questions/8637153/how-to-return-images-in-flask-response
    #filename = '/erdiagram.png'
    #render_er(db.Model, filename)
    #return send_file(filename, 'image/png')