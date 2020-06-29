import pytest



def test_mecaptures(two_captures_on_two_tags_fixture, mecapture_fixture):
    tagcaptures = two_captures_on_two_tags_fixture

    expected = list()
    expected.extend(tagcaptures[0]['clisthelper'].writtencaptures)
    expected.extend(tagcaptures[1]['clisthelper'].writtencaptures)
    expected.reverse() # We expect captures in order from newest to oldest

    # Remove keys because these are not returned by the captures API
    # and will cause any comparisons to fail.
    for capture in expected:
        del capture['samples']
        del capture['tag_id']
        del capture['parent_tag']

    mecapturesout = mecapture_fixture.get()

    for capture in mecapturesout:
        del capture['tagserial']

    assert expected == mecapturesout


def test_mecaptures_distinct(two_captures_on_two_tags_fixture, mecapture_fixture):
    tagcaptures = two_captures_on_two_tags_fixture

    mecapturesin = list()
    mecapturesin.append(tagcaptures[1]['clisthelper'].writtencaptures[1])
    mecapturesin.append(tagcaptures[0]['clisthelper'].writtencaptures[1])

    # Remove keys because these are not returned by the captures API
    # and will cause any comparisons to fail.
    for capture in mecapturesin:
        del capture['samples']
        del capture['tag_id']
        del capture['parent_tag']

    mecapturesout = mecapture_fixture.get(distinct=True)

    for capture in mecapturesout:
        del capture['tagserial']

    assert mecapturesin == mecapturesout


if __name__ == "__main__":
    pytest.main()
