import re
import urllib.parse
from typing import List

import airspeed
from pydantic import BaseModel

# @todo #/DEV Worksection task id in the middle (or end) might be in message
#  not only at the begining. It could be in the middle or end. It would be good
#  to support such cases as from app perspective we need Worksection task id
#  only and doesn't matter where it in message exactly...
commit_msg_pattern = re.compile(r"^#WS-(\d+):.+$")

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

    """
    Gitlab push commit SHA url
    """

    def push_sha(self) -> str:
        return self.project["homepage"] + "/-/commit/" + self.checkout_sha

    def quantity(self) -> str:
        return "commits" if self.total_commits_count > 1 else "commit"

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
        return urllib.parse.quote_plus(
            airspeed.Template(t).merge(
                {
                    "push_url": self.push_sha(),
                    "commits_count": self.total_commits_count,
                    "quantity": self.quantity(),
                    "branch_url": self.ref,
                    "branch_name": self.ref,
                    "user_id": author["id"],
                    "user_logo": author["avatar"],
                    "user_name": author["name"],
                    "commits": self.commits,
                    "commit_url": self.project["homepage"] + "/-/commit/",
                }
            )
        )

    """
    Extract worksection task id from Gitlab commit message
    """

    def tasks(self) -> List[int]:
        return list(
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
