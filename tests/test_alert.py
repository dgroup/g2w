from g2w import Alert


# @todo #/DEV Create fake grafana alert event object based on
#  https://grafana.com/docs/grafana/latest/alerting/unified-alerting/contact-points/#webhook   # noqa: E501


def test_comment():
    assert Alert().desc('{"user":"Tom"}').find("user%22%3A%22Tom") > 0
