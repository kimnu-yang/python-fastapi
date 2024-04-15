from fastapi import APIRouter
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.user import User, Base

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
def create_user(db_session, username: str, email: str):
    db_user = User(username=username, email=email)
    db_session.add(db_user)
    db_session.commit()
    db_session.refresh(db_user)
    return db_user


# 사용자 조회 함수
def get_user(db_session, user_id: int):
    return db_session.query(User).filter(User.id == user_id).first()


@router.get("")
async def read_root():
    create_user(SessionLocal(), "name", "email")
    print(get_user(SessionLocal(), 1))
    return get_user(SessionLocal(), 0)
