from app.common.api import Api


# 이메일 중복
def duplicated_email():
    return Api(status="400", message="Duplicated email", data={})


# 패스워드 생성 규칙 위반
def password_rule_violation():
    return Api(status="400", message="Password rule violation", data={})


def too_long_title():
    return Api(status="400", message="Too long title (100 limit)", data={})


# 로그인 데이터 불일치
def sign_in_data_not_match():
    return Api(status="401", message="Email or Password not matching", data={})


# 유효하지 않은 JWT
def invalid_jwt():
    return Api(status="401", message="Invalid token", data={})


# 기간이 만료된 JWT
def expired_jwt():
    return Api(status="401", message="Token expired", data={})


# JWT 데이터가 일치하지 않음
def jwt_data_not_match():
    return Api(status="401", message="JWT data not matching", data={})


# 수정/삭제 권한이 없음
def not_permitted():
    return Api(status="401", message="delete/update is not permitted", data={})


# 일치하는 데이터가 없음
def not_found():
    return Api(status="404", message="Data not found", data={})


# 정의되지 않은 오류
def undefined_error():
    return Api(status="500", message="Undefined error", data={})