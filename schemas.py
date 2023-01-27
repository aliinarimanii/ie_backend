from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class User(BaseModel):
    username: Optional[str]
    email: Optional[str]
    password: Optional[str]
    access_level: Optional[str]
    
    class Config:
        orm_mode = True


class Log(BaseModel):
    service: Optional[str]
    username: Optional[str]
    ip_address: Optional[str]
    content: Optional[str]
    created_at: Optional[datetime]
    
    class Config:
        orm_mode = True


class Token(User):
    access_token: str
    token_type: str


class IPAddressRange(BaseModel):
    from_address: str
    to_address: str
