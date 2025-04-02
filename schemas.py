from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

# 🧱 Базова модель
class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birthday: date
    additional_info: Optional[str] = None

# 🆕 Для створення
class ContactCreate(ContactBase):
    pass

# ✏️ Для оновлення
class ContactUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    birthday: Optional[date] = None
    additional_info: Optional[str] = None

# 📤 Для відповіді
class Contact(ContactBase):
    id: int

    class Config:
        orm_mode = True
