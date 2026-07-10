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
from dotenv import load_dotenv

load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="LuNu Messenger API", version="1.0.0")

# Lấy link Vercel từ biến môi trường (Mặc định cho phép localhost để test)
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL, "http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

app.mount("/static", StaticFiles(directory=UPLOAD_DIR), name="static")

app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(admin.router)

@app.on_event("startup")
def startup_event():
    start_scheduler()

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...), current_user: models.User = Depends(auth.get_current_user)):
    try:
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".webp", ".png", ".bmp"]
        if file_extension.lower() in image_extensions:
            msg_type = "image"
        else:
            msg_type = "file"
            
        file_url = f"/static/{unique_filename}"
        
        return {
            "filename": file.filename,
            "file_url": file_url,
            "message_type": msg_type
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi hệ thống khi upload tệp tin: {str(e)}")