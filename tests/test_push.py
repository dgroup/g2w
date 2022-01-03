# flake8: noqa
import pytest

from g2w import Push

given = pytest.mark.parametrize


# @todo #/DEV Inspect more sophisticated ways how to use asserts during unit
#  testing like assertj/Hamcrest matchers for Java. So far the simple dict
#  approach is used https://stackoverflow.com/a/46809074/6916890
def test_push():
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
        ).html()["ref"]
    )
