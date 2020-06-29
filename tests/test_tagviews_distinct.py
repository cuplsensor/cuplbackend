import pytest


@pytest.fixture(scope="function")
def two_tags_with_two_tagviews_fixture(tag_fixture_b, user_fixture, tagview_fixture):
    tagviews_grouped_by_tag = list()

    tags = list()
    tags.append(tag_fixture_b.add())
    tags.append(tag_fixture_b.add())

    for tag in tags:
        bvlist = list()
        bvlist.append(tagview_fixture.post(tag['serial']))
        bvlist.append(tagview_fixture.post(tag['serial']))
        tagviews_grouped_by_tag.append(bvlist)

    return tagviews_grouped_by_tag


def test_tagviews(two_tags_with_two_tagviews_fixture, tagview_fixture):
    bvexpected = list()
    bvexpected.extend(two_tags_with_two_tagviews_fixture[0])
    bvexpected.extend(two_tags_with_two_tagviews_fixture[1])

    bvall = tagview_fixture.get(distinct=False)

    assert bvall == bvexpected

def test_tagviews_distinct(two_tags_with_two_tagviews_fixture, tagview_fixture):
    bvexpected = list()
    bvexpected.append(two_tags_with_two_tagviews_fixture[1][1])
    bvexpected.append(two_tags_with_two_tagviews_fixture[0][1])

    bvall = tagview_fixture.get(distinct=True)

    assert bvall == bvexpected

if __name__ == "__main__":
    pytest.main()
