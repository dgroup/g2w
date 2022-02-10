import urllib.parse
import logging

import airspeed
from pydantic import BaseModel

log = logging.getLogger(__name__)


class Alert(BaseModel):
    """
    Alert event details from Grafana.
    """

    def desc(self, json) -> str:
        """
        Allows to transform Gitlab push event about multiple commits into HTML
        comment for worksection.
        """
        body = self.encode(
            airspeed.Template(
                """<pre><code class="code_init hljs json">$json
                                 </code></pre>"""
            ).merge(locals())
        )
        log.debug(
            "Transforming Gitlab push event into HTML comment '%s'.", body
        )
        return body

    def subject(self):
        return self.encode("Monitoring alert")

    # @todo #/DEV Move encode function to generic place as it will be used for
    #  all future Worksection requests:
    #  https://stackoverflow.com/a/30045261/6916890
    def encode(self, text: str) -> str:
        encoded = urllib.parse.quote_plus(text)
        log.debug("Encoded before '%s', after='%s'", text, encoded)
        return encoded
