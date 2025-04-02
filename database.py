from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_USER = "lesyakatanova"
DB_PASSWORD = ""

DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "contacts_db"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Підключення до бази
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовий клас для моделей
Base = declarative_base()
