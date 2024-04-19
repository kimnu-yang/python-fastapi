from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

from app import user, post

app = FastAPI()

app.include_router(user.user_controller.router)
app.include_router(post.post_controller.router)
