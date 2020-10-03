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

SQLALCHEMY_TRACK_MODIFICATIONS = False

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = os.environ['CSRF_SESSION_KEY']

# Secret key for signing cookies
SECRET_KEY = os.environ['SECRET_KEY']

# HashIds Salt
HASHIDS_SALT = os.environ['HASHIDS_SALT']
HASHIDS_OFFSET = int(os.getenv('HASHIDS_OFFSET', defaults.HASHIDS_OFFSET))

DROP_ON_INIT = bool(os.getenv('DROP_ON_INIT', defaults.DROP_ON_INIT)) # Flag to drop tables on startup.

TAGTOKEN_CLIENTID = os.getenv('TAGTOKEN_CLIENTID', defaults.TAGTOKEN_CLIENTID)
TAGTOKEN_CLIENTSECRET = os.environ['TAGTOKEN_CLIENTSECRET']

ADMINAPI_AUDIENCE = os.getenv('ADMINAPI_AUDIENCE', defaults.ADMINAPI_AUDIENCE)
ADMINAPI_CLIENTID = os.getenv('ADMINAPI_CLIENTID', defaults.ADMINAPI_CLIENTID)
ADMINAPI_CLIENTSERET = os.environ['ADMINAPI_CLIENTSECRET']

RATELIMIT_DEFAULT = os.environ.get('RATELIMIT_DEFAULT', defaults.RATELIMIT_DEFAULT)
RATELIMIT_HEADERS_ENABLED = os.getenv('RATELIMIT_HEADERS_ENABLED', defaults.RATELIMIT_HEADERS_ENABLED)
RATELIMIT_ENABLED = os.getenv('RATELIMIT_ENABLED', defaults.RATELIMIT_ENABLED)
RATELIMIT_STORAGE_URL = os.getenv('RATELIMIT_STORAGE_URL', defaults.RATELIMIT_STORAGE_URL)
RATELIMIT_STRATEGY = os.getenv('RATELIMIT_STRATEGY', defaults.RATELIMIT_STRATEGY)

WSB_PORT = os.getenv('WSB_PORT', defaults.WSB_PORT)
WSB_HOST = os.getenv('WSB_HOST', defaults.WSB_HOST)
WSB_PROTOCOL = os.getenv('WSB_PROTOCOL', defaults.WSB_PROTOCOL)
SERVER_NAME = os.getenv('SERVER_NAME', "{host}:{port}".format(host=WSB_HOST, port=WSB_PORT))

CORS_EXPOSE_HEADERS = ["Link", "X-CuplBackend-Hmac-SHA256"]

PREFERRED_URL_SCHEME = WSB_PORT.replace("://", "")

