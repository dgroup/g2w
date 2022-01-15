import logging  # pragma: no cover
import os  # pragma: no cover
from typing import List

import requests  # pragma: no cover


def get_hash(prj) -> str:
    """
    Fetch project hash from environment variable.
    The naming format is 'WS_PRJ_0000_HASH', where '0000' is project id:
      WS_PRJ_0001_HASH: 12fjasdfsdfhk34hsdf
      WS_PRJ_0002_HASH: asf324i324jdfi23hfd
      ...
    """
    val = os.getenv(f"WS_PRJ_{prj}_HASH")
    if val is None:
        logging.error("g2w-003: No hash found for project id '%'", prj)
        raise ValueError("g2w-003: No hash found for project id '%'", prj)
    return val


def post(req) -> dict:
    """
    Send POST request to Worksection API.
    """
    resp = requests.post(req).json()
    # @todo #58/DEV Ensure that logging is enabled for this method as well.
    logging.debug("WS req: '%s', resp: '%s'", req, resp)
    return resp


class Ws:
    """
    Worksection client that allows manipulation with
    """
    def __init__(
        self,
        email=os.getenv("WS_ADMIN_EMAIL"),
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
        """
        Fetch all users from worksection space.
        """
        if not self.users:
            # @todo #/DEV use memorize feature/approach instead of own caching.
            self.users.extend(requests.get(self.url_all_users).json()["data"])
        return self.users

    def add_comment(self, prj: int, task: int, body: str) -> dict:
        """
        Add a comment to a particular worksection task id.
        """
        resp = post(self.post_comment_url(prj, task, body))
        if resp["status"] == "ok":
            return resp["data"]
        else:
            return resp

    def post_comment_url(self, prj, task, body) -> str:
        """
        Construct URL for posting comments.
        """
        return self.url_post_comment.format(
            prj, task, self.system_email, body, get_hash(prj)
        )

    def find_user(self, email: str) -> dict:
        """
        Find user details in Worksection by email.
        Return user or system account (if not found).
        """
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
