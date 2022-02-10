import re
import urllib.parse
import logging
from typing import List

import airspeed
from pydantic import BaseModel

log = logging.getLogger(__name__)

commit_msg_pattern = re.compile(r"#WS-(\d+)")

"""
Push event details from Gitlab.
"""


class Push(BaseModel):
    ref: str
    user_name: str
    user_username: str
    user_email: str
    total_commits_count: int
    project: dict = {}
    commits: List[dict] = []
    object_kind: str
    event_name: str
    before: str
    after: str
    checkout_sha: str

    def push_sha(self) -> str:
        """
        Gitlab push commit SHA url
        """
        commit_url = (
            self.project["homepage"] + "/-/commit/" + self.checkout_sha
        )
        log.debug("Got commit url '%s'", commit_url)
        return commit_url

    def quantity(self) -> str:
        total = "commits" if self.total_commits_count > 1 else "commit"
        log.debug("Found %d %s", self.total_commits_count, total)
        return total

    def branch_url(self) -> str:
        prefix = "refs/heads/"
        if self.ref.index(prefix) == 0:
            branch = self.ref[len(prefix) :]
        else:
            branch = self.ref
        url = self.project["homepage"] + "/tree/" + branch
        log.debug("Returning branch url '%s'", url)
        return url

    """
    Allows to transform Gitlab push event about multiple commits into HTML
    comment for worksection.
    """

    def comment(self, author) -> str:
        t = """<a href="$push_url" target="_blank">$commits_count new $quantity</a>&nbsp;pushed to <b style="background: rgb(196, 255, 166)"><a href="$branch_url" target="_blank">$branch_name</a></b>&nbsp;by&nbsp; <span class="invite invite_old" rel="$user_id"><img src="$user_logo" class="av_sm av_i" width="24" height="24" alt="">$user_name</span>&nbsp;
                <br>
                <ul>
                    #foreach ($commit in $commits)
                        <li><a href="$commit_url$commit.id" target="_blank">$commit.id</a>&nbsp;-&nbsp;$commit.message</li>
                    #end
                </ul>
            """  # noqa: E501
        body = urllib.parse.quote_plus(
            airspeed.Template(t).merge(
                {
                    "push_url": self.push_sha(),
                    "commits_count": self.total_commits_count,
                    "quantity": self.quantity(),
                    "branch_url": self.branch_url(),
                    "branch_name": self.ref,
                    "user_id": author["id"],
                    "user_logo": author["avatar"],
                    "user_name": author["name"],
                    "commits": self.commits,
                    "commit_url": self.project["homepage"] + "/-/commit/",
                }
            )
        )
        log.debug("Leaving a comment '%s'", body)
        return body

    """
    Extract worksection task id from Gitlab commit message
    """

    def tasks(self) -> List[int]:
        ids = list(
            filter(
                lambda ticket_id: ticket_id > 0,
                map(
                    lambda m: 0 if m is None else int(m.group(1)),
                    filter(
                        lambda m: m is not None and int(m.group(1)) > 0,
                        map(
                            lambda c: commit_msg_pattern.search(c["message"]),
                            self.commits,
                        ),
                    ),
                ),
            )
        )
        log.debug(
            "Extract worksection task ids '%s' from Gitlab commit message", ids
        )
        return ids
