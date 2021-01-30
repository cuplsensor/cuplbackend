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

import pytest
import pytz
import datetime


def create_capture_get_samples(capturespeclist, tagwithcaptures, samplewrapper):
    bwc = tagwithcaptures.get(capturespeclist)

    tag = bwc['tag']
    clisthelper = bwc['clisthelper']

    captures_in = clisthelper.writtencaptures
    starttime = clisthelper.mints
    endtime = clisthelper.maxts

    samples_out = samplewrapper.get_samples(tag['serial'], starttime, endtime)
    return captures_in, samples_out


def test_samples(tag_with_captures_fixture, sample_fixture, capture_fixture):
    starttime = datetime.datetime.now().replace(tzinfo=pytz.utc)
    capturespeclist = [
        {
            'starttime': starttime,
            'nsamples': 4
        },
        {
            'starttime': starttime+datetime.timedelta(seconds=2),
            'nsamples': 5
        }
    ]
    captures_in, samples_out = create_capture_get_samples(capturespeclist, tag_with_captures_fixture, sample_fixture)
    captures_in[0]['samples'] = capture_fixture.get_samples(capture_id=captures_in[0]['id'])
    captures_in[1]['samples'] = capture_fixture.get_samples(capture_id=captures_in[1]['id'])

    # Newest to oldest order
    expectedsamples = [
        captures_in[1]['samples'][0],
        captures_in[0]['samples'][0],
        captures_in[0]['samples'][1],
        captures_in[0]['samples'][2],
        captures_in[0]['samples'][3],
        ]

    print(expectedsamples)
    print(samples_out)
    assert expectedsamples == samples_out


def test_samples_two(tag_with_captures_fixture, sample_fixture, capture_fixture):
    starttime = datetime.datetime.now().replace(tzinfo=pytz.utc)
    capturespeclist = [
        {
            'starttime': starttime,
            'nsamples': 4
        },
    ]
    captures_in, samples_out = create_capture_get_samples(capturespeclist, tag_with_captures_fixture, sample_fixture)
    captures_in[0]['samples'] = capture_fixture.get_samples(capture_id=captures_in[0]['id'])

    expectedsamples = [
        captures_in[0]['samples'][0],
        captures_in[0]['samples'][1],
        captures_in[0]['samples'][2],
        captures_in[0]['samples'][3]
        ]

    print(expectedsamples)
    print(samples_out)
    assert expectedsamples == samples_out


if __name__ == "__main__":
    pytest.main()
