from base64 import b64decode
from . import defaults

# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = 'home/debian/'


# Define the database - we are working with
# SQLite for this example
DB_NAME = os.environ['DB_NAME']
DB_USER = os.environ['DB_USER']
DB_PASS = os.environ['DB_PASS']
DB_HOST = os.environ['DB_HOST']
DB_PORT = os.environ['DB_PORT']
SQLALCHEMY_DATABASE_URI = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
        DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME
    )
DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Set config values for Flask-Security.
# We're using PBKDF2 with salt.
SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
# Replace this with your own salt.
SECURITY_PASSWORD_SALT = 'asfea44fafaefu4gh398ognrveffi4onkn32fhrn2new'

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = os.environ['CSRF_SESSION_KEY']

# Secret key for signing cookies
SECRET_KEY = os.environ['SECRET_KEY']

AUTH0_URL = os.getenv('AUTH0_URL', defaults.AUTH0_URL)
API_AUDIENCE = os.getenv('API_AUDIENCE', defaults.API_AUDIENCE)
JWKS_ENDPOINT = os.getenv('JWKS_ENDPOINT', defaults.JWKS_ENDPOINT)
ADMINAPI_AUDIENCE = os.getenv('ADMINAPI_AUDIENCE', defaults.ADMINAPI_AUDIENCE)
ADMINAPI_CLIENTID = os.getenv('ADMINAPI_CLIENTID', defaults.ADMINAPI_CLIENTID)
ADMINAPI_CLIENTSERET = os.environ['ADMINAPI_CLIENTSECRET']

# Auth0 credentials for decoding a JWT. Moved to wsfrontend.
#AUTHO_CLIENTSECRET = b64decode(os.environ['AUTH0_CLIENTSECRET'].replace("_","/").replace("-","+"))
#AUTH0_CLIENTID = os.environ['AUTH0_CLIENTID']


