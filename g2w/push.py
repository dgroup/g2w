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
    def html(self) -> dict:
        """
        Allows to transform Gitlab push event into HTML comment for
        worksection.
        """
        # @todo #/DEV Find a way how to escape text in order to send it as
        #  HTTP parameter
        return self.dict()
