from fastapi import APIRouter, Request
from app.common.api import Api
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.post.post_service import create_post, update_post, delete_post
from app.post.post_model import PostCreateRequest, PostUpdateRequest

router = APIRouter(
    prefix="/api/posts",
    tags=["posts"]
)

# 데이터베이스 연결 설정
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# 세션 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# SQLAlchemy 모델을 위한 베이스 클래스 생성
declarative_base().metadata.create_all(bind=engine)


@router.post("")
async def post_write(request: Request, post: PostCreateRequest) -> Api:
    return create_post(request, SessionLocal(), post)


@router.patch("/{post_id}")
async def post_update(request: Request, post_id: int, post: PostUpdateRequest) -> Api:
    return update_post(request, SessionLocal(), post_id, post)


@router.delete("/{post_id}")
async def post_delete(request: Request, post_id) -> Api:
    return delete_post(request, SessionLocal(), post_id)
