from g2w import Alert
import unittest


class AlertTest(unittest.TestCase):
    def test_comment(self):
        self.assertGreater(Alert().desc('{"user":"Tom"}').find("user%22%3A%22Tom"), 0)
