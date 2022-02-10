from g2w import Alert
import unittest


# @todo #/DEV Create fake grafana alert event object based on
#  https://grafana.com/docs/grafana/latest/alerting/unified-alerting/contact-points/#webhook   # noqa: E501

class SimpleTest(unittest.TestCase):

    def test_comment(self):
        self.assertGreater(Alert().desc('{"user":"Tom"}').find("user%22%3A%22Tom"), 0)
