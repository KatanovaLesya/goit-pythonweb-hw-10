from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime, timedelta

from models import Contact
from schemas import ContactCreate, ContactUpdate


# Створити новий контакт
def create_contact(db: Session, contact: ContactCreate):
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


# Отримати всі контакти
def get_contacts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Contact).offset(skip).limit(limit).all()


# Отримати контакт по ID
def get_contact(db: Session, contact_id: int):
    return db.query(Contact).filter(Contact.id == contact_id).first()


# Оновити контакт
def update_contact(db: Session, contact_id: int, updated_data: ContactUpdate):
    db_contact = get_contact(db, contact_id)
    if db_contact:
        for field, value in updated_data.dict(exclude_unset=True).items():
            setattr(db_contact, field, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact


# Видалити контакт
def delete_contact(db: Session, contact_id: int):
    db_contact = get_contact(db, contact_id)
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact


# Пошук по імені, прізвищу або email
def search_contacts(db: Session, query: str):
    return db.query(Contact).filter(
        or_(
            Contact.first_name.ilike(f"%{query}%"),
            Contact.last_name.ilike(f"%{query}%"),
            Contact.email.ilike(f"%{query}%")
        )
    ).all()


# Дні народження в найближчі 7 днів
def get_upcoming_birthdays(db: Session):
    today = datetime.today().date()
    in_seven_days = today + timedelta(days=7)
    contacts = db.query(Contact).all()
    upcoming = []

    for contact in contacts:
        if contact.birthday:
            bday_this_year = contact.birthday.replace(year=today.year)
            if today <= bday_this_year <= in_seven_days:
                upcoming.append(contact)

    return upcoming
