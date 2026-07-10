# models.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from database import Base

class RoleEnum(str, enum.Enum):
    admin = "admin"
    user = "user"

class MessageType(str, enum.Enum):
    text = "text"
    image = "image"
    file = "file"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.user)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Quan hệ hai chiều để truy vấn tin nhắn dễ dàng
    messages_sent = relationship("Message", foreign_keys="[Message.sender_id]", back_populates="sender", cascade="all, delete-orphan")
    messages_received = relationship("Message", foreign_keys="[Message.receiver_id]", back_populates="receiver", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Lưu nội dung tin nhắn hoặc tên của file/ảnh
    content = Column(Text, nullable=True) 
    
    # Phân loại tin nhắn để frontend biết đường render (hiển thị chữ, thẻ <img> hay nút Download)
    message_type = Column(Enum(MessageType), default=MessageType.text)
    
    # URL trỏ đến vị trí file lưu trên server
    file_url = Column(String(255), nullable=True) 
    
    created_at = Column(DateTime, default=datetime.utcnow)

    sender = relationship("User", foreign_keys=[sender_id], back_populates="messages_sent")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="messages_received")