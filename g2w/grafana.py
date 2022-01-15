import urllib.parse

import airspeed
from pydantic import BaseModel


class Alert(BaseModel):
    """
    Alert event details from Grafana.
    """

    def desc(self, json) -> str:
        """
        Allows to transform Gitlab push event about multiple commits into HTML
        comment for worksection.
        """
        return self.encode(
            airspeed.Template(
                """<pre><code class="code_init hljs json">$json
                                 </code></pre>"""
            ).merge(locals())
        )

    def subject(self):
        return self.encode("Monitoring alert")

    # @todo #/DEV Move encode function to generic place as it will be used for
    #  all future Worksection requests:
    #  https://stackoverflow.com/a/30045261/6916890
    def encode(self, text: str) -> str:
        return urllib.parse.quote_plus(text)
