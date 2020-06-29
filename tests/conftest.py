import os
import pytest
from dotenv import load_dotenv
import sys
import pytz
import datetime
import requests
from . import defaults

from .helpers.capturehelper import CaptureListHelper
from ..wsapiwrapper.admin import request_admin_token
from ..wsapiwrapper.admin.tag import TagWrapper
from ..wsapiwrapper.consumer.user import UserWrapper
from ..wsapiwrapper.consumer.mecapture import MeCaptureWrapper
from ..wsapiwrapper.consumer.tagview import TagViewWrapper
from ..wsapiwrapper.consumer.tagscanned import TagScannedWrapper
from ..wsapiwrapper.consumer.location import LocationWrapper
from ..wsapiwrapper.consumer.sample import SampleWrapper

sys.path.append(".")


@pytest.fixture(scope="function")
def token_fixture(idporigin):
    payload = {'grant_type': 'authorization_code'}
    r = requests.post('{idporigin}/token'.format(idporigin=idporigin), data=payload)
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
def two_captures_on_two_tags_fixture(tag_with_captures_fixture, user_fixture):
    tagcaptures = []

    # Create 2 tags with 2 captures each. These captures are assigned to the current user ID.
    capspecgen = generate_capspec(user_id=user_fixture['id'])

    # Create 1 tag with 2 captures that does not have a user ID. These captures should not be returned by the
    # mecaptures endpoint.
    capspecgen_nouser = generate_capspec()

    capspec1 = next(capspecgen)
    capspec2 = next(capspecgen)
    capspec3 = next(capspecgen_nouser)

    tagcaptures.append(tag_with_captures_fixture.get(capspec1))
    tagcaptures.append(tag_with_captures_fixture.get(capspec2))

    tag_with_captures_fixture.get(capspec3) # We do not expect these captures to be returned

    return tagcaptures


@pytest.fixture
def baseurl():
    """ Return baseurl environment variable. """
    wsb_protocol = os.getenv("WSB_PROTOCOL", defaults.WSB_PROTOCOL)
    wsb_host = os.getenv("WSB_HOST", defaults.WSB_HOST)
    wsb_port = os.getenv("WSB_PORT", defaults.WSB_PORT)
    return '{wsb_protocol}{wsb_host}:{wsb_port}'.format(wsb_protocol=wsb_protocol, wsb_host=wsb_host, wsb_port=str(wsb_port))

@pytest.fixture
def idporigin():
    idp_protocol = os.getenv("IDP_PROTOCOL", defaults.IDP_PROTOCOL)
    idp_host = os.getenv("IDP_HOST", defaults.IDP_HOST)
    idp_port = os.getenv("IDP_PORT", defaults.IDP_PORT)
    return '{idp_protocol}{idp_host}:{idp_port}'.format(idp_protocol=idp_protocol, idp_host=idp_host, idp_port=str(idp_port))


@pytest.fixture
def clientid():
    """ Return client id environment variable. """
    return os.getenv("ADMINAPI_CLIENTID", defaults.ADMINAPI_CLIENTID)


@pytest.fixture
def clientsecret():
    """ Return client secret environment variable. """
    return os.getenv("ADMINAPI_CLIENTSECRET", defaults.ADMINAPI_CLIENTSECRET)


@pytest.fixture
def admintoken(baseurl, clientid, clientsecret):
    return request_admin_token(baseurl, clientid, clientsecret)


@pytest.fixture(scope="function")
def tag_fixture(request, baseurl, admintoken):
    taghelper = TagWrapper(baseurl, admintoken)

    def teardown():
        tagid = tagresponse['id']
        print("teardown tag fixture")
        taghelper.delete(tagid)

    request.addfinalizer(teardown)

    tagresponse = taghelper.post()
    return tagresponse

@pytest.fixture(scope="function")
def mecapture_fixture(token_fixture, baseurl):
    mecaphelper = MeCaptureWrapper(baseurl, tokenstr=token_fixture)
    return mecaphelper


@pytest.fixture(scope="function")
def tag_fixture_b(request, baseurl, admintoken):
    taghelper = TagWrapper(baseurl, admintoken)

    class TagFactory(object):
        tagids = []
        def add(self):
            tagresponse = taghelper.post()
            tagid = tagresponse['id']
            self.tagids.append(tagid)
            return tagresponse

        def delete_all(self):
            for tagid in self.tagids:
                taghelper.delete(tagid)

    bf = TagFactory()

    def teardown():
        print("teardown all tags")
        bf.delete_all()

    request.addfinalizer(teardown)
    return bf

@pytest.fixture(scope="function")
def tagview_fixture(baseurl, token_fixture):
    return TagViewWrapper(baseurl, token_fixture)

@pytest.fixture(scope="function")
def tagscanned_fixture(baseurl, token_fixture):
    return TagScannedWrapper(baseurl, token_fixture)

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
def tag_with_captures_fixture(baseurl, admintoken, tag_fixture_b):
    class TagWithCapturesFactory(object):

        def get(self, capturespeclist):
            tag = tag_fixture_b.add()
            clisthelper = CaptureListHelper(baseurl, admintoken, capturespeclist, tagid=tag['id'])
            return {'tag': tag, 'clisthelper': clisthelper}

    return TagWithCapturesFactory()
