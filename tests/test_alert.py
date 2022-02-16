from g2w import Alert
from .conftest import AbstractTest


class AlertTest(AbstractTest):
    def test_comment(self):
        self.assertGreater(Alert().desc('{"user":"Tom"}').find("user%22%3A%22Tom"), 0)
