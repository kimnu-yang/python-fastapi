import time
import uuid

from fastapi import Request

from app.common.function import password_validation
from app.models.user_model import User, UserCreateRequest, UserUpdateRequest, UserSignInRequest
from app.common.api import success_response
from app.common.exception import duplicated_email, password_rule_violation, sign_in_data_not_match, jwt_data_not_match, \
    not_found
from app.common.jwt import create_tokens, decode_token, create_access_token
import bcrypt


# 사용자 생성
def create_user(db_session, user: UserCreateRequest):
    # 이메일 중복 체크
    if email_check(db_session, user.email):
        return duplicated_email()
    # 비밀번호 규칙 체크
    if not password_validation(user.password):
        return password_rule_violation()

    salt = bcrypt.gensalt()
    db_user = User(username=user.username,
                   email=user.email,
                   password=bcrypt.hashpw(
                       user.password.encode('utf-8'),
                       salt
                   ), salt=salt)
    db_session.add(db_user)
    db_session.commit()
    db_session.refresh(db_user)
    return success_response(db_user.to_dict())


# 이메일 중복 검사
def email_check(db_session, email: str):
    user = db_session.query(User).filter(User.email == email).first()
    if user is not None:
        return True
    else:
        return False


# 사용자 조회
def get_user(db_session, user: UserSignInRequest):
    data = db_session.query(User).filter(User.email == user.email).first()
    if data:
        if data.password == bcrypt.hashpw(user.password.encode('utf-8'), data.salt):
            token = create_tokens(data.to_dict())
            return success_response(
                {
                    "access_token": token["access"],
                    "refresh_token": token["refresh"]
                }
            )
        else:
            return sign_in_data_not_match()
    else:
        return sign_in_data_not_match()


def get_user_by_id(db_session, user_id: int):
    data = db_session.query(User).filter(User.id == user_id).first()
    return data.to_dict()


# 사용자 정보 갱신
def user_update(db_session, request: Request, user: UserUpdateRequest):
    token = request.headers.get("authorized-key")
    token_data = decode_token(token)

    if token_data["email"] == user.email:
        data = db_session.query(User).filter(user.email == User.email).first()
        if data:
            if user.username is not None:
                data.username = user.username
            if user.password is not None:
                if password_validation(user.password):
                    salt = bcrypt.gensalt()
                    data.salt = salt
                    data.password = bcrypt.hashpw(user.password.encode("utf-8"), salt)
                else:
                    return password_rule_violation()

            db_session.commit()
            db_session.refresh(data)
            return success_response({"user_id": data.id})
        else:
            return not_found()
    else:
        return jwt_data_not_match()


def token_refresh(request: Request, email: str):
    data = decode_token(request.headers.get("authorized-key"))
    if data["email"] == email:
        return success_response({"access_token": create_access_token({"email": data["email"]})})
    else:
        return jwt_data_not_match()


# 회원 탈퇴
def delete_user(db_session, request: Request, password: str):
    token_data = decode_token(request.headers.get("authorized-key"))
    db_data = db_session.query(User).filter(User.id == token_data["id"]).first()
    if db_data:
        if db_data.password == bcrypt.hashpw(password.encode('utf-8'), db_data.salt):
            db_data.username = "탈퇴한 유저"
            db_data.email = str(uuid.uuid4()) + str(time.time())
            db_data.password = ""

            db_session.commit()
            db_session.refresh(db_data)
            return success_response({"deleted_user_id": db_data.id})
        else:
            return sign_in_data_not_match()
    else:
        return not_found()
