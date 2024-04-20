from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from app.common.exception import invalid_jwt, expired_jwt, undefined_error
from app.common.jwt import decode_token


class JwtMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        path = request.url.path
        method = request.method
        if path.split("/")[1] == "api" and method != "GET":
            token = request.headers.get("authorized-key")
            if token is None:
                return JSONResponse(content=invalid_jwt().dict())

            token_data = decode_token(token)
            if type(token_data) is int:
                if token_data == 1:
                    return JSONResponse(content=expired_jwt().dict())
                elif token_data == 2:
                    return JSONResponse(content=invalid_jwt().dict())
                else:
                    return JSONResponse(content=undefined_error().dict())
            elif type(token_data) is not dict:
                return JSONResponse(content=undefined_error().dict())

        response = await call_next(request)

        return response
