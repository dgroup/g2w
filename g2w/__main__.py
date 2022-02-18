# @todo #/DEV Replace requests framework by using
#  https://github.com/juancarlospaco/faster-than-requests
#  Their benchmarks shows that's faster, however own micro-benchmarks are
#  required.
import argparse  # pragma: no cover
import logging

import uvicorn  # pragma: no cover
from fastapi import Request, FastAPI, Response, status
from fastapi.routing import APIRouter

from g2w import Push, Ws, LoggableRoute, Alert, Log, __version__
from prometheus_fastapi_instrumentator import Instrumentator

ws = Ws()
app = FastAPI(version=__version__, title="g2w")
router = APIRouter(route_class=LoggableRoute)
log = logging.getLogger(f"g2w.{__name__}")
Instrumentator().instrument(app).expose(app)


@router.post(
    path="/gitlab/push/{project_id}",
    summary="Create a comment in worksection task from Gitlab push event",
)
def push(event: Push, project_id: int, response: Response) -> dict:
    log.debug("Got push event '%s' for project '%d'", event, project_id)
    author = ws.find_user(event.user_email)
    msg = event.comment(author)
    comments = []
    if not event.tasks():
        response.status_code = status.HTTP_400_BAD_REQUEST
    for task_id in event.tasks():
        comments.append(ws.add_comment(project_id, task_id, msg))
    log.debug("Added comments %s", comments)
    return {"comments": comments}


@router.post(
    path="/grafana/alert/{project_id}",
    summary="Create a ticket in worksection from Grafana's alert",
)
async def alert(event: Request, project_id: int) -> dict:
    # @todo #/DEV Replace plain json in ticket summary by more sophisticated
    #  object with proper formatting
    log.debug("Got project id %d", project_id)
    alert = Alert()
    # @todo #/DEV Return the direct answer from Worksection instead of wrapping
    log.debug("Adding task to project %d", project_id)
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
    cmd.add_argument(
        "-log",
        "--log",
        type=str,
        help="The default log level for application logs",
        default="WARNING",
        required=False,
    )
    cmd.add_argument(
        "--log-file",
        type=str,
        help="The default log format application logs",
        default="logconfig.yaml",
        required=False,
    )
    cmd.add_argument(
        "--log-format",
        type=str,
        help="The default formatter for primary(default) logger",
        default="[%(asctime)s] %(levelname)s tid=%(thread)d - %(message)s",
        required=False,
    )
    cmd.add_argument(
        "--host",
        type=str,
        help="The default host value",
        default="localhost",
        required=False,
    )
    args = cmd.parse_args()
    uvicorn.run(
        app,
        host=args.host,
        port=args.port,
        log_config=Log(
            args.log_file, args.log.upper(), args.log_format
        ).read(),
    )


if __name__ == "__main__":  # pragma: no cover
    main()
