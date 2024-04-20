import json

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.common.jwt import decode_token
from app.models.log_model import Log


class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        host = request.client.host
        url = request.url
        method = request.method
        user_id = ""

        token = request.headers.get("authorized-key")
        if token:
            token_data = decode_token(token)
            if type(token_data) is dict:
                user_id = token_data["id"]

        # GET 요청은 request 데이터가 없으니 쿼리 파라미터로 처리
        if method != "GET":
            req_data = await request.json()
        else:
            req_data = dict(request.query_params)

        response = await call_next(request)
        res_status = response.status_code

        # 데이터베이스 연결 설정
        SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
        engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

        # 세션 생성
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db_session = SessionLocal()

        # SQLAlchemy 모델을 위한 베이스 클래스 생성
        declarative_base().metadata.create_all(bind=engine)

        log = Log(user_id=user_id, host=host, url=str(url), method=method, req_data=json.dumps(req_data), res_status=res_status)
        db_session.add(log)
        db_session.commit()
        db_session.refresh(log)

        return response
