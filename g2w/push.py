from typing import List

from pydantic import BaseModel

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

    # @todo #/DEV Transform PUSH json event into HTML comment
    #  The json format you might find here: https://bit.ly/3JvWtEx
    #  Don't forget about unit tests from push.py as they have simple skeleton
    #  so far.
    def multiple_commits(self, author) -> str:
        """
        Allows to transform Gitlab push event about multiple commits into HTML
        comment for worksection.
        """
        # @todo #/DEV Find a way how to escape text in order to send it as
        #  HTTP parameter
        return ""

    def single_commit(self, author) -> str:
        """
        Allows to transform Gitlab push event about single commit into HTML
        comment for worksection.
        """
        return ""

    """
    Worksection task ids fetched from commit messages.
    """

    def tasks(self) -> List[int]:
        if self.total_commits_count <= 0:
            raise ValueError(
                "g2w-001: No commits found within push event",
                self.ref,
                self.checkout_sha,
                self.after,
                self.commits,
            )
        # @todo #/DEV Detect task id from commit messages
        return []
