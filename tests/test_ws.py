import os

import pytest

from g2w import Ws
from .test_push import fake_push_event

# @todo #/DEV Think about more elegant test ignorance procedure.
#  Right now this @pytest.mark.skipif looks too verbose.


@pytest.mark.skipif(os.getenv("WS_INT_TESTS_DISABLED") is not None, reason="Integration tests are disabled")
@pytest.mark.skipif(os.getenv("WS_URL_ALL_USERS") is None, reason="Environment variable 'WS_URL_ALL_USERS' is absent")
def test_users():
    assert len(Ws().all_users()) > 20


given = pytest.mark.parametrize


@pytest.mark.skipif(os.getenv("WS_INT_TESTS_DISABLED") is not None, reason="Integration tests are disabled")
@pytest.mark.skipif(os.getenv("WS_ADMIN_EMAIL") is None, reason="WS_ADMIN_EMAIL variable 'WS_URL_POST_COMMENT' is absent")
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
