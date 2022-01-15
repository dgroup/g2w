import logging
import time
from typing import Callable

from fastapi import Request, Response
from fastapi.routing import APIRoute

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
            # @todo #58/DEV Ensure that logging is enabled for HTTP traffic and
            #  could be used.
            logging.debug("req duration: {0}", duration)
            logging.debug(
                "req: %s, duration: %s, resp: %s, resp. headers: %s",
                req,
                duration,
                resp,
                resp.headers,
            )
            return resp

        return custom_route_handler
