from typing import Callable, Awaitable

from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from config import ALLOW_ORIGINS, FORBIDDEN_PAGES

from re import search

class ForbiddenPagesMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        response = await call_next(request)

        url = str(request.url)
        client = str(request.client)

        if not any(
            [page for page in FORBIDDEN_PAGES if bool(search(page, url))]
        ):
            return response

        if not any(
            [origin for origin in ALLOW_ORIGINS if bool(search(origin, client))]
        ):
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={
                    'status': False,
                    'err_description': 'Forbidden!!!'
                }
            )

        return response