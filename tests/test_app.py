import os
import pytest
from fastapi.testclient import TestClient
from .conftest import AbstractTest


from g2w.__main__ import app


# Fake worksection api for unit testing purposes
# @todo #/DEV Fake worksection api implementation required
#  - https://requests-mock.readthedocs.io/en/latest/pytest.html
#  - https://stackoverflow.com/q/46865169/6916890
#  - https://stackoverflow.com/a/52065289/6916890


class ClientTest(AbstractTest):
    @pytest.mark.skipif(os.getenv("WS_ADMIN_EMAIL") is None, reason="Environment variable 'WS_ADMIN_EMAIL' is absent")
    @pytest.mark.skipif(os.getenv("WS_URL_ALL_USERS") is None, reason="Environment variable 'WS_URL_ALL_USERS' is absent")
    @pytest.mark.skipif(os.getenv("WS_URL_POST_COMMENT") is None, reason="Environment variable 'WS_URL_POST_COMMENT' is absent")
    @pytest.mark.skipif(os.getenv("WS_INT_TESTS_DISABLED") is not None, reason="Integration tests are disabled")
    def test_e2e_push(self):
        # ws = 'http://worksection.api'
        # requests_mock.get('http://test.com', text='data')
        response = TestClient(app).post("/gitlab/push/223728", json=self.body("sample2_commits.json"))
        self.assertEqual(response.status_code, 200)
        self.assertGreater(int(response.json()["comments"][0]["id"]), 0)

    @pytest.mark.skipif(os.getenv("WS_ADMIN_EMAIL") is None, reason="Environment variable 'WS_ADMIN_EMAIL' is absent")
    @pytest.mark.skipif(os.getenv("WS_URL_POST_TASK") is None, reason="Environment variable 'WS_URL_POST_TASK' is absent")
    @pytest.mark.skipif(os.getenv("WS_INT_TESTS_DISABLED") is not None, reason="Integration tests are disabled")
    def test_e2e_alert(self):
        response = TestClient(app).post("/grafana/alert/223728", json=self.body("sample1_alert.json"))
        self.assertEqual(response.status_code, 200)
        self.assertGreater(response.json()["created"]["id"], 0)
