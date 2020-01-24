import pytest


@pytest.fixture(scope="function")
def two_boxes_with_two_boxviews_fixture(box_fixture_b, user_fixture, boxview_fixture):
    boxviews_grouped_by_box = list()

    boxes = list()
    boxes.append(box_fixture_b.add())
    boxes.append(box_fixture_b.add())

    for box in boxes:
        bvlist = list()
        bvlist.append(boxview_fixture.post(box['serial']))
        bvlist.append(boxview_fixture.post(box['serial']))
        boxviews_grouped_by_box.append(bvlist)

    return boxviews_grouped_by_box


def test_boxviews(two_boxes_with_two_boxviews_fixture, boxview_fixture):
    bvexpected = list()
    bvexpected.extend(two_boxes_with_two_boxviews_fixture[0])
    bvexpected.extend(two_boxes_with_two_boxviews_fixture[1])

    bvall = boxview_fixture.get(distinct=False)

    assert bvall == bvexpected

def test_boxviews_distinct(two_boxes_with_two_boxviews_fixture, boxview_fixture):
    bvexpected = list()
    bvexpected.append(two_boxes_with_two_boxviews_fixture[1][1])
    bvexpected.append(two_boxes_with_two_boxviews_fixture[0][1])

    bvall = boxview_fixture.get(distinct=True)

    assert bvall == bvexpected

if __name__ == "__main__":
    pytest.main()
