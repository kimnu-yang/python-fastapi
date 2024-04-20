from fastapi import APIRouter, Request
from app.common.api import Api
from app.user.user_model import UserUpdateRequest
from app.user.user_service import user_update, token_refresh
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

router = APIRouter(
    prefix="/api/users",
    tags=["users"]
)

# 데이터베이스 연결 설정
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# 세션 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# SQLAlchemy 모델을 위한 베이스 클래스 생성
declarative_base().metadata.create_all(bind=engine)


@router.patch("/update")
async def update_user(request: Request, user: UserUpdateRequest) -> Api:
    return user_update(SessionLocal(), request, user)


@router.post("/refresh")
async def refresh_jwt(request: Request, email: str) -> Api:
    return token_refresh(request, email)
