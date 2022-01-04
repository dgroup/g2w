# @todo #/DEV Replace requests framework by using
#  https://github.com/juancarlospaco/faster-than-requests
#  Their benchmarks shows that's faster, however own micro-benchmarks are
#  required.
import argparse  # pragma: no cover
import os  # pragma: no cover

import uvicorn  # pragma: no cover
from fastapi import FastAPI

from g2w import Push, Ws


# @todo #/DEV Fetch users data from worksection in order to get mapping between
#  Gitlab and WS users. It should be a class, which is collection and each
#  element is a user that represents json user from worksection.


# @todo #/DEV Add support of command line parser for program arguments


def main() -> None:  # pragma: no cover

    # @todo #/DEV Create a REST endpoint that receives the Gitlab push
    #  notification through the web-hook (https://bit.ly/3sGueNt)
    print("Executing main function")
    # @todo #/DEV Choose a simple REST API framework for pure python without
    #  any massive frameworks like django or flask. Add few tests and ensure
    #  that's it easy to test.
    print(os.environ.get("HOME", "/home/username/"))
    # @todo #/DEV Add prometheus client library for app monitoring
    #  https://github.com/prometheus/client_python


ws = Ws()
app = FastAPI()


# @todo #/DEV add logging framework and remove `print` statement everywhere


@app.post("/gitlab/push/{project_id}")
def push(event: Push, project_id: int) -> dict:
    who = next((u for u in ws.all_users() if u["email"] == event.user_email))
    if event.total_commits_count > 1:
        msg = event.multiple_commits(who)
    elif event.total_commits_count == 1:
        msg = event.single_commit(who)
    else:
        return {
            "status": 400,
            "message": "g2w-001: No commits found within push event",
        }
    resp = []
    for task_id in event.tasks():
        resp.append(ws.add_comment(project_id, task_id, msg))
    return {"comments": resp}


if __name__ == "__main__":  # pragma: no cover
    cmd = argparse.ArgumentParser()
    cmd.add_argument(
        "-p",
        "--port",
        type=int,
        help="The port to listen REST API endpoints",
        default=8080,
        required=False,
    )
    uvicorn.run(app, host="0.0.0.0", port=cmd.parse_args().port)
