import logging  # pragma: no cover
import os  # pragma: no cover
from typing import List

import requests  # pragma: no cover

log = logging.getLogger(__name__)


def env(key) -> str:
    val = os.getenv(key)
    if val is None:
        raise ValueError(f"g2w-003: Environment variable '{key}' not found")
    log.debug("Env variable '%s'='%s'", key, val)
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
    log.debug("WS req: '%s', resp: '%s'", req, resp)
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
        log.debug("Got e-mail %s", email)
        user = next((u for u in self.all_users() if u["email"] == email), None)
        if user is None:
            user = next(
                (u for u in self.all_users() if u["id"] == ws_admin_userid())
            )
        log.debug("Found user %s", user)
        return user

    def all_users(self) -> List[dict]:
        """
        Fetch all users from worksection space.
        """
        if not self.users:
            # @todo #/DEV use memorize feature/approach instead of own caching.
            self.users.extend(
                requests.get(env("WS_URL_ALL_USERS")).json()["data"]
            )
        log.debug("Found %d worksection users", len(self.users))
        return self.users

    def add_comment(self, prj: int, task: int, body: str) -> dict:
        """
        Add a comment to a particular worksection task id.
        """
        url = self.post_comment_url(prj, task, body)
        log.debug("Add new comment by '%s' url based on text '%s'", url, body)
        return post(url)

    def post_comment_url(self, prj, task, body) -> str:
        """
        Construct URL for posting comments.
        """
        url = env("WS_URL_POST_COMMENT").format(
            prj,
            task,
            ws_admin_email(),
            body,
            env(f"WS_PRJ_{prj}_POST_COMMENT_HASH"),
        )
        log.debug("Constructing post url '%s'", url)
        return url

    def add_task(self, prj, subj, body) -> dict:
        """
        Add a ticket to a particular worksection project.
        """
        url = self.post_task_url(prj, subj, body)
        log.debug("Adding a ticket with url '%s' to project '%s'", url, prj)
        return post(url)

    def post_task_url(self, prj, subj, body) -> str:
        """
        Construct Worksection API url for new tickets creation
          https://worksection.com/faq/api-task.html#q1577
        where
         - 'WS_URL_POST_TASK' env variable with Worksection endpoint URL
         - 'WS_PRJ_{YOUR_PROJECT_ID}_POST_TASK_HASH' env variable with
            Worksection md5 hash for this action:
             /project/{YOUR_PROJECT_ID}/post_task{YOUR_API_KEY}
        """
        url = env("WS_URL_POST_TASK").format(
            prj,
            subj,
            ws_admin_email(),
            body,
            env(f"WS_PRJ_{prj}_POST_TASK_HASH"),
        )
        log.debug("Constructing task url '%s'", url)
        return url
