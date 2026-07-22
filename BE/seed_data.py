from database import SessionLocal
import models
import auth

db = SessionLocal()

existing = db.query(models.User).filter(models.User.email == "demo@example.com").first()
if existing:
    print("User demo đã tồn tại, bỏ qua.")
else:
    demo_user = models.User(
        email="demo@example.com",
        password_hash=auth.hash_password("demo123456")
    )
    db.add(demo_user)
    db.commit()
    print("Đã tạo user demo@example.com thành công.")

db.close()