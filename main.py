from fastapi import FastAPI
from app import user, post
from app.middleware.jwt_middleware import JwtMiddleware

app = FastAPI()

app.add_middleware(JwtMiddleware)
app.include_router(user.user_api_controller.router)
app.include_router(user.user_open_api_controller.router)
app.include_router(post.post_api_controller.router)
app.include_router(post.post_open_api_controller.router)
