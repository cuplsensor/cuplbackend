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

ADMINAPI_AUDIENCE = "default_adminapi_audience"
ADMINAPI_CLIENTID = "default_adminapi_clientid"
TAGTOKEN_CLIENTID = "default_tagtoken_clientid"
RATELIMIT_HEADERS_ENABLED = 'True'
RATELIMIT_ENABLED = 'False'
RATELIMIT_STORAGE_URL = "memory://"
RATELIMIT_DEFAULT = "80/hour,100/day,2000/year"
RATELIMIT_STRATEGY = "fixed-window-elastic-expiry"
HASHIDS_OFFSET = 0
DROP_ON_INIT = 'False'
WSB_PORT = 5000
WSB_HOST = "localhost"
WSB_PROTOCOL = "http://"