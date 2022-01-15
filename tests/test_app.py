import os
import pytest
from fastapi.testclient import TestClient

from g2w.__main__ import app


# Fake worksection api for unit testing purposes
# @todo #/DEV Fake worksection api implementation required
#  - https://requests-mock.readthedocs.io/en/latest/pytest.html
#  - https://stackoverflow.com/q/46865169/6916890
#  - https://stackoverflow.com/a/52065289/6916890


# @todo #/DEV Move push event details into a separate *.json file.
#  For example, the `json.load` or `pkg_resources` from `setuptools` might
#  be used:
#  - https://stackoverflow.com/a/37151805/6916890
#  - https://stackoverflow.com/a/1396657/6916890
#  - https://setuptools.pypa.io/en/latest/pkg_resources.html


@pytest.mark.skipif(os.getenv("WS_ADMIN_EMAIL") is None, reason="Environment variable 'WS_ADMIN_EMAIL' is absent")
@pytest.mark.skipif(os.getenv("WS_URL_ALL_USERS") is None, reason="Environment variable 'WS_URL_ALL_USERS' is absent")
@pytest.mark.skipif(os.getenv("WS_URL_POST_COMMENT") is None, reason="Environment variable 'WS_URL_POST_COMMENT' is absent")
@pytest.mark.skipif(os.getenv("WS_INT_TESTS_DISABLED") is not None, reason="Integration tests are disabled")
def test_e2e_push():
    # ws = 'http://worksection.api'
    # requests_mock.get('http://test.com', text='data')
    response = TestClient(app).post(
        "/gitlab/push/223728",
        json={
            "object_kind": "push",
            "event_name": "push",
            "before": "95790bf891e76fee5e1747ab589903a6a1f80f22",
            "after": "da1560886d4f094c3e6c9ef40349f7d38b5d27d7",
            "ref": "refs/heads/master",
            "checkout_sha": "da1560886d4f094c3e6c9ef40349f7d38b5d27d7",
            "user_id": 4,
            "user_name": "John Smith",
            "user_username": "jsmith",
            "user_email": "john@example.com",
            "user_avatar": "https://s.gravatar.com/avatar/d4c74594d841139328695756648b6bd6?s=8://s.gravatar.com/avatar/d4c74594d841139328695756648b6bd6?s=80",
            "project_id": 15,
            "project": {
                "id": 15,
                "name": "Diaspora",
                "description": "",
                "web_url": "https://example.com/mike/diaspora",
                "avatar_url": None,
                "git_ssh_url": "git@example.com:mike/diaspora.git",
                "git_http_url": "https://example.com/mike/diaspora.git",
                "namespace": "Mike",
                "visibility_level": 0,
                "path_with_namespace": "mike/diaspora",
                "default_branch": "master",
                "homepage": "https://example.com/mike/diaspora",
                "url": "git@example.com:mike/diaspora.git",
                "ssh_url": "git@example.com:mike/diaspora.git",
                "http_url": "https://example.com/mike/diaspora.git",
            },
            "repository": {
                "name": "Diaspora",
                "url": "git@example.com:mike/diaspora.git",
                "description": "",
                "homepage": "https://example.com/mike/diaspora",
                "git_http_url": "https://example.com/mike/diaspora.git",
                "git_ssh_url": "git@example.com:mike/diaspora.git",
                "visibility_level": 0,
            },
            "commits": [
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
                    "message": "#WS-6231285: fixed readme",
                    "title": "#WS-6231285: fixed readme",
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
            "total_commits_count": 2,
        },
    )
    assert response.status_code == 200
    assert int(response.json()["comments"][0]["id"]) > 0
