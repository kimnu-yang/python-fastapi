import jwt
from datetime import datetime, timedelta, timezone

# JWT 설정
SECRET_KEY = "secretkey123!"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
ACCESS_TOKEN_EXPIRE_DAYS = 1


# Access/Refresh 토큰 생성
def create_tokens(data: dict) -> dict:
    to_encode = {"id": data["id"], "email": data["email"]}

    access_expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + access_expires_delta
    to_encode.update({"exp": expire})
    access_token = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    refresh_expires_delta = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    expire = datetime.now(timezone.utc) + refresh_expires_delta
    to_encode.update({"exp": expire})
    refresh_token = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    return {
        "access": access_token,
        "refresh": refresh_token
    }


# Access 토큰 생성
def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    access_expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + access_expires_delta
    to_encode.update({"exp": expire})
    access_token = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    return access_token


# 토큰 해독
def decode_token(token: str):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, ALGORITHM)
        return decoded_token
    except jwt.ExpiredSignatureError:
        return 1
    except jwt.InvalidTokenError:
        return 2
