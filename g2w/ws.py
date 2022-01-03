import os  # pragma: no cover
from typing import List

import requests  # pragma: no cover

"""
Worksection client that allows manipulation with
"""


class Ws:
    def __init__(
        self,
        all_users=os.getenv("WS_URL_ALL_USERS"),
        post_comment=os.getenv("WS_URL_POST_COMMENT"),
    ):
        self.url_all_users = all_users
        self.url_post_comment = post_comment

    users: List[dict] = []

    def all_users(self) -> List[dict]:
        if not self.users:
            self.users.extend(self.get(self.url_all_users))
        return self.users

    # @todo #/DEV Add comment to worksection system
    def add_comment(self, body) -> dict:
        print(body)
        return {}

    def get(self, url) -> dict:
        return requests.get(url).json()["data"]
