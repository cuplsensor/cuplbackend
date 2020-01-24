import pytest



def test_mecaptures(two_captures_on_two_boxes_fixture, mecapture_fixture):
    boxcaptures = two_captures_on_two_boxes_fixture

    expected = list()
    expected.extend(boxcaptures[0]['clisthelper'].writtencaptures)
    expected.extend(boxcaptures[1]['clisthelper'].writtencaptures)
    expected.reverse() # We expect captures in order from newest to oldest

    # Remove keys because these are not returned by the captures API
    # and will cause any comparisons to fail.
    for capture in expected:
        del capture['samples']
        del capture['box_id']
        del capture['parent_box']

    mecapturesout = mecapture_fixture.get()

    for capture in mecapturesout:
        del capture['boxserial']

    assert expected == mecapturesout


def test_mecaptures_distinct(two_captures_on_two_boxes_fixture, mecapture_fixture):
    boxcaptures = two_captures_on_two_boxes_fixture

    mecapturesin = list()
    mecapturesin.append(boxcaptures[1]['clisthelper'].writtencaptures[1])
    mecapturesin.append(boxcaptures[0]['clisthelper'].writtencaptures[1])

    # Remove keys because these are not returned by the captures API
    # and will cause any comparisons to fail.
    for capture in mecapturesin:
        del capture['samples']
        del capture['box_id']
        del capture['parent_box']

    mecapturesout = mecapture_fixture.get(distinct=True)

    for capture in mecapturesout:
        del capture['boxserial']

    assert mecapturesin == mecapturesout


if __name__ == "__main__":
    pytest.main()
