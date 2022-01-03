import os
import pytest

from g2w import Ws

given = pytest.mark.parametrize


# @todo #/DEV Inspect more sophisticated ways how to use asserts during unit
#  testing like assertj/Hamcrest matchers for Java. So far the simple dict
#  approach is used https://stackoverflow.com/a/46809074/6916890
@pytest.mark.skipif(os.getenv("WS_URL_ALL_USERS") is None, reason="Environment variable 'WS_URL_ALL_USERS' is absent")
@pytest.mark.skipif(os.getenv("WS_URL_POST_COMMENT") is None, reason="Environment variable 'WS_URL_POST_COMMENT' is absent")
def test_users():
    assert len(Ws().all_users()) > 20
