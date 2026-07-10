# database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Tự động tìm và nạp các biến môi trường từ file .env
load_dotenv()

# Lấy chuỗi kết nối từ file .env (Bảo mật 100%, không lộ code)
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Aiven MySQL bắt buộc kết nối phải có chứng chỉ bảo mật SSL
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    pool_pre_ping=True,
    connect_args={"ssl": {}} 
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()