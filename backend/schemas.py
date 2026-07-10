# schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from models import RoleEnum, MessageType

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    role: RoleEnum
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class MessageResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    content: Optional[str]
    message_type: MessageType
    file_url: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True