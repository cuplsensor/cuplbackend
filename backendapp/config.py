#  A web application that stores samples from a collection of NFC sensors.
#
#  https://github.com/cuplsensor/cuplbackend
#
#  Original Author: Malcolm Mackay
#  Email: malcolm@plotsensor.com
#  Website: https://cupl.co.uk
#
#  Copyright (c) 2021. Plotsensor Ltd.
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License
#  as published by the Free Software Foundation, either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the
#  GNU Affero General Public License along with this program.
#  If not, see <https://www.gnu.org/licenses/>.

#  A web application that stores samples from a collection of NFC sensors.
#
#  https://github.com/cuplsensor/cuplbackend
#
#  Original Author: Malcolm Mackay
#  Email: malcolm@plotsensor.com
#  Website: https://cupl.co.uk
#
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License
#  as published by the Free Software Foundation, either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the
#  GNU Affero General Public License along with this program.
#  If not, see <https://www.gnu.org/licenses/>.

from base64 import b64decode
from . import defaults

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
DB_SSLMODE = os.getenv('DB_SSLMODE', None) # Needs to be 'require' or 'verify-ca' for SSL to work.
DB_SSLROOTCERT = os.getenv('DB_SSLROOTCERT', None)

# https://stackoverflow.com/questions/36372772/flask-sqlalchemy-ssl-connection-with-aws-rds-error
sslstr = ''
if isinstance(DB_SSLMODE, str):
    sslstr += '?sslmode={0}'.format(DB_SSLMODE, DB_SSLROOTCERT)
    if isinstance(DB_SSLROOTCERT, str):
        sslstr += '&sslrootcert={0}'.format(DB_SSLROOTCERT)

SQLALCHEMY_DATABASE_URI = 'postgresql://{0}:{1}@{2}:{3}/{4}{5}'.format(
        DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME, sslstr
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

DROP_ON_INIT = (os.getenv('DROP_ON_INIT', defaults.DROP_ON_INIT).lower() == 'true')  # Flag to drop tables on startup.

TAGTOKEN_CLIENTID = os.getenv('TAGTOKEN_CLIENTID', defaults.TAGTOKEN_CLIENTID)
TAGTOKEN_CLIENTSECRET = os.environ['TAGTOKEN_CLIENTSECRET']

ADMINAPI_AUDIENCE = os.getenv('ADMINAPI_AUDIENCE', defaults.ADMINAPI_AUDIENCE)
ADMINAPI_CLIENTID = os.getenv('ADMINAPI_CLIENTID', defaults.ADMINAPI_CLIENTID)
ADMINAPI_CLIENTSERET = os.environ['ADMINAPI_CLIENTSECRET']

RATELIMIT_DEFAULT = os.environ.get('RATELIMIT_DEFAULT', defaults.RATELIMIT_DEFAULT)
RATELIMIT_HEADERS_ENABLED = (os.getenv('RATELIMIT_HEADERS_ENABLED', defaults.RATELIMIT_HEADERS_ENABLED).lower() == 'true')
RATELIMIT_ENABLED = (os.getenv('RATELIMIT_ENABLED', defaults.RATELIMIT_ENABLED).lower() == 'true')
RATELIMIT_STORAGE_URL = os.getenv('RATELIMIT_STORAGE_URL', defaults.RATELIMIT_STORAGE_URL)
RATELIMIT_STRATEGY = os.getenv('RATELIMIT_STRATEGY', defaults.RATELIMIT_STRATEGY)

WSB_PORT = os.getenv('WSB_PORT', defaults.WSB_PORT)
WSB_HOST = os.getenv('WSB_HOST', defaults.WSB_HOST)
WSB_PROTOCOL = os.getenv('WSB_PROTOCOL', defaults.WSB_PROTOCOL)
SERVER_NAME = os.getenv('SERVER_NAME', None) #os.getenv('SERVER_NAME', "{host}:{port}".format(host=WSB_HOST, port=WSB_PORT))

CORS_EXPOSE_HEADERS = ["Link", "X-CuplBackend-Hmac-SHA256"]

PREFERRED_URL_SCHEME = WSB_PORT.replace("://", "")

