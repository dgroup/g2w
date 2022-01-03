import os
import pytest

from g2w import Ws

given = pytest.mark.parametrize


@pytest.mark.skipif(os.getenv("WS_URL_ALL_USERS") is None, reason="Environment variable 'WS_URL_ALL_USERS' is absent")
def test_users():
    assert len(Ws().all_users()) > 20
