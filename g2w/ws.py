import logging  # pragma: no cover
import os  # pragma: no cover
from typing import List

import requests  # pragma: no cover


def env(key) -> str:
    val = os.getenv(key)
    if val is None:
        raise ValueError(f"g2w-003: Environment variable '{key}' not found")
    return val


def ws_admin_email() -> str:
    return env("WS_ADMIN_EMAIL")


def ws_admin_userid() -> str:
    return env("WS_ADMIN_USER_ID")


def post(req) -> dict:
    """
    Send POST request to Worksection API.
    """
    resp = requests.post(req).json()
    # @todo #58/DEV Ensure that logging is enabled for this method as well.
    logging.debug("WS req: '%s', resp: '%s'", req, resp)
    if resp["status"] == "ok":
        return resp["data"]
    else:
        return resp


class Ws:
    """
    Worksection client that allows manipulation with
    """

    users: List[dict] = []

    def find_user(self, email: str) -> dict:
        """
        Find user details in Worksection by email.
        Return user or system account (if not found).
        """
        user = next((u for u in self.all_users() if u["email"] == email), None)
        if user is not None:
            return user
        else:
            return next(
                (u for u in self.all_users() if u["id"] == ws_admin_userid())
            )

    def all_users(self) -> List[dict]:
        """
        Fetch all users from worksection space.
        """
        if not self.users:
            # @todo #/DEV use memorize feature/approach instead of own caching.
            self.users.extend(
                requests.get(env("WS_URL_ALL_USERS")).json()["data"]
            )
        return self.users

    def add_comment(self, prj: int, task: int, body: str) -> dict:
        """
        Add a comment to a particular worksection task id.
        """
        return post(self.post_comment_url(prj, task, body))

    def post_comment_url(self, prj, task, body) -> str:
        """
        Construct URL for posting comments.
        """
        return env("WS_URL_POST_COMMENT").format(
            prj,
            task,
            ws_admin_email(),
            body,
            env(f"WS_PRJ_{prj}_POST_COMMENT_HASH"),
        )

    def add_task(self, prj, subj, body) -> dict:
        """
        Add a ticket to a particular worksection project.
        """
        return post(self.post_task_url(prj, subj, body))

    def post_task_url(self, prj, subj, body) -> str:
        return env("WS_URL_POST_TASK").format(
            prj,
            subj,
            ws_admin_email(),
            body,
            env(f"WS_PRJ_{prj}_POST_TASK_HASH"),
        )
