import pytest
from .conftest import generate_capspec


@pytest.fixture(scope="function")
def box_with_mecapture_fixture(box_with_captures_fixture, user_fixture):
    capspecgen = generate_capspec(user_id=user_fixture['id'])

    capspec1 = next(capspecgen)

    return box_with_captures_fixture.get(capspec1)


def test_scannedbyuser_true(box_with_mecapture_fixture, boxscanned_fixture):
    boxserial = box_with_mecapture_fixture['box']['serial']

    expected = True
    scannedbyuser = boxscanned_fixture.get(boxserial=boxserial)

    assert expected == scannedbyuser


def test_scannedbyuser_false(box_with_captures_fixture, user_fixture, boxscanned_fixture):
    # Generate a capture with no user
    capspecgen = generate_capspec()

    capspec1 = next(capspecgen)

    boxwithcapture = box_with_captures_fixture.get(capspec1)['box']
    boxserial = boxwithcapture['serial']

    expected = False
    scannedbyuser = boxscanned_fixture.get(boxserial=boxserial)

    assert expected == scannedbyuser


def test_post_location(box_with_mecapture_fixture, location_fixture):
    boxserial = box_with_mecapture_fixture['box']['serial']
    capturesample = box_with_mecapture_fixture['clisthelper'].writtencaptures[0]['samples'][0]

    response = location_fixture.post(capturesample['id'], description="test location")

    assert response['parent_capturesample'] == capturesample['id']


def test_get_location_list(box_with_mecapture_fixture, location_fixture):
    boxserial = box_with_mecapture_fixture['box']['serial']

    capturesample_older = box_with_mecapture_fixture['clisthelper'].writtencaptures[0]['samples'][2]
    capturesample_newer = box_with_mecapture_fixture['clisthelper'].writtencaptures[0]['samples'][0]

    loc_older = location_fixture.post(capturesample_older['id'], description="test location")
    loc_newer = location_fixture.post(capturesample_newer['id'], description="test location 2")

    expected_first_id = loc_newer['id']
    expected_second_id = loc_older['id']

    endtime = capturesample_newer['timestamp']

    response = location_fixture.get_list(boxserial=boxserial, endtime=endtime)

    # Ensure that results are correctly ordered with the location belonging to the newest capturesample first.
    assert (response[0]['id'] == expected_first_id) & (response[1]['id'] == expected_second_id)


def test_get_location(box_with_mecapture_fixture, location_fixture):
    capturesample = box_with_mecapture_fixture['clisthelper'].writtencaptures[0]['samples'][0]

    response = location_fixture.post(capturesample['id'], description="test location")
    posted_id = response['id']

    response = location_fixture.get(location_id=posted_id)

    assert response['id'] == posted_id


def test_patch_location(box_with_mecapture_fixture, location_fixture):
    capturesample = box_with_mecapture_fixture['clisthelper'].writtencaptures[0]['samples'][0]

    response = location_fixture.post(capturesample['id'], description="test location")
    posted_id = response['id']

    response = location_fixture.patch(location_id=posted_id, description="altered description")

    assert response['id'] == posted_id


def test_delete_location(box_with_mecapture_fixture, location_fixture):
    capturesample = box_with_mecapture_fixture['clisthelper'].writtencaptures[0]['samples'][0]

    response = location_fixture.post(capturesample['id'], description="test location")
    posted_id = response['id']

    status_code = location_fixture.delete(location_id=posted_id)

    assert status_code == 204

if __name__ == "__main__":
    pytest.main()
