# @todo #/DEV Replace requests framework by using
#  https://github.com/juancarlospaco/faster-than-requests
#  Their benchmarks shows that's faster, however own micro-benchmarks are
#  required.
import argparse  # pragma: no cover

import uvicorn  # pragma: no cover
from fastapi import Request, FastAPI
from fastapi.routing import APIRouter
import logging

from g2w import Push, Ws, LoggableRoute, Alert, __version__

ws = Ws()
app = FastAPI(version=__version__, title="g2w")
router = APIRouter(route_class=LoggableRoute)
logger = logging.getLogger("uvicorn")


@router.post(
    path="/gitlab/push/{project_id}",
    summary="Create a comment in worksection task from Gitlab push event",
)
def push(event: Push, project_id: int) -> dict:
    logger.debug("Got push event '%s' for project '%d'", event, project_id)
    author = ws.find_user(event.user_email)
    msg = event.comment(author)
    comments = []
    # @todo #/DEV Return 400 if no WS tasks found within commit messages
    for task_id in event.tasks():
        comments.append(ws.add_comment(project_id, task_id, msg))
    logger.debug("Added comments %s", comments)
    return {"comments": comments}


@router.post(
    path="/grafana/alert/{project_id}",
    summary="Create a ticket in worksection from Grafana's alert",
)
async def alert(event: Request, project_id: int) -> dict:
    # @todo #/DEV Replace plain json in ticket summary by more sophisticated
    #  object with proper formatting
    logger.debug("Got project id %d", project_id)
    alert = Alert()
    # @todo #/DEV Return the direct answer from Worksection instead of wrapping
    logger.debug("Adding task to project %d", project_id)
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
        required=False
    )
    cmd.add_argument(
        "--log",
        type=str,
        help="The default log level for apllication logs",
        default="WARNING",
        required=False
    )
    args = cmd.parse_args()
    logger.setLevel(args.log.upper())
    logger.debug('This message should go to the log file')
    logger.info('So should this')
    logger.warning('And this, too')
    logger.error('And non-ASCII stuff, too, like Øresund and Malmö')
    uvicorn.run(app, host="0.0.0.0", port=args.port)
    # @todo #/DEV Add prometheus client library for app monitoring
    #  https://github.com/prometheus/client_python


if __name__ == "__main__":  # pragma: no cover
    main()
