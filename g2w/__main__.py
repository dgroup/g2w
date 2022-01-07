# @todo #/DEV Replace requests framework by using
#  https://github.com/juancarlospaco/faster-than-requests
#  Their benchmarks shows that's faster, however own micro-benchmarks are
#  required.
import argparse  # pragma: no cover

import uvicorn  # pragma: no cover
from fastapi import FastAPI

from g2w import Push, Ws


# @todo #/DEV Add support of command line parser for program arguments


def main() -> None:  # pragma: no cover
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
    # @todo #/DEV Add prometheus client library for app monitoring
    #  https://github.com/prometheus/client_python


ws = Ws()
app = FastAPI()


# @todo #/DEV add logging framework and remove `print` statement everywhere


@app.post("/gitlab/push/{project_id}")
def push(event: Push, project_id: int) -> dict:
    author = ws.find_user(event.user_email)
    msg = event.comment(author)
    comments = []
    # @todo #/DEV Return 400 if no WS tasks found within commit messages
    for task_id in event.tasks():
        comments.append(ws.add_comment(project_id, task_id, msg))
    return {"comments": comments}


if __name__ == "__main__":  # pragma: no cover
    main()
