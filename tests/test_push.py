# flake8: noqa
import pytest

from g2w import Push

given = pytest.mark.parametrize


# @todo #/DEV Inspect more sophisticated ways how to use asserts during unit
#  testing like assertj/Hamcrest matchers for Java. So far the simple dict
#  approach is used https://stackoverflow.com/a/46809074/6916890
def test_ctor():
    assert (
        "refs/heads/master"
        == Push(
            ref="refs/heads/master",
            user_name="John Smith",
            user_username="jsmith",
            user_email="john@example.com",
            total_commits_count=4,
            object_kind="push",
            event_name="push",
            before="95790bf891e76fee5e1747ab589903a6a1f80f22",
            after="da1560886d4f094c3e6c9ef40349f7d38b5d27d7",
            checkout_sha="da1560886d4f094c3e6c9ef40349f7d38b5d27d7",
        ).ref
    )


def test_multiple_commits_message():
    comment = Push(
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
                "title": "Update Catalan translation to e38cb41.",
                "timestamp": "2011-12-12T14:27:31+02:00",
                "url": "https://example.com/mike/diaspora/commit/b6568db1bc1dcd7f8b4d5a946b0b91f9dacd7327",
                "author": {"name": "Jordi Mallach", "email": "jordi@softcatala.org"},
                "added": ["CHANGELOG"],
                "modified": ["app/controller/application.rb"],
                "removed": [],
            },
            {
                "id": "da1560886d4f094c3e6c9ef40349f7d38b5d27d7",
                "message": "fixed readme",
                "title": "fixed readme",
                "timestamp": "2012-01-03T23:36:29+02:00",
                "url": "https://example.com/mike/diaspora/commit/da1560886d4f094c3e6c9ef40349f7d38b5d27d7",
                "author": {
                    "name": "GitLab dev user",
                    "email": "gitlabdev@dv6700.(none)",
                },
                "added": ["CHANGELOG"],
                "modified": ["app/controller/application.rb"],
                "removed": [],
            },
        ],
    ).comment({"id": 10, "avatar": "https://logo.com?id=10", "name": "John Smith"})
    assert comment.find('<a href="https://example.com/mike/diaspora/-/commit/b6568db1bc1dcd7f8b4d5a946b0b91f9dacd7327"') == 501
    assert comment.find('<a href="https://example.com/mike/diaspora/-/commit/da1560886d4f094c3e6c9ef40349f7d38b5d27d7"') == 0
    assert comment.find("2 new commits") == 110
    assert comment.find('rel="10"') == 294
