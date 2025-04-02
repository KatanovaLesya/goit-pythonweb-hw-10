from database import SessionLocal

try:
    db = SessionLocal()
    print("✅ Успішне підключення до бази!")
except Exception as e:
    print(f"❌ Помилка підключення: {e}")
finally:
    db.close()
