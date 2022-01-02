import pytest

from g2w import App, Api, Ws

given = pytest.mark.parametrize


# Fake worksection api for unit testing purposes
# @todo #/DEV Fake worksection api implementation required


class FakeWs(Ws):
    def users(self) -> dict:
        return {}

    def add_comment(self, body) -> dict:
        print(body)
        return {}

    def comments(self) -> dict:
        return {}


def test_start():
    ws = FakeWs()
    App().start(8080, Api(), ws)
    # @todo #20/DEV send push notification to test endpoint
    assert ws.comments() is not None
