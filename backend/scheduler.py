# scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import models
from database import SessionLocal

def delete_old_messages():
    """
    Hàm này sẽ tự động xóa các tin nhắn cũ hơn 60 phút.
    """
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Đang quét và dọn dẹp tin nhắn cũ hơn 60 phút...")
    db = SessionLocal()
    try:
        # Tính thời điểm mốc (Hiện tại trừ đi 60 phút)
        time_threshold = datetime.utcnow() - timedelta(minutes=60)
        
        # Tìm các record có created_at nhỏ hơn time_threshold và xóa trực tiếp
        deleted_count = db.query(models.Message).filter(models.Message.created_at < time_threshold).delete()
        db.commit()
        
        if deleted_count > 0:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] LuNu-Messenger đã xóa tự động {deleted_count} tin nhắn.")
    except Exception as e:
        print(f"Lỗi khi thực thi background job xóa tin nhắn: {e}")
        db.rollback()
    finally:
        db.close()

def start_scheduler():
    scheduler = BackgroundScheduler()
    # Lên lịch chạy mỗi 1 phút
    scheduler.add_job(delete_old_messages, 'interval', minutes=1)
    scheduler.start()