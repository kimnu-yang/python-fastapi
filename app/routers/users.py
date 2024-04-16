from fastapi import APIRouter
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import User, Base
from app.common.api import success_response
import bcrypt

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# 데이터베이스 연결 설정
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# 세션 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# SQLAlchemy 모델을 위한 베이스 클래스 생성
Base.metadata.create_all(bind=engine)


# 사용자 생성 함수
def create_user(db_session, username: str, email: str, password: str):
    salt = bcrypt.gensalt()
    db_user = User(username=username, email=email, password=bcrypt.hashpw(password.encode('utf-8'), salt), salt=salt)
    db_session.add(db_user)
    db_session.commit()
    db_session.refresh(db_user)
    return db_user


# 사용자 조회 함수
def get_user(db_session, user_id: int):
    user = db_session.query(User).filter(User.id == user_id).first()
    return user.to_dict()


# @router.post("")
# async def sign_up():
#     return success_response(create_user(SessionLocal(), "name", "email", "password"))
#

@router.get("")
async def read_root():
    return success_response(get_user(SessionLocal(), 1))
