import logging
import time
from typing import Callable

from fastapi import Request, Response
from fastapi.routing import APIRoute

log = logging.getLogger(__name__)

# @todo #/DEV Extract timings to a separate route.
"""
Interceptor that logs all for incoming requests/responses.
"""


class LoggableRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(req: Request) -> Response:
            before = time.time()
            resp: Response = await original_route_handler(req)
            duration = time.time() - before
            resp.headers["X-Response-Time"] = str(duration)
            log.debug(
                "%s %s req='%s', duration='%.2fs', resp='%s'",
                req.method,
                req.url,
                req.__dict__,
                duration,
                resp.__dict__,
            )
            return resp

        return custom_route_handler
