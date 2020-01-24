from flask import Blueprint, redirect, render_template, \
    request, url_for, session, abort, flash, Response, jsonify, current_app
# from ..services import boxes, viewlogitems
from werkzeug.exceptions import NotFound
from ..apiwrapper.consumer.capture import CaptureWrapper
from ..apiwrapper.consumer.box import BoxWrapper

# For GET and POST
import requests
import json
import os
from .defs import auth0_template, requires_auth, optional_auth, route

# static_url_path needed because of http://stackoverflow.com/questions/22152840/flask-blueprint-static-directory-does-not-work
bp = Blueprint('boxview', __name__, template_folder='templates/pages/box', static_folder='static',
               static_url_path='/static/frontend', url_prefix='/box')


@bp.errorhandler(NotFound)
def handle_error(e):
    return render_template('errors/%s.html' % e.code), e.code


@route(bp, '/<string:serial>')
@optional_auth
def box(serial, **kwargs):
    boxwrapper = BoxWrapper()
    box = boxwrapper.get(boxserial=serial)

    capturewrapper = CaptureWrapper()
    latestcapture = capturewrapper.get_list(serial, offset=0, limit=1)[0]
    latestsample = capturewrapper.get_samples(capture_id=latestcapture['id'],
                                              offset=0,
                                              limit=1)[0]

    # viewlogitems.create(boxobj=boxwithserial, **kwargs)
    return auth0_template('box_page.html'
                          , box=box
                          , latestcapture=latestcapture
                          , latestsample=latestsample
                          , **kwargs)
