from functools import wraps
from os import environ as env
from flask import render_template, session, abort, redirect, url_for, request

def route(bp, *args, **kwargs):
    def decorator(f):
        @bp.route(*args, **kwargs)
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)
        return f

    return decorator

def auth0_template(templ_name, **kwargs):
    kwargs['auth0clientid'] = env['AUTH0_CLIENTID']
    kwargs['auth0url'] = env['AUTH0_URL']
    return render_template(templ_name, **kwargs)

# Optional auth decorator
def optional_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    user = session.get('user')
    # TODO: Verify user token here to make sure it has not expired.
    #  If it has, pop the access token and user info from the session.
    return f(userobj=user, *args, **kwargs)
  return decorated

# Requires auth decorator
def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    user = session.get('user')
    if user == None:
        return redirect(url_for('dashboard.signin', next=request.url))
    return f(userobj=user, *args, **kwargs)
  return decorated
