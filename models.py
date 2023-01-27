from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    access_level = Column(String)  # read, write, admin


class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    service = Column(String)
    username = Column(String)
    ip_address = Column(Integer)
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), default=datetime.now)
