"""
Worksection client that allows manipulation with
"""


# @todo #/DEV Create ctor that receives worksection connection details and
#  connects to remote worksection instance
class Ws:
    # @todo #/DEV Return worksection users associated with account in WS.
    #  It should be collection of users
    def users(self) -> dict:
        print("tbd")
        return {}

    # @todo #/DEV Add comment to worksection
    def add_comment(self, body) -> dict:
        print(body)
        return {}
