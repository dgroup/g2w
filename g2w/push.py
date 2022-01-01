"""
Push event to Gitlab.

Allows to transform Gitlab push event into HTML comment for worksection.
"""


class Push:
    # @todo #/DEV Transform PUSH json event into HTML comment
    #  The json format you might find here: https://bit.ly/3JvWtEx
    #  Don't forget about unit tests from push.py as they have simple skeleton
    #  so far.
    def html(self, event) -> dict:
        # @todo #/DEV Find a way how to escape text in order to send it as
        #  HTTP parameter
        return event
