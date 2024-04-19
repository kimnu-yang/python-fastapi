from app.user.user_model import User
from app.common.api import success_response
from app.common.exception import duplicated_email, password_rule_violation, sign_in_data_not_match, invalid_jwt, \
    expired_jwt, undefined_error, jwt_data_not_match
from app.common.jwt import create_tokens, decode_token
import bcrypt
import re


# 사용자 생성
def create_user(db_session, username: str, email: str, password: str):
    # 이메일 중복 체크
    if email_check(db_session, email):
        return duplicated_email()
    # 비밀번호 규칙 체크
    if not bool(re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()-+=]).{8,}$", password)):
        return password_rule_violation()

    salt = bcrypt.gensalt()
    db_user = User(username=username, email=email, password=bcrypt.hashpw(password.encode('utf-8'), salt),
                   salt=salt)
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
def get_user(db_session, email: str, password: str):
    user = db_session.query(User).filter(User.email == email).first()
    if user is not None:
        if user.password == bcrypt.hashpw(password.encode('utf-8'), user.salt):
            token = create_tokens(user.to_dict())
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


def token_refresh(email: str, refresh_token: str):
    data = decode_token(refresh_token)
    print(data["email"] == email)
    if type(data) is dict:
        if data["email"] == email:
            return success_response({"access_token": data})
        else:
            return jwt_data_not_match()
    elif type(data) is int:
        if data == 1:
            return invalid_jwt()
        elif data == 2:
            return expired_jwt()
        else:
            return undefined_error()
    else:
        return undefined_error()
