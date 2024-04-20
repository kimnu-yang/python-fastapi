from fastapi import APIRouter, Request
from app.common.api import Api
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.post.post_service import get_all_posts, create_post, get_post, update_post, delete_post

router = APIRouter(
    prefix="/open-api/posts",
    tags=["posts"]
)

# 데이터베이스 연결 설정
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# 세션 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# SQLAlchemy 모델을 위한 베이스 클래스 생성
declarative_base().metadata.create_all(bind=engine)


@router.get("")
async def all_post(sort: str = None, page: int = 1, size: int = 10) -> Api:
    return get_all_posts(SessionLocal(), sort, page, size)


@router.get("/{post_id}")
async def post_detail(post_id: int) -> Api:
    return get_post(SessionLocal(), post_id)
