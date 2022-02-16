import pytest
import unittest

from g2w import Push
from .conftest import AbstractTest

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
        {
            "id": "da1560886d4f094c3e6c9ef40349f7d38b5d27d8",
            "message": "The message regarding #WS-100510",
            "title": "#WS-100510: fixed readme",
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
        {
            "id": "da1560886d4f094c3e6c9ef40349f7d38b5d27d9",
            "message": "It fix for #WS-1234567 that we are waiting",
            "title": "#WS-1234567: fixed readme",
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


class PushTest(AbstractTest):
    def test_ctor(self):
        self.assertEqual(fake_push_event.ref, "refs/heads/master")

    def test_multiple_commits_message(self):
        comment = fake_push_event.comment({"id": 10, "avatar": "https://logo.com?id=10", "name": "John Smith"})
        self.assertIn("%3Ca+href%3D%22https%3A%2F%2Fexample.com%2Fmike%2Fdiaspora%2F-%2Fcommit%2Fda1560886d4f094c3e6c9ef40349f7d38b5d27d7", comment)  # noqa: E501
        self.assertIn("da1560886d4f094c3e6c9ef40349f7d38b5d27d7", comment)
        self.assertIn("b6568db1bc1dcd7f8b4d5a946b0b91f9dacd7327", comment)
        self.assertIn("2+new+commits%3C", comment, "2 commits summary is exist")
        self.assertIn("+rel%3D%2210", comment, "User with id 10 is mentioned")

    def test_task_id_is_present_as_plain_id(self):
        self.assertEqual(fake_push_event.tasks(), [6231285, 100510, 1234567])

    def test_branch_url(self):
        self.assertEqual(fake_push_event.branch_url(), "https://example.com/mike/diaspora/tree/master")  # noqa: E501
