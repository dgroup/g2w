from .ws import Ws
from .api import Api

"""
The application that process Gitlab webhook notifications.
"""


class App:
    # @todo #20/DEV Start the API once its ready
    def start(self, port: int, api: Api, ws: Ws):
        print("started...", port, api, ws)
