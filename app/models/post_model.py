from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone
from pydantic import BaseModel

Base = declarative_base()


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    writer = Column(String, nullable=False)
    content = Column(String, nullable=False)
    hits = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "writer": self.writer,
            "content": self.content,
            "hits": self.hits,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


class PostCreateRequest(BaseModel):
    title: str
    content: str


class PostUpdateRequest(BaseModel):
    title: str = None
    content: str = None
