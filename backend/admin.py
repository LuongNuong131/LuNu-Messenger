# admin.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import inspect, text
import models
import schemas
import auth
from database import get_db, engine

router = APIRouter(prefix="/admin", tags=["Admin Management"])

# --- Dependency kiểm tra xem có phải Admin thực sự không ---
def check_admin(current_user: models.User = Depends(auth.get_current_user)):
    if current_user.role != models.RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Bạn không có quyền truy cập vào khu vực này!")
    return current_user

# --- API lấy toàn bộ danh sách User ---
@router.get("/users", response_model=list[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db), _: models.User = Depends(check_admin)):
    return db.query(models.User).all()

# --- API xóa một User khỏi hệ thống ---
@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), _: models.User = Depends(check_admin)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User không tồn tại")
    db.delete(user)
    db.commit()
    return {"message": f"Đã xóa thành công người dùng: {user.username}"}

# --- API Nâng cấp quyền Admin ---
@router.put("/users/{user_id}/promote")
def promote_user(user_id: int, db: Session = Depends(get_db), _: models.User = Depends(check_admin)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User không tồn tại")
    if user.role == models.RoleEnum.admin:
        raise HTTPException(status_code=400, detail="User này đã là Admin rồi!")
    
    user.role = models.RoleEnum.admin
    db.commit()
    return {"message": f"Đã thăng cấp Admin cho: {user.username}"}

# --- API Quản lý Database Mini: Lấy danh sách toàn bộ các Bảng ---
@router.get("/db/tables")
def list_db_tables(_: models.User = Depends(check_admin)):
    inspector = inspect(engine)
    return inspector.get_table_names()

# --- API Quản lý Database Mini: Lấy cấu trúc cột và dữ liệu của một bảng chỉ định ---
@router.get("/db/table/{table_name}")
def get_table_data(table_name: str, db: Session = Depends(get_db), _: models.User = Depends(check_admin)):
    inspector = inspect(engine)
    if table_name not in inspector.get_table_names():
        raise HTTPException(status_code=404, detail="Bảng dữ liệu không tồn tại trong Database")
    
    columns = [col["name"] for col in inspector.get_columns(table_name)]
    result = db.execute(text(f"SELECT * FROM `{table_name}` LIMIT 100"))
    rows = [dict(zip(columns, row)) for row in result]
    
    return {
        "columns": columns,
        "rows": rows
    }