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
