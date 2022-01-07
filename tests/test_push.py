import pytest

from g2w import Push

given = pytest.mark.parametrize

"""
Fake Gitlab push event object
"""
fake_push_event = Push(
    ref="refs/heads/master",
    user_name="John Smith",
    user_username="jsmith",
    user_email="john@example.com",
    total_commits_count=2,
    object_kind="push",
    event_name="push",
    before="95790bf891e76fee5e1747ab589903a6a1f80f22",
    after="da1560886d4f094c3e6c9ef40349f7d38b5d27d7",
    checkout_sha="da1560886d4f094c3e6c9ef40349f7d38b5d27d7",
    project={
        "homepage": "https://example.com/mike/diaspora",
    },
    commits=[
        {
            "id": "b6568db1bc1dcd7f8b4d5a946b0b91f9dacd7327",
            "message": "Update Catalan translation to e38cb41.\n\nSee https://gitlab.com/gitlab-org/gitlab for more information",
            # noqa: E501
            "title": "Update Catalan translation to e38cb41.",
            "timestamp": "2011-12-12T14:27:31+02:00",
            "url": "https://example.com/mike/diaspora/commit/b6568db1bc1dcd7f8b4d5a946b0b91f9dacd7327",
            # noqa: E501
            "author": {"name": "Jordi Mallach", "email": "jordi@softcatala.org"},
            "added": ["CHANGELOG"],
            "modified": ["app/controller/application.rb"],
            "removed": [],
        },
        {
            "id": "da1560886d4f094c3e6c9ef40349f7d38b5d27d7",
            "message": "#WS-6231285: fixed readme",
            "title": "#WS-6231285: fixed readme",
            "timestamp": "2012-01-03T23:36:29+02:00",
            "url": "https://example.com/mike/diaspora/commit/da1560886d4f094c3e6c9ef40349f7d38b5d27d7",
            # noqa: E501
            "author": {
                "name": "GitLab dev user",
                "email": "gitlabdev@dv6700.(none)",
            },
            "added": ["CHANGELOG"],
            "modified": ["app/controller/application.rb"],
            "removed": [],
        },
    ],
)


# @todo #/DEV Inspect more sophisticated ways how to use asserts during unit
#  testing like assertj/Hamcrest matchers for Java. So far the simple dict
#  approach is used https://stackoverflow.com/a/46809074/6916890


def test_ctor():
    assert fake_push_event.ref == "refs/heads/master"


def test_multiple_commits_message():
    comment = fake_push_event.comment({"id": 10, "avatar": "https://logo.com?id=10", "name": "John Smith"})
    assert_str_has(comment, "%3Ca+href%3D%22https%3A%2F%2Fexample.com%2Fmike%2Fdiaspora%2F-%2Fcommit%2Fda1560886d4f094c3e6c9ef40349f7d38b5d27d7")  # noqa: E501
    assert_str_has(comment, "da1560886d4f094c3e6c9ef40349f7d38b5d27d7")
    assert_str_has(comment, "b6568db1bc1dcd7f8b4d5a946b0b91f9dacd7327")
    assert_str_has(comment, "2+new+commits%3C", "2 commits summary is exist")
    assert_str_has(comment, "+rel%3D%2210", "User with id 10 is mentioned")


# @todo #17/DEV Replace assert below by well-known standard statement:
#  https://docs.pytest.org/en/6.2.x/assert.html
#  https://understandingdata.com/list-of-python-assert-statements-for-unit-tests # noqa: E501


def assert_str_has(origin: str, substr: str, msg: str = None):
    found = origin.find(substr) >= 0
    if msg:
        assert found, msg
    else:
        assert found, "String '{0}' contains '{1}".format(origin, substr)


def test_task_id_is_present_as_plain_id():
    assert fake_push_event.tasks() == [6231285]
