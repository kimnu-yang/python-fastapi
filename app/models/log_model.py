from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone

Base = declarative_base()


class Log(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String)
    host = Column(String)
    url = Column(String)
    method = Column(String)
    req_data = Column(String)
    res_status = Column(String)
    log_time = Column(DateTime, default=datetime.now(timezone.utc))