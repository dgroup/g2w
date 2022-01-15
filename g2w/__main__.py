# @todo #/DEV Replace requests framework by using
#  https://github.com/juancarlospaco/faster-than-requests
#  Their benchmarks shows that's faster, however own micro-benchmarks are
#  required.
import argparse  # pragma: no cover

import uvicorn  # pragma: no cover
from fastapi import Request, FastAPI
from fastapi.routing import APIRouter
from g2w import Push, Ws, LoggableRoute, Alert

# @todo #/DEV Add support of command line parser for program arguments
ws = Ws()
app = FastAPI()
router = APIRouter(route_class=LoggableRoute)


# @todo #/DEV add logging framework and remove `print` statement everywhere


@router.post("/gitlab/push/{project_id}")
def push(event: Push, project_id: int) -> dict:
    author = ws.find_user(event.user_email)
    msg = event.comment(author)
    comments = []
    # @todo #/DEV Return 400 if no WS tasks found within commit messages
    for task_id in event.tasks():
        comments.append(ws.add_comment(project_id, task_id, msg))
    return {"comments": comments}


@router.post("/grafana/alert/{project_id}")
async def alert(event: Request, project_id: int) -> dict:
    # @todo #/DEV Replace plain json in ticket summary by more sophisticated
    #  object with proper formatting
    alert = Alert()
    return {
        "created": ws.add_task(
            project_id, alert.subject(), alert.desc(await event.json())
        )
    }


app.include_router(router)


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


if __name__ == "__main__":  # pragma: no cover
    main()
