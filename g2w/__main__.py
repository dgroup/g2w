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
    # @todo #/DEV Invoke worksection REST API in order to test the E2E concept
    #  https://realpython.com/api-integration-in-python/
    #  https://worksection.com/faq/api-start.html
    print(os.environ.get("HOME", "/home/username/"))
    # @todo #/DEV Add prometheus client library for app monitoring
    #  https://github.com/prometheus/client_python


ws = Ws()
app = FastAPI()


@app.post("/gitlab/push")
def push(event: Push) -> dict:
    return {"checkout_sha": event.checkout_sha}


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
