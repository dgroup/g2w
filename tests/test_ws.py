import os

import pytest

from g2w import Ws
from .test_push import fake_push_event


@pytest.mark.skipif(os.getenv("WS_E2E_TESTS_DISABLED") is not None, reason="Integration tests are disabled")
@pytest.mark.skipif(os.getenv("WS_URL_ALL_USERS") is not None, reason="Environment variable 'WS_URL_ALL_USERS' is absent")
def test_users():
    assert len(Ws().all_users()) > 20


given = pytest.mark.parametrize


@pytest.mark.skipif(os.getenv("WS_E2E_TESTS_DISABLED") is not None, reason="Integration tests are disabled")
@pytest.mark.skipif(os.getenv("WS_EMAIL") is None, reason="Email account for worksection is absent")
@pytest.mark.skipif(os.getenv("WS_URL_POST_COMMENT") is None, reason="Environment variable 'WS_URL_POST_COMMENT' is absent")
def test_add_comment():
    assert (
        Ws().add_comment(
            223728,
            6231285,
            fake_push_event.comment({"id": "370080", "avatar": "https://worksection.com/images/avatar/mail/av_1_25.gif", "name": "mr. Bot from test_ws.py"}),  # noop
        )["id"]
        is not None
    )
