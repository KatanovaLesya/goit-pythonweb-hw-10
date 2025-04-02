from database import engine, Base
from models import Contact

print("📦 Створюємо таблиці у базі...")

Base.metadata.create_all(bind=engine)

print("✅ Таблиці успішно створено!")
