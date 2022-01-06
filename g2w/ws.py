import os  # pragma: no cover
from typing import List

import requests  # pragma: no cover

"""
Worksection client that allows manipulation with
"""


class Ws:
    def __init__(
        self,
        email=os.getenv("WS_EMAIL"),
        system_user_id=os.getenv("WS_ADMIN_USER_ID"),
        all_users=os.getenv("WS_URL_ALL_USERS"),
        post_comment=os.getenv("WS_URL_POST_COMMENT"),
    ):
        self.system_email = email
        self.system_user_id = system_user_id
        self.url_all_users = all_users
        self.url_post_comment = post_comment

    users: List[dict] = []

    def all_users(self) -> List[dict]:
        if not self.users:
            # @todo #/DEV use memorize feature/approach instead of own caching.
            self.users.extend(requests.get(self.url_all_users).json()["data"])
        return self.users

    def add_comment(self, prj: int, task_id: int, body: str) -> dict:
        return requests.post(
            self.url_post_comment.format(prj, task_id, self.system_email, body)
        ).json()["data"]

    def find_user(self, email: str) -> dict:
        user = next((u for u in self.all_users() if u["email"] == email), None)
        if user is not None:
            return user
        if self.system_user_id is None:
            raise ValueError(
                "g2w-002: No user found with email {0}".format(email)
            )
        else:
            return next(
                (u for u in self.all_users() if u["id"] == self.system_user_id)
            )
