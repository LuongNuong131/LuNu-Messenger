# chat.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from sqlalchemy.orm import Session
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
        # Lưu kết nối hiện tại: key là user_id, value là WebSocket object
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

# --- Hàm xác thực User qua WebSocket Token ---
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

# --- Endpoint WebSocket chính ---
@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str, db: Session = Depends(get_db)):
    user = get_current_user_ws(token, db)
    if not user:
        await websocket.close(code=1008) # 1008: Policy Violation (Token sai)
        return

    await manager.connect(websocket, user.id)
    try:
        while True:
            # Lắng nghe tin nhắn từ Frontend gửi lên
            data = await websocket.receive_json()
            receiver_id = data.get("receiver_id")
            
            # Lưu tin nhắn vào Database
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

            # Đóng gói dữ liệu để gửi đi
            msg_dict = {
                "id": new_msg.id,
                "sender_id": new_msg.sender_id,
                "receiver_id": new_msg.receiver_id,
                "content": new_msg.content,
                "message_type": new_msg.message_type,
                "file_url": new_msg.file_url,
                "created_at": new_msg.created_at.isoformat()
            }

            # Bắn tin nhắn qua cho người nhận (nếu họ đang mở chat)
            await manager.send_personal_message(msg_dict, receiver_id)
            # Bắn ngược lại cho người gửi để cập nhật giao diện
            await manager.send_personal_message(msg_dict, user.id)

    except WebSocketDisconnect:
        manager.disconnect(user.id)

# --- API Lấy lịch sử chat 1-1 ---
@router.get("/history/{receiver_id}", response_model=List[schemas.MessageResponse])
def get_chat_history(receiver_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    messages = db.query(models.Message).filter(
        ((models.Message.sender_id == current_user.id) & (models.Message.receiver_id == receiver_id)) |
        ((models.Message.sender_id == receiver_id) & (models.Message.receiver_id == current_user.id))
    ).order_by(models.Message.created_at.asc()).all()
    return messages

# --- API Tìm kiếm User để mở hộp thoại chat ---
@router.get("/users/search", response_model=List[schemas.UserResponse])
def search_users(keyword: str, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    if not keyword or not keyword.strip():
        return []
    
    # Tìm theo tên (bỏ qua phân biệt hoa thường) và loại trừ chính bản thân mình ra
    users = db.query(models.User).filter(
        models.User.username.ilike(f"%{keyword}%"),
        models.User.id != current_user.id
    ).all()
    return users