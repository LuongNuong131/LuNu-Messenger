# chat.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Dict, List
import jwt
from datetime import datetime

import models
import schemas
import auth
from database import get_db

router = APIRouter(prefix="/chat", tags=["Chat"])

# --- Quản lý kết nối WebSocket ---
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_personal_message(self, message: dict, receiver_id: int):
        if receiver_id in self.active_connections:
            websocket = self.active_connections[receiver_id]
            await websocket.send_json(message)

manager = ConnectionManager()

def get_current_user_ws(token: str, db: Session):
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
    except jwt.PyJWTError:
        return None
        
    user = db.query(models.User).filter(models.User.username == username).first()
    return user

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str, db: Session = Depends(get_db)):
    user = get_current_user_ws(token, db)
    if not user:
        await websocket.close(code=1008) 
        return

    await manager.connect(websocket, user.id)
    try:
        while True:
            data = await websocket.receive_json()
            receiver_id = data.get("receiver_id")
            
            new_msg = models.Message(
                sender_id=user.id,
                receiver_id=receiver_id,
                content=data.get("content"),
                message_type=data.get("message_type", "text"),
                file_url=data.get("file_url")
            )
            db.add(new_msg)
            db.commit()
            db.refresh(new_msg)

            msg_dict = {
                "id": new_msg.id,
                "sender_id": new_msg.sender_id,
                "receiver_id": new_msg.receiver_id,
                "content": new_msg.content,
                "message_type": new_msg.message_type,
                "file_url": new_msg.file_url,
                "created_at": new_msg.created_at.isoformat()
            }

            await manager.send_personal_message(msg_dict, receiver_id)
            await manager.send_personal_message(msg_dict, user.id)

    except WebSocketDisconnect:
        manager.disconnect(user.id)

@router.get("/history/{receiver_id}", response_model=List[schemas.MessageResponse])
def get_chat_history(receiver_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    messages = db.query(models.Message).filter(
        ((models.Message.sender_id == current_user.id) & (models.Message.receiver_id == receiver_id)) |
        ((models.Message.sender_id == receiver_id) & (models.Message.receiver_id == current_user.id))
    ).order_by(models.Message.created_at.asc()).all()
    return messages

# --- API Mới: Lấy những người đang có nhắn tin (những người có tin nhắn chưa bị xóa) ---
@router.get("/recent", response_model=List[schemas.UserResponse])
def get_recent_chats(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    messages = db.query(models.Message).filter(
        or_(models.Message.sender_id == current_user.id, models.Message.receiver_id == current_user.id)
    ).all()
    
    recent_user_ids = set()
    for msg in messages:
        if msg.sender_id != current_user.id:
            recent_user_ids.add(msg.sender_id)
        if msg.receiver_id != current_user.id:
            recent_user_ids.add(msg.receiver_id)
    
    if not recent_user_ids:
        return []
        
    recent_users = db.query(models.User).filter(models.User.id.in_(recent_user_ids)).all()
    return recent_users

@router.get("/users/search", response_model=List[schemas.UserResponse])
def search_users(keyword: str, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    if not keyword or not keyword.strip():
        return []
    
    users = db.query(models.User).filter(
        models.User.username.ilike(f"%{keyword}%"),
        models.User.id != current_user.id
    ).all()
    return users