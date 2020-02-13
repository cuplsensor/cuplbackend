import os
import pytest
from dotenv import load_dotenv
import sys
import pytz
import datetime
import requests
from . import defaults

from .helpers.capturehelper import CaptureListHelper
from wsbackend.apiwrapper.admin.box import BoxWrapper
from wsbackend.apiwrapper.consumer.user import UserWrapper
from wsbackend.apiwrapper.consumer.mecapture import MeCaptureWrapper
from wsbackend.apiwrapper.consumer.boxview import BoxViewWrapper
from wsbackend.apiwrapper.consumer.boxscanned import BoxScannedWrapper
from wsbackend.apiwrapper.consumer.location import LocationWrapper
from wsbackend.apiwrapper.consumer.sample import SampleWrapper

sys.path.append(".")


@pytest.fixture(scope="function")
def token_fixture(baseurl):
    payload = {'grant_type': 'authorization_code'}
    r = requests.post('{baseurl}/token'.format(baseurl=baseurl), data=payload)
    unverified_token = r.json().get('access_token')

    return unverified_token


def pytest_runtest_setup(item):
    """ called before ``pytest_runtest_call(item). """
    # do some stuff`
    # Load environment variables from the .env file in the project root.
    basepath = os.path.dirname(__file__)
    envpath = os.path.abspath(os.path.join(basepath, "..", "..", ".env"))
    load_dotenv(dotenv_path=envpath)


def generate_capspec(user_id=None):
    starttime = datetime.datetime.now().replace(tzinfo=pytz.utc)
    hourtimedelta = datetime.timedelta(hours=1)
    hoursafter = 0

    while hoursafter < 100:
        capturespeclist = [
            {
                'starttime': starttime + hourtimedelta * hoursafter,
                'nsamples': 4,
                'user_id': user_id
            },
            {
                'starttime': starttime + hourtimedelta * (hoursafter + 1),
                'nsamples': 5,
                'user_id': user_id
            }
        ]

        hoursafter += 2

        yield capturespeclist


@pytest.fixture(scope="function")
def two_captures_on_two_boxes_fixture(box_with_captures_fixture, user_fixture):
    boxcaptures = []

    # Create 2 boxes with 2 captures each. These captures are assigned to the current user ID.
    capspecgen = generate_capspec(user_id=user_fixture['id'])

    # Create 1 box with 2 captures that does not have a user ID. These captures should not be returned by the
    # mecaptures endpoint.
    capspecgen_nouser = generate_capspec()

    capspec1 = next(capspecgen)
    capspec2 = next(capspecgen)
    capspec3 = next(capspecgen_nouser)

    boxcaptures.append(box_with_captures_fixture.get(capspec1))
    boxcaptures.append(box_with_captures_fixture.get(capspec2))

    box_with_captures_fixture.get(capspec3) # We do not expect these captures to be returned

    return boxcaptures


@pytest.fixture
def baseurl():
    """ Return baseurl environment variable. """
    wsb_protocol = os.getenv("WSB_PROTOCOL", defaults.WSB_PROTOCOL)
    wsb_host = os.getenv("WSB_HOST", defaults.WSB_HOST)
    wsb_port = os.getenv("WSB_PORT", defaults.WSB_PORT)
    return '{wsb_protocol}{wsb_host}:{wsb_port}'.format(wsb_protocol=wsb_protocol, wsb_host=wsb_host, wsb_port=str(wsb_port))


@pytest.fixture
def clientid():
    """ Return client id environment variable. """
    return os.getenv("ADMINAPI_CLIENTID", defaults.ADMINAPI_CLIENTID)


@pytest.fixture
def clientsecret():
    """ Return client secret environment variable. """
    return os.environ.get("ADMINAPI_CLIENTSECRET")


@pytest.fixture(scope="function")
def box_fixture(request, baseurl):
    boxhelper = BoxWrapper(baseurl)

    def teardown():
        boxid = boxresponse['id']
        print("teardown box fixture")
        boxhelper.delete(boxid)

    request.addfinalizer(teardown)

    boxresponse = boxhelper.post()
    return boxresponse

@pytest.fixture(scope="function")
def mecapture_fixture(token_fixture, baseurl):
    mecaphelper = MeCaptureWrapper(baseurl, tokenstr=token_fixture)
    return mecaphelper


@pytest.fixture(scope="function")
def box_fixture_b(request, baseurl, clientid, clientsecret):
    boxhelper = BoxWrapper(baseurl, clientid, clientsecret)

    class BoxFactory(object):
        boxids = []
        def add(self):
            boxresponse = boxhelper.post()
            boxid = boxresponse['id']
            self.boxids.append(boxid)
            return boxresponse

        def delete_all(self):
            for boxid in self.boxids:
                boxhelper.delete(boxid)

    bf = BoxFactory()

    def teardown():
        print("teardown all boxes")
        bf.delete_all()

    request.addfinalizer(teardown)
    return bf

@pytest.fixture(scope="function")
def boxview_fixture(baseurl, token_fixture):
    return BoxViewWrapper(baseurl, token_fixture)

@pytest.fixture(scope="function")
def boxscanned_fixture(baseurl, token_fixture):
    return BoxScannedWrapper(baseurl, token_fixture)

@pytest.fixture(scope="function")
def location_fixture(baseurl, token_fixture):
    return LocationWrapper(baseurl, token_fixture)

@pytest.fixture(scope="function")
def sample_fixture(baseurl, token_fixture):
    return SampleWrapper(baseurl, token_fixture)

@pytest.fixture(scope="function")
def user_fixture(request, baseurl, token_fixture):
    userhelper = UserWrapper(baseurl, tokenstr=token_fixture)

    def teardown():
        print("teardown test user")
        userhelper.delete()

    request.addfinalizer(teardown)
    return userhelper.post()



@pytest.fixture(scope="function")
def box_with_captures_fixture(baseurl, clientid, clientsecret, box_fixture_b):
    class BoxWithCapturesFactory(object):

        def get(self, capturespeclist):
            box = box_fixture_b.add()
            clisthelper = CaptureListHelper(baseurl, clientid, clientsecret, capturespeclist, boxid=box['id'])
            return {'box': box, 'clisthelper': clisthelper}

    return BoxWithCapturesFactory()