# main.py
import os
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uuid

import models
from database import engine
import auth
import chat
import admin
from scheduler import start_scheduler

# Tự động đồng bộ cấu trúc, tạo các bảng dữ liệu bên trong MySQL Aiven nếu chưa tồn tại
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="LuNu Messenger API", version="1.0.0")

# Cấu hình CORS - Cho phép VueJS ở Frontend có thể gọi API mà không bị chặn
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Bạn có thể đổi cụ thể thành ["http://localhost:5173"] khi chạy Frontend Vue
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cấu hình thư mục lưu trữ file upload trên server cục bộ
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Mount thư mục tĩnh để có thể click xem ảnh hoặc tải file về trực tiếp qua link URL
app.mount("/static", StaticFiles(directory=UPLOAD_DIR), name="static")

# Đăng ký các cụm API thành phần vào Server chính
app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(admin.router)

# Sự kiện chạy khi Server khởi động thành công
@app.on_event("startup")
def startup_event():
    # Kích hoạt Background Job dọn dẹp tin nhắn sau 60 phút
    start_scheduler()

# API Upload hình ảnh hoặc tài liệu đính kèm khi nhắn tin
@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...), current_user: models.User = Depends(auth.get_current_user)):
    try:
        # Băm lại tên file bằng chuỗi UUID để tránh bị trùng tên đè file trên hệ thống
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        # Ghi tệp tin vào ổ đĩa cứng của server
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        # Nhận diện định dạng tệp tin để phân chia hiển thị ở Frontend
        image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".webp", ".png", ".bmp"]
        if file_extension.lower() in image_extensions:
            msg_type = "image"
        else:
            msg_type = "file"
            
        # Trả về URL tương đối trỏ đến thư mục tĩnh
        file_url = f"/static/{unique_filename}"
        
        return {
            "filename": file.filename,
            "file_url": file_url,
            "message_type": msg_type
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi hệ thống khi upload tệp tin: {str(e)}")

# Lệnh chạy server thực tế từ terminal: uvicorn main:app --reload --port 8000