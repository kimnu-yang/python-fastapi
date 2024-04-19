from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True)
    password = Column(String)
    username = Column(String)
    salt = Column(String)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }


class UserCreateRequest(BaseModel):
    username: str
    email: str
    password: str


class UserSignInRequest(BaseModel):
    email: str
    password: str


class UserUpdateRequest(BaseModel):
    email: str
    username: str = None
    password: str = None


class TokenRefreshRequest(BaseModel):
    email: str
    refresh_token: str
